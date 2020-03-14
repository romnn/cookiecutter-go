import os
import pprint
import shlex
import subprocess
from collections import OrderedDict
from contextlib import contextmanager

from ruamel.yaml import YAML
from cookiecutter.utils import rmtree

yaml = YAML()
dir_path = os.path.dirname(os.path.realpath(__file__))
travis_config_samples_path = os.path.join(dir_path, "sample_travis_configs")


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
            return int(subprocess.check_call(shlex.split(command)))
        except subprocess.CalledProcessError as e:
            print("Error")
            print(e.output)
            return int(e.returncode)


def sort_dict(d):
    res = OrderedDict()
    for k, v in sorted(d.items()):
        if isinstance(v, dict):
            res[k] = sort_dict(v)
        else:
            res[k] = v
    return res


class Fix:
    def __init__(self, config_file, project_dir, force=True):
        self.config_file = config_file
        self.project_dir = project_dir
        self.project_config_file = project_dir.join(".travis.yml")
        self.force = force
        self.before, self.after = self.parse_configs()

    def run_fix(self, force=None):
        if force is None:
            force = self.force
        # Replace with test .travis config
        command = "cp {} {}".format(self.config_file, self.project_config_file)
        subprocess.check_call(shlex.split(command))
        result = run_inside_dir(
            "invoke fix-token --no-verify {}".format("--force" if force else ""),
            self.project_dir,
        )
        self.before, self.after = self.parse_configs()
        print(result, type(result))
        return result

    def parse_configs(self):
        with open(self.config_file, "r") as _source_file:
            with open(self.project_config_file, "r") as _destination_file:
                before = sort_dict(yaml.load(_source_file))
                after = sort_dict(yaml.load(_destination_file))
                return before, after

    def get(self):
        return self.before, self.after

    def debug(self):
        print("##################################")
        [pprint.pprint(p) for p in self.get()]
        print("##################################")

    def was_modified(self):
        return self.before != self.after

    def get_final_token(self):
        try:
            releases_stages = [
                stage
                for stage in self.after["jobs"]["include"]
                if stage.get("deploy", dict()).get("provider") == "releases"
            ]
            return releases_stages[0]["deploy"]["token"]["secure"]
        except (TypeError, KeyError):
            return None


def _test_fix_travis___after_travis_cli_equally_modified(project_dir):
    after_travis_cli_equally_modified = Fix(
        config_file=os.path.join(
            travis_config_samples_path, "after_travis_cli.equally.modified.travis.yml"
        ),
        project_dir=project_dir,
    )
    assert after_travis_cli_equally_modified.run_fix(force=False) == 0
    assert after_travis_cli_equally_modified.was_modified()


def _test_fix_travis___after_travis_cli_modified(project_dir):
    after_travis_cli_modified = Fix(
        config_file=os.path.join(
            travis_config_samples_path, "after_travis_cli.modified.travis.yml"
        ),
        project_dir=project_dir,
    )
    assert after_travis_cli_modified.run_fix(force=False) == 1
    assert not after_travis_cli_modified.was_modified()

    assert after_travis_cli_modified.run_fix(force=True) == 0
    assert after_travis_cli_modified.was_modified()
    assert after_travis_cli_modified.get_final_token() == "NEW_GH_TOKEN"


def _test_fix_travis___after_travis_cli_multiple_deploy(project_dir):
    after_travis_cli_multiple_deploy = Fix(
        config_file=os.path.join(
            travis_config_samples_path, "after_travis_cli.multiple_deploy.travis.yml"
        ),
        project_dir=project_dir,
    )
    assert after_travis_cli_multiple_deploy.run_fix(force=False) == 1
    assert not after_travis_cli_multiple_deploy.was_modified()
    assert after_travis_cli_multiple_deploy.run_fix(force=True) == 1
    assert not after_travis_cli_multiple_deploy.was_modified()


def _test_fix_travis___after_travis_cli_no_deploy(project_dir):
    after_travis_cli_no_deploy = Fix(
        config_file=os.path.join(
            travis_config_samples_path, "after_travis_cli.no_deploy.travis.yml"
        ),
        project_dir=project_dir,
    )
    assert after_travis_cli_no_deploy.run_fix(force=False) == 1
    assert not after_travis_cli_no_deploy.was_modified()
    assert after_travis_cli_no_deploy.run_fix(force=True) == 1
    assert not after_travis_cli_no_deploy.was_modified()


def _test_fix_travis___after_travis_cli_unmodified(project_dir):
    after_travis_cli_unmodified = Fix(
        config_file=os.path.join(
            travis_config_samples_path, "after_travis_cli.unmodified.travis.yml"
        ),
        project_dir=project_dir,
    )
    assert after_travis_cli_unmodified.run_fix(force=False) == 0
    assert after_travis_cli_unmodified.was_modified()
    assert after_travis_cli_unmodified.get_final_token() == "NEW_GH_TOKEN"
    assert after_travis_cli_unmodified.run_fix(force=True) == 0
    assert after_travis_cli_unmodified.was_modified()
    assert after_travis_cli_unmodified.get_final_token() == "NEW_GH_TOKEN"


def _test_fix_travis___before_travis_cli(project_dir):
    before_travis_cli = Fix(
        config_file=os.path.join(
            travis_config_samples_path, "before_travis_cli.travis.yml"
        ),
        project_dir=project_dir,
    )
    assert before_travis_cli.run_fix(force=False) == 1
    assert not before_travis_cli.was_modified()
    assert before_travis_cli.run_fix(force=True) == 1
    assert not before_travis_cli.was_modified()


def test_fix_travis(cookies):
    with bake_in_temp_dir(cookies) as result:
        _test_fix_travis___after_travis_cli_equally_modified(project_dir=result.project)
        _test_fix_travis___after_travis_cli_modified(project_dir=result.project)
        _test_fix_travis___after_travis_cli_multiple_deploy(project_dir=result.project)
        _test_fix_travis___after_travis_cli_no_deploy(project_dir=result.project)
        _test_fix_travis___after_travis_cli_unmodified(project_dir=result.project)
        _test_fix_travis___before_travis_cli(project_dir=result.project)
