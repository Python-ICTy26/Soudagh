import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    ...


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    try:
        os.chdir(workdir)
        gitdir = workdir / ".git"

        os.mkdir(gitdir)

        os.mkdir("objects")
        os.makedirs(gitdir / "refs" / "heads")
        os.mkdir(gitdir / "refs" / "tags")
        os.chdir(gitdir)

        head = open("HEAD", "w")
        head.write("ref: refs/heads/master\n")
        head.close()

        config = open("config", "a")
        config.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = "
            "true\n\tbare = false\n\tlogallrefupdates = "
            "false\n"
        )
        config.close()

        description = open("description", "a")
        description.write("Unnamed pyvcs repository")
        description.close()

    except NotADirectoryError:
        raise Exception(f"{workdir} is not a directory")
    return gitdir
