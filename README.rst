.. highlight:: console

===============================
Cookiecutter Go Template
===============================

.. image:: https://github.com/romnn/cookiecutter-go/workflows/test/badge.svg
    :target: https://github.com/romnn/cookiecutter-go/actions 
    :alt: Build status

Opinionated ``cookiecutter`` template for golang projects.

The key features of this template include:

* Support for ``golang`` 1.11+ modules
* Pre-commit hooks via `pre-commit <https://pre-commit.com/>`_ including:

  * `gofmt <https://golang.org/cmd/gofmt/>`_ to automatically format source files
  * `govet <https://golang.org/cmd/vet/>`_ to statically lint source files
  * `golint <https://godoc.org/golang.org/x/lint/golint>`_ to lint source files
  * `goimports <https://godoc.org/golang.org/x/tools/cmd/goimports>`_ to check imports
  * `gocyclo <https://github.com/fzipp/gocyclo>`_ to check for too complex functions
  * ``go build`` to check successful builds

* Automatic testing and deployment of binaries to GitHub releases via `travis-ci.com <https://travis-ci.com>`_
* Pre configured repository including sample tests, a nice README and contribution guide and more
* Measuring test coverage for `codecov.io <https://codecov.io/>`_
* `bump2version <https://github.com/c4urself/bump2version>`_ for version management
* Dockerfile for deploying binaries as containers


Quickstart
----------

Prerequisites
^^^^^^^^^^^^^^^

Before you get started, make sure you have installed the following tools::

    $ python3 -m pip install -U cookiecutter>=1.4.0
    $ python3 -m pip install pre-commit bump2version invoke ruamel.yaml halo
    $ go get -u golang.org/x/tools/cmd/goimports
    $ go get -u golang.org/x/lint/golint
    $ go get -u github.com/fzipp/gocyclo/cmd/gocyclo
    $ go get -u github.com/mitchellh/gox  # if you want to test building on different architectures

**Remember**: To be able to excecute the tools downloaded with ``go get``, 
make sure to include ``$GOPATH/bin`` in your ``$PATH``.
If ``echo $GOPATH`` does not give you a path make sure to set it
(``export GOPATH="$HOME/go"`` for example). On order for your changes to persist, 
do not forget to add these to your shells ``.bashrc``.

Create a new go project
^^^^^^^^^^^^^^^^^^^^^^^^^

Navigate to wherever you want your project to be created, and run cookiecutter (you will be asked for the project name etc)::

    $ cookiecutter https://github.com/romnn/cookiecutter-go.git

After your project was created:

* Create a remote repository and publish your project::

    $ cd <mypackage>
    $ git remote add origin git@github.com:myusername/mypackage.git
    $ git add .
    $ pre-commit run --all-files
    $ git add .
    $ git commit -m "Initial commit"
    $ git push --set-upstream origin master

* Add the repo to your `Travis-CI`_ account. If you have connected travis with GitHub this is done automatically.
* If you choose *tool* or *both* for your project and want to publish pre built release binaries,
  `install the Travis CLI`_ and run::

    $ travis login                  # Login with your GitHub credentials
    $ travis setup releases         # When using travis.org
    $ travis setup releases --com   # When using travis.com

  to automatically encrypt a GitHub OAuth token into your ``.travis.yml`` config.

  Unfortunately, the travis cli tool appends the token at the config's top level,
  so you need to manually edit the ``.travis.yml`` config or run::

    $ invoke fix-token

  Now you can push the updated ``.travis.yml`` to your remote repository::

    $ git add .travis.yml
    $ git commit -m "Add GitHub releases token"
    $ git push

  If you do not want to publish pre-built releases,
  remove the *Publish release* stage in ``.travis.yml``.

* If you want to publish the tool as a ``docker`` container, connect `hub.docker.com <https://https://hub.docker.com/>`_ with
  your GitHub account and `create a new repository <https://hub.docker.com/repository/create>`_.
  
  Make sure to choose a matching name and connect your GitHub repository at the bottom of the page.
  You must also specify the location of the ``Dockerfile`` (choose the default ``/``).
  When you are done click *Create and build*.

* Start coding!::

  $ go build <your-package>
  $ invoke run -- --name Roman  # If you chose "tool" or "both"
  $ pre-commit run --all-files

* Release new versions of your package by pushing a new tag to master::

    $ bump2version (major | minor | patch)
    $ git push --follow-tags

.. _Travis-CI: https://travis-ci.com
.. _Install the Travis CLI: https://github.com/travis-ci/travis.rb#installation

Documentation
-------------

If you need more guidance I encourage you to have a look at the `more extensive documentation`_.

.. _`more extensive documentation`: https://cookiecutter-go.readthedocs.io/en/latest/
