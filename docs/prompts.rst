Prompts
=======

When you create your package, you are prompted to enter these values.

Templated values
----------------

The following appear in various parts of your generated project. Do not worry entering your username, full name and email address, these values are genuinely required in files
including ``AUTHORS.rst``, ``setup.py``, ``__init__.py`` and the package's documentation.

:full_name:             Your full name

:email:                 Your email address

:github_username:       Your GitHub username

:project_name:          The name of your new go package project. This is used in documentation, so spaces and any characters are fine here

:project_slug:          The namespace of your go package. This should be go import-friendly. Typically, it is the `slugified` version of ``project_name``

:public_import_path:    The import path of your package or the download path of your tool. Defaults to ``github.com/<github_username>/<project_slug>``

:version:               The starting version number of the package

:project_type:          The type of your project, which can be 	*package*, *tool* or *both*