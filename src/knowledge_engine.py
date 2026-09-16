import json
import os
import re
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.models import ScientificCitation

class HybridKnowledgeEngine:
    """
    Hybrid RAG Knowledge Retrieval Engine.
    Combines dense TF-IDF n-gram vectorization with keyword semantic matching and
    structured domain filtering across peer-reviewed ecological literature.
    """
    def __init__(self, corpus_path: Optional[str] = None):
        if corpus_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            corpus_path = os.path.join(base_dir, "data", "knowledge_corpus.json")
        self.corpus_path = corpus_path
        self.documents: List[Dict[str, Any]] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self._load_and_index_corpus()

    def _load_and_index_corpus(self):
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Knowledge corpus not found at: {self.corpus_path}")

        with open(self.corpus_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        # Build combined text representations for indexing
        corpus_texts = []
        for doc in self.documents:
            keywords_str = " ".join(doc.get("keywords", []))
            metrics_str = " ".join([f"{k}: {v}" for k, v in doc.get("metrics_impacted", {}).items()])
            full_text = (
                f"{doc.get('title', '')} {doc.get('authors', '')} {doc.get('domain', '')} "
                f"{keywords_str} {doc.get('summary', '')} {doc.get('ecological_mechanisms', '')} "
                f"{doc.get('applicability', '')} {metrics_str}"
            )
            corpus_texts.append(full_text)

        # Vectorize using word and char n-grams for robust matching
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=5000,
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus_texts)

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        domain_filter: Optional[str] = None,
        min_relevance: float = 0.08
    ) -> List[ScientificCitation]:
        """
        Retrieves top relevant scientific citations for a query using hybrid scoring.
        """
        if not query.strip() or self.vectorizer is None:
            return []

        # TF-IDF query representation
        query_vec = self.vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Keyword booster
        query_words = set(re.findall(r'\w+', query.lower()))
        boosted_scores = []

        for idx, doc in enumerate(self.documents):
            base_score = float(sim_scores[idx])
            
            # Domain filter check
            if domain_filter and doc.get("domain") != domain_filter:
                boosted_scores.append((0.0, idx))
                continue

            # Check keyword overlaps
            doc_keywords = set([k.lower() for k in doc.get("keywords", [])])
            overlap = len(query_words.intersection(doc_keywords))
            keyword_boost = overlap * 0.05

            final_score = base_score + keyword_boost
            boosted_scores.append((final_score, idx))

        # Sort descending by score
        boosted_scores.sort(key=lambda x: x[0], reverse=True)

        results: List[ScientificCitation] = []
        for score, idx in boosted_scores[:top_k]:
            if score < min_relevance and len(results) >= 2:
                continue
            doc = self.documents[idx]
            
            # Formulate concise relevant finding
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
