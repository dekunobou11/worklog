# utils/markdown_parser.py
import markdown
from markupsafe import Markup

# Markdown文字列をHTMLに変換
def render_markdown(text):
    html = markdown.markdown(text, extensions=['fenced_code', 'codehilite', 'tables'])
    return Markup(html)
