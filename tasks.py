"""Development tasks for the cookiecutter template project"""

import webbrowser
import platform
from invoke import task
from pathlib import Path
Path().expanduser()

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath('docs')
DOCS_BUILD_DIR = DOCS_DIR.joinpath('build')
DOCS_INDEX = DOCS_BUILD_DIR.joinpath('index.html')
TEST_DIR = ROOT_DIR.joinpath('tests')


@task
def test(c):
    """
    Run tests
    """
    pty = platform.system() == 'Linux'
    c.run("pipenv run pytest --cov={}".format(ROOT_DIR), pty=pty)


@task(help={'output': "Generated documentation output format (default is html)"})
def docs(c, output="html"):
    """Generate documentation
    """
    c.run("pipenv run sphinx-apidoc -o {} .".format(DOCS_DIR))
    c.run("pipenv run sphinx-build -b {} {} {}".format(output.lower(), DOCS_DIR, DOCS_BUILD_DIR))
    if output.lower() == "html":
        webbrowser.open(DOCS_INDEX.as_uri())
    elif output.lower() == "latex":
        c.run("cd {} && make".format(DOCS_BUILD_DIR))


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    c.run("rm -fr {}".format(DOCS_BUILD_DIR))
