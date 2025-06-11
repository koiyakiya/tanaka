import nox
from functools import wraps


def with_dev_dependencies(func):
    """Decorator to install development dependencies before running a session."""

    @wraps(func)
    def wrapper(session: nox.Session, *args, **kwargs):
        pyproject = nox.project.load_toml()  # default is pyproject.toml
        session.install(*nox.project.dependency_groups(pyproject, 'dev'))
        return func(session, *args, **kwargs)

    return wrapper


@nox.session(reuse_venv=True, venv_backend='uv|virtualenv')
@with_dev_dependencies
def linting(session: nox.Session) -> None:
    """Run the ruff linter."""
    session.run('ruff', 'check')


@nox.session(reuse_venv=True, venv_backend='uv|virtualenv')
@with_dev_dependencies
def formatting(session: nox.Session) -> None:
    """Run the ruff formatter."""
    session.run('ruff', 'format')
