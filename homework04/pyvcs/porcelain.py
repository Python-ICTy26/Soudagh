import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    index = read_index(gitdir)
    return commit_tree(
        gitdir=gitdir, tree=write_tree(gitdir, index), message=message, author=author
    )


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    head = gitdir / "refs" / "heads" / obj_name

    if head.exists():
        with head.open(mode="r") as f:
            obj_name = f.read()

    index = read_index(gitdir)

    for file in index:
        if pathlib.Path(file.name).is_file():
            if "/" in file.name:
                shutil.rmtree(file.name[: file.name.find("/")])
            else:
                os.chmod(file.name, 0o777)
                os.remove(file.name)

    obj_path = gitdir / "objects" / obj_name[:2] / obj_name[2:]

    with obj_path.open(mode="rb") as f1:
        commit_content = f1.read()

    sha = commit_parse(commit_content).decode()

    for file in find_tree_files(sha, gitdir):
        if "/" in file[0]:
            dir_name = file[0][: file[0].find("/")]
            pathlib.Path(dir_name).absolute().mkdir()

        with open(file[0], "w") as f2:
            header, content = read_object(file[1], gitdir)
            f2.write(content.decode())
