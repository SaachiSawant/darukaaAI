import os

def bundle():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    with open('static/style.css', 'r', encoding='utf-8') as f:
        css = f.read()
    with open('static/app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    css_tag = f"<style>\n{css}\n</style>"
    js_tag = f"<script>\n{js}\n</script>"

    bundled_html = html.replace('<link rel="stylesheet" href="/static/style.css">', css_tag)
    bundled_html = bundled_html.replace('<script src="/static/app.js"></script>', js_tag)

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(bundled_html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(bundled_html)

    code = f'''# Embedded static assets to guarantee 100% availability in serverless environments
INDEX_HTML = {repr(bundled_html)}
STYLE_CSS = {repr(css)}
APP_JS = {repr(js)}
'''
    with open('src/embedded_static.py', 'w', encoding='utf-8') as f:
        f.write(code)
    with open('api/src/embedded_static.py', 'w', encoding='utf-8') as f:
        f.write(code)

    print("Successfully bundled single-page app into index.html, static/index.html, and embedded_static.py!")

if __name__ == '__main__':
    bundle()
