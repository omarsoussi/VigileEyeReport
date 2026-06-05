#!/usr/bin/env python3
import re
from pathlib import Path

src = Path(__file__).resolve().parents[1] / 'main.tex'
dst = Path(__file__).resolve().parents[1] / 'main_pandoc.tex'
raw = src.read_text(encoding='utf-8')

# Extract only the document body between \begin{document} and \end{document}
m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", raw, flags=re.S)
if m:
    body = m.group(1)
else:
    body = raw

# Remove \input{image_paths} (we'll leave \includegraphics lines alone)
body = re.sub(r"\\input\{image_paths\}", "", body)

# Replace custom \Path...{file} with the inner path only
def strip_path_cmd(m):
    s = m.group(0)
    inner = re.search(r"\{(.*)\}", s)
    return inner.group(1) if inner else s
body = re.sub(r"\\Path[A-Za-z0-9_]*\{.*?\}", strip_path_cmd, body)

# Simplify figure environments: remove float specifiers like [H] or [htbp]
body = re.sub(r"\\begin\{figure\}\[[^\]]*\]", "\\begin{figure}", body)

# Fix corrupted \begin sequences (sometimes a backslash was lost)
body = body.replace('egin{figure}', '\\begin{figure}')
body = body.replace('egin{table}', '\\begin{table}')

# Remove some layout-only commands that don't affect content
remove_patterns = [r"\\onehalfspacing", r"\\sloppy", r"\\raggedbottom",
                   r"\\setlength\{\\textfloatsep\}.*?\\n",
                   r"\\setcounter\{.*?\}.*?\\n", r"\\renewcommand\{.*?\}.*?\\n"]
for p in remove_patterns:
    body = re.sub(p, '', body)

# Minimal preamble for Pandoc to accept the file
preamble = """\\documentclass{article}
\\usepackage{graphicx}
\\begin{document}
"""

out = preamble + body + "\\end{document}\n"
dst.write_text(out, encoding='utf-8')
print(f"Wrote {dst}")
