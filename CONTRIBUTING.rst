.. highlight:: console

============
Contributing
============

Contributions are welcome and greatly appreciated!
Contributions will always be credited.

How can I contribute?
---------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/romnn/cookiecutter-go/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the `GitHub issues`_ for bugs. Anything tagged with *"bug"* and *"help
wanted"* is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the `GitHub issues`_ for features. Anything tagged with *"enhancement"*
and *"help wanted"* is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

``cookiecutter-go`` could always use more documentation, whether as part of the
official ``cookiecutter-go`` docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to `file an issue <https://github.com/romnn/cookiecutter-go/issues>`_ on GitHub.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven open source project, so contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up ``cookiecutter-go`` for local development.

1. Fork the `cookiecutter-go repo <https://github.com/romnn/cookiecutter-go>`_ on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/cookiecutter-go.git

3. Install development dependencies into a virtual development environment (assuming you have ``pipenv`` installed)::

    $ cd cookiecutter-go/
    $ pipenv install --dev

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you are ready to make changes. Remember to add tests to ``tests/`` and make sure all existing tests pass::

    $ pytest                                    # Run all tests
    $ pytest tests/one_specific_test_file.py    # Run one specific test
    $ tox                                       # Run the tests for different python versions

6. If you are done, commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website so your changes can
   be merged into the master.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the documentation (``docs/``)  should be updated. Put
   your new functionality into a function with a docstring and add the
   feature to the list in ``README.rst``.
3. The pull request should work for python 3.6+ and the latest version of golang. Check the
   `build status of your pull request <https://travis-ci.org/romnn/cookiecutter-go/pull_requests>`_
   and make sure that all tests pass for all supported python versions.

Add a New Test
---------------
When fixing a bug or adding features, it's good practice to add a test to demonstrate your fix or new feature behaves as expected. These tests should focus on one tiny bit of functionality and prove changes are correct.

To write and run your new test, follow these steps:

1. Add the new test to `tests/test_bake_project.py`. Focus your test on the specific bug or a small part of the new feature.

2. If you have already made changes to the code, stash your changes and confirm all your changes were stashed::

    $ git stash
    $ git stash list

3. Run your test and confirm that your test fails. If your test does not fail, rewrite the test until it fails on the original code::

    $ py.test ./tests

4. (Optional) Run the tests with tox to ensure that the code changes work with different Python versions::

    $ tox

5. Proceed work on your bug fix or new feature or restore your changes. To restore your stashed changes and confirm their restoration::

    $ git stash pop
    $ git stash list

6. Rerun your test and confirm that your test passes. If it passes, congratulations!

Publishing (Maintainers only)
-----------------------------

After merging the changes, tag your commits with a new version and push to GitHub::

$ bump2version (major | minor | patch)
$ git push --follow-tags

.. _GitHub issues: https://github.com/romnn/cookiecutter-go/issues
