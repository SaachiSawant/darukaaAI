import json
import os
import re
import math
from typing import List, Dict, Any, Optional
from src.models import ScientificCitation

from src.embedded_data import EMBEDDED_KNOWLEDGE_CORPUS

class HybridKnowledgeEngine:
    """
    Hybrid RAG Knowledge Retrieval Engine.
    Combines n-gram TF-IDF vectorization with keyword semantic matching and
    structured domain filtering across peer-reviewed ecological literature.
    Resilient across both local environments and Serverless (Vercel) runtimes.
    """
    def __init__(self, corpus_path: Optional[str] = None):
        if corpus_path is None:
            candidates = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "knowledge_corpus.json"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "knowledge_corpus.json"),
                os.path.join(os.getcwd(), "data", "knowledge_corpus.json"),
                os.path.join(os.getcwd(), "api", "data", "knowledge_corpus.json"),
                os.path.join(os.path.dirname(os.getcwd()), "data", "knowledge_corpus.json")
            ]
            for c in candidates:
                if os.path.exists(c):
                    corpus_path = c
                    break

        self.corpus_path = corpus_path
        self.documents: List[Dict[str, Any]] = []
        self.doc_vectors: List[Dict[str, float]] = []
        self.idf: Dict[str, float] = {}
        self._load_and_index_corpus()

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', text.lower())
        tokens = []
        for i in range(len(words)):
            tokens.append(words[i])
            if i < len(words) - 1:
                tokens.append(f"{words[i]}_{words[i+1]}")
        return tokens

    def _load_and_index_corpus(self):
        if self.corpus_path and os.path.exists(self.corpus_path):
            with open(self.corpus_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
        else:
            self.documents = EMBEDDED_KNOWLEDGE_CORPUS.copy()

        N = len(self.documents)
        doc_freqs: Dict[str, int] = {}
        doc_token_counts: List[Dict[str, int]] = []

        for doc in self.documents:
            keywords_str = " ".join(doc.get("keywords", []))
            metrics_str = " ".join([f"{k}: {v}" for k, v in doc.get("metrics_impacted", {}).items()])
            full_text = (
                f"{doc.get('title', '')} {doc.get('authors', '')} {doc.get('domain', '')} "
                f"{keywords_str} {doc.get('summary', '')} {doc.get('ecological_mechanisms', '')} "
                f"{doc.get('applicability', '')} {metrics_str}"
            )
            tokens = self._tokenize(full_text)
            counts: Dict[str, int] = {}
            for t in tokens:
                counts[t] = counts.get(t, 0) + 1
            doc_token_counts.append(counts)

            for t in counts.keys():
                doc_freqs[t] = doc_freqs.get(t, 0) + 1

        # Calculate IDF
        self.idf = {}
        for t, df in doc_freqs.items():
            self.idf[t] = math.log((N + 1) / (df + 1)) + 1.0

        # Calculate TF-IDF vectors
        self.doc_vectors = []
        for counts in doc_token_counts:
            vec: Dict[str, float] = {}
            norm_sq = 0.0
            for t, count in counts.items():
                tfidf = (1.0 + math.log(count)) * self.idf.get(t, 1.0)
                vec[t] = tfidf
                norm_sq += tfidf * tfidf
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            for t in vec:
                vec[t] /= norm
            self.doc_vectors.append(vec)

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        domain_filter: Optional[str] = None,
        min_relevance: float = 0.05
    ) -> List[ScientificCitation]:
        if not query.strip() or not self.documents:
            return []

        q_tokens = self._tokenize(query)
        q_counts: Dict[str, int] = {}
        for t in q_tokens:
            q_counts[t] = q_counts.get(t, 0) + 1

        # Vectorize query
        q_vec: Dict[str, float] = {}
        norm_sq = 0.0
        for t, count in q_counts.items():
            if t in self.idf:
                tfidf = (1.0 + math.log(count)) * self.idf[t]
                q_vec[t] = tfidf
                norm_sq += tfidf * tfidf
        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        for t in q_vec:
            q_vec[t] /= norm

        query_words = set(re.findall(r'\w+', query.lower()))
        boosted_scores = []

        for idx, doc in enumerate(self.documents):
            # Domain filter check
            if domain_filter and doc.get("domain") != domain_filter:
                boosted_scores.append((0.0, idx))
                continue

            # Dot product cosine similarity
            d_vec = self.doc_vectors[idx] if idx < len(self.doc_vectors) else {}
            cos_sim = sum(q_vec.get(t, 0.0) * d_vec.get(t, 0.0) for t in q_vec)

            # Keyword overlap boost
            doc_keywords = set([k.lower() for k in doc.get("keywords", [])])
            overlap = len(query_words.intersection(doc_keywords))
            final_score = cos_sim + (overlap * 0.05)
            boosted_scores.append((final_score, idx))

        boosted_scores.sort(key=lambda x: x[0], reverse=True)

        results: List[ScientificCitation] = []
        for score, idx in boosted_scores[:top_k]:
            if score < min_relevance and len(results) >= 2:
                continue
            doc = self.documents[idx]
            finding = f"{doc.get('summary')} Key Mechanism: {doc.get('ecological_mechanisms')}"
            
            citation = ScientificCitation(
                id=doc.get("id", "UNKNOWN"),
                title=doc.get("title", ""),
                authors=doc.get("authors", ""),
                year=doc.get("year", 2020),
                publisher=doc.get("publisher", ""),
                doi_or_url=doc.get("doi_or_url", ""),
                relevant_finding=finding,
                relevance_score=round(float(score), 3)
            )
            results.append(citation)

        return results

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        for doc in self.documents:
            if doc.get("id") == doc_id:
                return doc
        return None

    def get_all_domains(self) -> List[str]:
        return list(set([doc.get("domain", "") for doc in self.documents if doc.get("domain")]))
