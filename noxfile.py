"""Nox sessions."""

import sys
from textwrap import dedent

import nox

try:
    from nox_poetry import Session, session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


package = "restlogger"
python_versions = ["3.10"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    "lint",
    "mypy",
)


@session(name="lint", python=python_versions)
def lint(session: Session) -> None:
    """Check cod style with black, flake8, isort"""
    args = session.posargs or ["."]
    session.install(
        "black",
        "ruff",
    )
    session.run("black", "--check", *args)
    session.run("ruff", "check", *args)


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = ["--ignore-missing-imports"]
    session.install("mypy")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")
