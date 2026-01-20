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

It is possible to build the documentation using Python utilities `mike` and `mkdocs`. `mike` is used for creating persistent versions of the documentation which will not be changed once the documentation has changed. Those versions are created under a special `gh-pages` branch.

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

5. Test the `mike` utility

    ```bash
    mike --version
    ```

6. Build a version of the documentation using `mike`, where `1.1` is an arbitrary version. Any other version name can be used. Then use `mike serve` to serve all built versions of the documentation under different URL-s.

    ```bash
    cd cdoc2-system-docs
    mike deploy 1.1
    mike serve
    ```

    If a default version number is not configured, then the documentation will be served at <http://localhost:8000/v1/> , where `v1` is the name of the version that was used with the `deploy` command.

7. Alternatively `mkdocs` can be used directly to build the documentation under the same git branch into the `/site` folder and served from there.

    ```bash
    cd cdoc2-system-docs
    mkdocs build
    mike serve
    ```

    The documentation should be served at <http://127.0.0.1:8000/>

# Development process

1. Create RM ticket, if not already there, and corresponding GIT branch from master
2. Switch to new GIT branch in your working directory
3. Edit source code files with VSCode in `docs/` folder, resolve linter errors, check with VSCode "Markdown: Open Preview" command
4. Run `mkdocs serve` and check the local website <http://127.0.0.1:8000> within your browser
5. Commit and push to the branch
6. When the ticket is completed or feedback is needed, create GitLab MR (Merge Request)
7. After feedback and fixing problems, finish MR and merge changes to master branch
8. Check the published website <https://cdoc2.pages.ext.cyber.ee/cdoc2-documentation/>

# Publish to GitHub Pages (<open-eid.github.io/CDOC2>)

1. Add open-eid remote (if not done already)

    ```shell
    git remote add github.com/open-eid git@github.com:open-eid/CDOC2.git
    git remote -v   
    ```

2. [Add your SSH public](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) key to your GitHub account  (if not done already)
3. Publish to GitHub Pages

    ```shell
    mike deploy -F cdoc2-system-docs/mkdocs.yml --remote github.com/open-eid --deploy-prefix docs --branch gh-pages --push 1.1
    mike set-default -F cdoc2-system-docs/mkdocs.yml --remote github.com/open-eid --deploy-prefix docs --branch gh-pages --push 1.1
    ```

    , where `1.1` is an arbitrary version

Updated site is available at <http://open-eid.github.io/CDOC2>

`mike` tool will generate mkdocs HTML site using `mkdocs` tool under directory `docs` and push it to `gh-pages` branch.

Generated site files can be viewed <https://github.com/open-eid/CDOC2/tree/gh-pages> or by running
   `git checkout gh-pages`

CDOC2 Pages [configuration](<https://github.com/open-eid/CDOC2/settings/pages>) is configured to serve generated documentation from `gh-pages` branch and `docs` directory.
More info from [GitHub Pages](<https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-from-a-branch>)

# Publish to Gitlab Pages (<https://cdoc2.pages.ext.cyber.ee/cdoc2-documentation>)

Gitlab-CI handles publishing Gitlab Pages

Default version is managed by CI/CD variable `DOC_DEFAULT_VERSION`. To change the default version please change `DOC_DEFAULT_VERSION` variable before publishing a new tag.
