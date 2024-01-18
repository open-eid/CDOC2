# Intro

This is testing, how to write documents with .md files and have the output rendered:

1. in a browser, like modern and cool mkdocs sites (see <https://www.mkdocs.org> or <https://squidfunk.github.io/mkdocs-material/>)
2. as printable PDF files (TODO)
3. as Confluence pages (possibly not required at all)

# Source code

Content is in directory `docs/`.

# Try in your computer 

Install `mkdocs` package (<https://pypi.org/project/mkdocs/>) and other dependencies:

```bash
pip3 install mkdocs
pip3 install pymdown-extensions
pip3 install katex
pip3 install markdown-katex
pip3 install mkdocs-enumerate-headings-plugin
pip3 install mkdocs-material
```

Then type in the active directory:
```bash
$ mkdocs serve
```

and open <http://127.0.0.1:8000/> in your browser.

# Test site

Open <https://people.cyber.ee/~aivo/mkdocs_try1/site/ch02_external_interfaces/>
