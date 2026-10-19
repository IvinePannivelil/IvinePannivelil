"""
Builds preview.html from root README.md
Renders the approved README in a GitHub-like markdown container for local assessment.
"""
import markdown
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def build_preview():
    readme_path = ROOT / "README.md"
    content = readme_path.read_text(encoding="utf-8")
    
    # Python-Markdown needs explicit opt-in for Markdown inside HTML blocks.
    # Apply only to the renderer input, leaving the README unchanged.
    preview_content = content.replace(
        '<div align="center">', '<div align="center" markdown="1">'
    ).replace('<details>', '<details markdown="1">')
    rendered_body = markdown.markdown(
        preview_content, extensions=['extra', 'tables', 'fenced_code', 'md_in_html']
    )
    
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ivine P Sabu — Profile README Preview</title>
<link rel="icon" href="v4/motion-proof/favicon.ico" sizes="any">
<style>
:root {{
  color-scheme: dark;
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --heading: #f0f6fc;
  --muted: #8b949e;
  --link: #58a6ff;
  --cyan: #00d9ff;
  --orange: #ff7a00;
  --code-bg: rgba(110,118,129,0.4);
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ max-width: 100%; background: var(--bg); color: var(--text); font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif; font-size: 14px; line-height: 1.5; }}

/* Top Context Banner — Outside README composition */
.top-banner {{
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 10px 20px;
  font-size: 12px;
  color: var(--muted);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}}
.top-banner strong {{ color: var(--heading); }}
.badge-unverified {{
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  background: rgba(255, 122, 0, 0.12);
  border: 1px solid rgba(255, 122, 0, 0.35);
  color: var(--orange);
  font-family: ui-monospace, monospace;
}}
.banner-info {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}

/* README Container */
.readme-wrapper {{
  max-width: 980px;
  margin: 0 auto;
  padding: 28px 24px 72px;
}}
@media (max-width: 600px) {{
  .readme-wrapper {{ padding: 16px 12px 60px; }}
}}

/* GitHub Markdown Styling */
.markdown-body {{
  color: var(--text);
  font-size: 15px;
  line-height: 1.7;
  word-wrap: break-word;
}}
.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4 {{
  color: var(--heading);
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}}
.markdown-body h2 {{
  font-size: 1.5em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid var(--border);
}}
.markdown-body h3 {{ font-size: 1.25em; }}
.markdown-body h4 {{ font-size: 1em; }}
.markdown-body p, .markdown-body blockquote, .markdown-body ul, .markdown-body ol, .markdown-body table, .markdown-body pre, .markdown-body details {{
  margin-top: 0;
  margin-bottom: 16px;
}}
.markdown-body a {{ color: var(--link); text-decoration: none; }}
.markdown-body a:hover {{ text-decoration: underline; }}
.markdown-body blockquote {{
  padding: 0 1em;
  color: var(--muted);
  border-left: 0.25em solid #3b434b;
}}
.markdown-body hr {{
  height: 0.25em;
  padding: 0;
  margin: 24px 0;
  background-color: var(--border);
  border: 0;
}}
.markdown-body code {{
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  white-space: break-spaces;
  background-color: var(--code-bg);
  border-radius: 6px;
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
}}
.markdown-body ul {{
  padding-left: 2em;
  list-style-type: disc;
}}
.markdown-body li + li {{ margin-top: 0.25em; }}
.markdown-body details {{
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
}}
.markdown-body summary {{
  cursor: pointer;
  color: var(--heading);
}}
.markdown-body img {{
  max-width: 100%;
  box-sizing: content-box;
  display: block;
}}
.markdown-body picture img {{
  width: 100%;
  height: auto;
}}
.markdown-body div[align="center"] {{
  text-align: center;
}}
.markdown-body div[align="center"] img {{
  margin: 0 auto;
}}
.markdown-body a > img[src^="https://img.shields.io/"] {{
  display: inline-block;
  vertical-align: middle;
  margin: 3px 0;
}}
</style>
</head>
<body>

<!-- Outside README Composition: Banner -->
<header class="top-banner" role="region" aria-label="Preview metadata">
  <div class="banner-info">
    <strong>APPROVED PROFILE PREVIEW</strong> &middot; <code>README.md</code>
  </div>
  <div>
    <span class="badge-unverified">&#9888; Local Approximation &middot; Live GitHub rendering verified after push</span>
  </div>
</header>

<!-- The exact README markdown composition -->
<main class="readme-wrapper">
  <article class="markdown-body" id="readme-article">
{rendered_body}
  </article>
</main>

</body>
</html>
"""
    output_path = ROOT / "preview.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated {output_path} ({len(html)} bytes)")

if __name__ == "__main__":
    build_preview()
