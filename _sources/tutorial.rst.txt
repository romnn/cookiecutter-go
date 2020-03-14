Tutorial
========

.. note:: Do you find any of these instructions confusing? `Edit this file`_
          and submit a pull request with your improvements!

.. _`Edit this file`: https://github.com/romnnn/cookiecutter-go/blob/master/docs/tutorial.rst

To start with, you will need a `GitHub account`_. Create this before you get started with this tutorial.
If you are new to Git and GitHub, you should probably spend a few minutes on some of the tutorials at the top of the page at `GitHub Help`_.

.. _`GitHub account`: https://github.com/
.. _`GitHub Help`: https://help.github.com/


|:cookie:| Step 1: Install Cookiecutter
---------------------------------------

Install ``cookiecutter>=1.4.0``:

.. code-block:: console

    $ python3 -m pip install -U cookiecutter>=1.4.0

We'll also need ``pre-commit`` and ``bump2version`` for initializing the new project:

.. code-block:: console

    $ python3 -m pip install pre-commit bump2version

As part of the ``pre-commit`` hooks, go tools are run. Those must also be installed:

.. code-block:: console

    $ go get -u golang.org/x/tools/cmd/goimports
    $ go get -u golang.org/x/lint/golint
    $ go get -u github.com/fzipp/gocyclo
    $ go get -u github.com/mitchellh/gox  # if you want to test building on different architectures and platforms

.. warning::    To be able to excecute the tools downloaded with ``go get``, 
                make sure to include ``$GOPATH/bin`` in your ``$PATH``.
                If ``echo $GOPATH`` does not give you a path make sure to set it
                (``export GOPATH="$HOME/go`` for example). On order for your changes to persist, 
                do not forget to add these to your shells ``.bashrc``.

|:package:| Step 2: Generate Your Go Project
-----------------------------------------

Now it's time to generate your golang project.

Use cookiecutter, pointing it at the cookiecutter-go repo:

.. code-block:: console

    $ cookiecutter https://github.com/romnnn/cookiecutter-go.git

You'll be asked to enter a bunch of values to set the package up.
If you don't know what to enter, stick with the defaults.


|:octopus:| Step 3: Create a GitHub Repo
----------------------------------------

Go to your GitHub account and create a new repo named ``mypackage``, where ``mypackage`` matches the ``[project_slug]`` from your answers to running cookiecutter.
This is so that Travis CI can find it when we get to Step 5.

You will find one folder named after the ``[project_slug]``.
Move into this folder, and then setup git to use your GitHub repo and upload the code:

.. code-block:: console

    $ cd mypackage
    $ git init .
    $ git add .
    $ git commit -m "Initial commit."
    $ git remote add origin git@github.com:myusername/mypackage.git
    $ git push -u origin master

Where ``myusername`` and ``mypackage`` are adjusted for your username and package name.

You can use HTTPS to push the repository, but it's more convenient to use a ssh key to push the repo.
You can `Generate`_ a key or `Add`_ an existing one.

.. _`Generate`: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
.. _`Add`: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/

|:hammer_and_wrench:| Step 4: First build
--------------------------------------------------------------

You should still be in the folder containing the ``go.mod`` file.

Go ahead and give building the initial project a go (no pun intended)::

.. code-block:: console

    $ go build <your-package>

You can also test the entire project by running the pre commit hooks, which should have been installed
into your git repository::

  $ pre-commit run --all-files

Next to building, this will also format and lint your code amongst other things.

|:construction_worker:| Step 6: Set up TravisCI
-----------------------------------------------

`Travis-CI`_ [*]_ is a continuous integration tool used to prevent integration problems.
Every commit to the master branch will trigger automated builds of the application.

Add the repository to your Travis-CI account by activating it.
If you have connected travis with GitHub this is done automatically.
If you have not yet installed the Travis CLI (Command line interface), follow `the installation guide`_.

With the Travis CLI, setup automatic upload of binaries to the GitHub releases like so:

.. code-block:: console

    $ travis login
    $ travis setup releases         # When using travis.org
    $ travis setup releases --com   # When using travis.com

.. note:: Both commands will ask you for your GitHub credentials.
          If you are worried, skip ``travis login``, create a GitHub token manually
          and use ``travis encrypt``...

After running ``setup releases``, your ``.travis.yml`` config will:

* Include the encrypted GitHub oauth token
* Be able to automatically deploy binaries to releases when you push a new tag to the master branch.

Because the token is appended outside of any build stage,
you still need to manually edit the ``.travis.yml`` config or run:

.. code-block:: console

    $ invoke fix-token

.. [*] For private projects go to `travis-ci.com`_, for public ones go to `travis-ci.org`_ has been a thing.
       But afaik all projects should use `travis-ci.com`_ as of now.

.. _`Travis-CI`: https://travis-ci.com/
.. _`travis-ci.org`: https://travis-ci.org/
.. _`travis-ci.com`: https://travis-ci.com/
.. _the installation guide: https://github.com/travis-ci/travis.rb#installation

|:tada:| Step 7: Start coding!
-------------------------------

Hopefully this tutorial was helpful to you!
