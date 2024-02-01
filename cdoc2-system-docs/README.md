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
pip3 install plantuml_markdown
pip3 install python-markdown-comments
pip3 install mkdocs-awesome-pages-plugin
```

Then type in the active directory:
```bash
$ mkdocs serve
```

and open <http://127.0.0.1:8000/> in your browser.

# Test site

Open <https://people.cyber.ee/~aivo/mkdocs_try1/>

# Export to Confluence

## Install exporting tools

```bash
cd ..
git clone git@gitlab.cyber.ee:id/utilities/md-upload-to-confluence.git
cd md-upload-to-confluence
make build
```

```bash
cd ..
git clone https://github.com/kovetskiy/mark.git
cd mark
make build
```

## Export files to Confluence

```bash
cd cdoc2-architecture/mkdocs_try1/cdoc2-system-usecasemodel/docs
~/tmp/repos/CDOC2/md-upload-to-confluence/mark -u <RIA_Confluence_username> -p <password> -b https://confluence.ria.ee/ -f ch02_business_cases.md
git clone git@gitlab.cyber.ee:id/utilities/md-upload-to-confluence.git
cd md-upload-to-confluence
make build
```

```bash
export_Confluence.sh
```