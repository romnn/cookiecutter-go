## {{ cookiecutter.project_name }}

[![Build Status](https://travis-ci.{{ cookiecutter.travis_plan }}/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg?branch=master)](https://travis-ci.{{ cookiecutter.travis_plan }}/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
![GitHub](https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
{% if cookiecutter.project_type != 'tool' -%}
[![GoDoc](https://godoc.org/{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}?status.svg)](https://godoc.org/{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}){% endif %}
{% if cookiecutter.project_type != 'module' -%}
[![Docker Pulls](https://img.shields.io/docker/pulls/{{ cookiecutter.docker_hub_username }}/{{ cookiecutter.project_slug }})](https://hub.docker.com/r/{{ cookiecutter.docker_hub_username }}/{{ cookiecutter.project_slug }}){% endif %}
[![Test Coverage](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/master/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})

Your description goes here...

{% if cookiecutter.project_type != 'module' -%}
{% if cookiecutter.project_type == 'both' -%}
```bash
go get {{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}/cmd/{{ cookiecutter.project_slug }}
```
{% elif cookiecutter.project_type == 'tool' %}
```bash
go get {{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}
```
{% endif %}

You can also download pre built binaries from the [releases page](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/releases).

For a list of options, run with `--help`.
{% endif %}

{% if cookiecutter.project_type != 'tool' -%}
#### Usage as a library

```golang
import "{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}"
```

For more examples, see `examples/`.
{% endif %}

#### Development

######  Prerequisites

Before you get started, make sure you have installed the following tools::

    $ python3 -m pip install -U cookiecutter>=1.4.0
    $ python3 -m pip install pre-commit bump2version invoke ruamel.yaml halo
    $ go get -u golang.org/x/tools/cmd/goimports
    $ go get -u golang.org/x/lint/golint
    $ go get -u github.com/fzipp/gocyclo
    $ go get -u github.com/mitchellh/gox  # if you want to test building on different architectures

**Remember**: To be able to excecute the tools downloaded with `go get`, 
make sure to include `$GOPATH/bin` in your `$PATH`.
If `echo $GOPATH` does not give you a path make sure to run
(`export GOPATH="$HOME/go` to set it). In order for your changes to persist, 
do not forget to add these to your shells `.bashrc`.

With the tools in place, it is strongly advised to install the git commit hooks to make sure checks are passing in CI:
```bash
invoke install-hooks
```

You can check if all checks pass at any time:
```bash
invoke pre-commit
```

Note for Maintainers: After merging changes, tag your commits with a new version and push to GitHub to create a release:
```bash
bump2version (major | minor | patch)
git push --follow-tags
```

#### Note

This project is still in the alpha stage and should not be considered production ready.
