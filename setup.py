# !/usr/bin/env python

from setuptools import setup

version = "0.0.1"

test_requirements = [
    "tox",
    "pytest",
    "pytest-cov",
    "pytest-cookies",
    "pytest-xdist",
    "pytest-sugar",
    "ruamel.yaml"
]
coverage_requirements = ["coverage", "codecov"]
docs_requirements = ["sphinx>=2.0", "romnnn_sphinx_press_theme", "sphinxemoji"]
dev_requirements = ["invoke", "pre-commit", "cookiecutter"]

setup(
    name="romnnn-cookiecutter-go",
    packages=[],
    python_requires=">=3.6",
    version=version,
    description="Cookiecutter template for a go project",
    author="romnnn",
    license="MIT",
    author_email="contact@romnn.com",
    url="https://github.com/romnnn/cookiecutter-go",
    keywords=["cookiecutter", "template", "package", "golang"],
    extras_require=dict(
        dev=dev_requirements
        + docs_requirements
        + test_requirements
        + coverage_requirements,
        docs=docs_requirements,
        test=test_requirements + coverage_requirements,
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
    ],
)
