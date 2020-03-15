#!/usr/bin/env python
import os
import time
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


class _Halo:
    def __init__(self, *args, **kwargs):
        self.text = kwargs.get("text", "")

    def __enter__(self):
        print(self.text)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _print(text):
        print(text)

    fail = succeed = _print


try:
    from halo import Halo
except (ImportError, ModuleNotFoundError):
    Halo = _Halo


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def run_command(*cmd_args, **cmd_kwargs):
    try:
        return subprocess.check_output(*cmd_args, **cmd_kwargs).decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output.decode("utf-8"))
        raise


def install_git_hooks():
    with Halo(text="Installing git hooks", spinner="dots", color="cyan") as spinner:
        try:
            run_command(
                "pre-commit install", stderr=subprocess.STDOUT, shell=True
            )
            time.sleep(0.5)
        except Exception:
            spinner.fail("Failed to install git hooks")
            raise
        spinner.succeed("Successfully installed git hooks")


def initialize_git():
    with Halo(text="Initializing git repository", spinner="dots", color="red") as spinner:
        try:
            run_command(
                "cd {} && git init".format(PROJECT_DIRECTORY),
                stderr=subprocess.STDOUT,
                shell=True,
            )
            time.sleep(0.5)
        except Exception:
            spinner.fail("Failed to initialize git repository")
            raise
        spinner.succeed("Successfully initialized git repository")


def go_mod_init():
    """Creates a go mod init file"""
    with Halo(text="Initializing go module", spinner="dots", color="blue") as spinner:
        module_name = '{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}'
        try:
            run_command(
                "cd {} && go mod init {}".format(
                    PROJECT_DIRECTORY, module_name),
                stderr=subprocess.STDOUT,
                shell=True,
            )
            time.sleep(0.5)
        except Exception:
            spinner.fail("Failed to initialize go module")
            raise
        spinner.succeed("Successfully initialized go module")


if __name__ == "__main__":
    initialize_git()
    install_git_hooks()
    go_mod_init()

    # Remove unnecessary files
    if '{{ cookiecutter.project_type }}' == 'module':
        remove('Dockerfile')
        remove('.dockerignore')
    if '{{ cookiecutter.project_type }}' != 'both':
        remove('cmd/')
