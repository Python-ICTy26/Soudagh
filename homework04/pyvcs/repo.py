import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    try:
        gitdir = os.environ["GIT_DIR"] if os.environ["GIT_DIR"] else ".git"
    except:
        gitdir = ".git"

    resdir = ""
    workdir = pathlib.Path(workdir)

    if len(workdir.parents) == 0:
        if not pathlib.Path.exists(workdir / gitdir):
            raise Exception("Not a git repository")
        return workdir.absolute() / gitdir
    elif pathlib.Path.exists(workdir / gitdir):
        return workdir.absolute() / gitdir
    else:
        for path in workdir.parents:
            if gitdir in str(path) or pathlib.Path.exists(path / gitdir):
                resdir = path
    if not resdir:
        raise Exception("Not a git repository")
    if gitdir in str(resdir):
        return resdir
    else:
        return resdir / gitdir


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    try:
        if workdir.is_file():
            raise Exception(f"{workdir} is not a directory")
    except AttributeError:
        workdir = pathlib.Path(workdir)

    try:
        gitdir = os.environ["GIT_DIR"] if os.environ["GIT_DIR"] else ".git"
    except:
        gitdir = ".git"

    dir = workdir / gitdir
    dir.mkdir()

    (dir / "refs").mkdir()
    (dir / "refs/heads").mkdir()
    (dir / "refs/tags").mkdir()
    (dir / "objects").mkdir()

    (dir / "HEAD").write_text("ref: refs/heads/master\n")
    (dir / "config").write_text(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = "
        "false\n\tlogallrefupdates = "
        "false\n"
    )

    (dir / "description").write_text("Unnamed pyvcs repository.\n")

    return dir
