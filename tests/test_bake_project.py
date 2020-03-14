import datetime
import importlib.util
import json
import os
import shlex
import subprocess
from contextlib import contextmanager

from ruamel.yaml import YAML
from click.testing import CliRunner
from cookiecutter.utils import rmtree


yaml = YAML()
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "../cookiecutter.json")) as cookiecutter_config_file:
    default_package_name = (
        json.load(cookiecutter_config_file)
        .get("project_name", "Python Package Template")
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(str(dirpath))
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        try:
            return subprocess.check_call(shlex.split(command))
        except subprocess.CalledProcessError as e:
            return e.returncode


def check_output_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the command output"""
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert default_package_name in found_toplevel_files
        assert "tox.ini" in found_toplevel_files
        assert "tests" in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert run_inside_dir("invoke test", result.project) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(
        cookies, extra_context={"full_name": 'name "quote" name'}
    ) as result:
        assert result.project.isdir()
        assert run_inside_dir("invoke test", result.project) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project.isdir()
        assert run_inside_dir("invoke test", result.project) == 0


# def test_bake_and_run_travis_pypi_setup(cookies):
#     # given:
#     with bake_in_temp_dir(cookies) as result:
#         project_path = str(result.project)
#
#         # when:
#         travis_setup_cmd = ('python travis_pypi_setup.py'
#                             ' --repo audreyr/cookiecutter-go --password invalidpass')
#         run_inside_dir(travis_setup_cmd, project_path)
#         # then:
#         with open(result.project.join(".travis.yml"), "r") as file:
#           result_travis_config = yaml.load(file)
#         min_size_of_encrypted_password = 50
#         assert len(result_travis_config["deploy"]["password"]["secure"]) > min_size_of_encrypted_password


def test_bake_without_travis_pypi_setup(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_pypi_deployment_with_travis": "n"}
    ) as result:
        with open(result.project.join(".travis.yml"), "r") as file:
            result_travis_config = yaml.load(file)
        assert "deploy" not in result_travis_config
        assert "python" == result_travis_config["language"]
        found_toplevel_files = [f.basename for f in result.project.listdir()]


def test_mit_license(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert "MIT" in result.project.join("LICENSE").read()
        assert "MIT" in result.project.join("setup.py").read()


def test_using_pytest(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        # Test Pipfile installs pytest
        pipfile_file_path = result.project.join("Pipfile")
        lines = pipfile_file_path.readlines()
        assert 'pytest = "*"\n' in lines
        # Test contents of test file
        test_file_path = result.project.join(
            "tests/test_{}.py".format(default_package_name)
        )
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        assert run_inside_dir("invoke test", result.project) == 0


def test_using_google_docstrings(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        # Test docs include sphinx extension
        docs_conf_file_path = result.project.join("docs/conf.py")
        lines = docs_conf_file_path.readlines()
        assert "sphinx.ext.napoleon" in "".join(lines)


def test_not_using_google_docstrings(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_google_docstrings": "n"}
    ) as result:
        assert result.project.isdir()
        # Test docs do not include sphinx extension
        docs_conf_file_path = result.project.join("docs/conf.py")
        lines = docs_conf_file_path.readlines()
        assert "sphinxcontrib.napoleon" not in "".join(lines)


def test_bake_with_console_script_files(cookies):
    context = {"command_line_interface": "click"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files

    setup_path = os.path.join(project_path, "setup.py")
    with open(setup_path, "r") as setup_file:
        assert "entry_points" in setup_file.read()


def test_bake_with_console_script_cli(cookies):
    result = cookies.bake()
    project_path, project_slug, project_dir = project_info(result)

    module_path = os.path.join(project_dir, "cli.py")
    module_name = ".".join([project_slug, "cli"])

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)

    runner = CliRunner()
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = " ".join(
        ["Replace this message by putting your code into", project_slug]
    )
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output
