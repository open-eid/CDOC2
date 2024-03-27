# Intro

This is documentation for CDOC2 system, including analysis, protocol and format specification and architecture documentation.

# Organisation of source files

Please follow these conventions:

* Approximately one chapter per one `.md` file. If needed, split larger files at section level. All files with `.md` extension will be automatically included. Also see [mkdocs user guide](https://www.mkdocs.org/user-guide/writing-your-docs/)).
* Use numbers in beginning of filenames for sorting `.md` files.
* Divide material under analysis/spec/architecture topics (subfolders `docs/01_use_case_model`, `docs/02_protocol_and_cryptography_spec`, `docs/03_system_architecture`). When needed, create additional topics.
* Put common acronyms and terms into `docs/includes/abbreviations.md`
* Put image files into the `docs/img` folder, so that they could be re-used from multiple `.md` files and refer to them with paths like `../img/SID_MID_full.png`
* Follow [Python-Markdown](https://python-markdown.github.io/#features) conventions and [MkDocs Material features](https://squidfunk.github.io/mkdocs-material/reference/)

# Linting

```bash
markdownlint-cli2 "cdoc2-system-docs/**/*.md"
```

# Generation toolchain

1. Visual Studio Code (<https://code.visualstudio.com>)
2. Python with [`pip` package manager](<https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line>)
3. Install smaller Python packages and other requirements:

```bash
pip3 install -r ../mkdocs_requirements.txt
```

4. Test the `mkdocs` utility

```bash
mkdocs --version
```

# Development process

1. Create RM ticket, if not already there, and corresponding GIT branch from master
2. Switch to new GIT branch in your working directory
3. Edit source code files with VSCode in `docs/` folder, resolve linter errors, check with VSCode "Markdown: Open Preview" command
4. Run `mkdocs serve` and check the local website <http://127.0.0.1:8000> within your browser
5. Commit and push to the branch
6. When the ticket is completed or feedback is needed, create GitLab MR (Merge Request)
7. After feedback and fixing problems, finish MR and merge changes to master branch
8. Check the published website <https://cdoc2.pages.ext.cyber.ee/cdoc2-documentation/>
