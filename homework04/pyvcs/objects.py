import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    content = data.decode()
    header = f"{fmt} {len(content)}\0"
    store = header + content
    hash = hashlib.sha1(store.encode()).hexdigest()

    if write:
        gitdir = repo_find(".")
        obj_path = gitdir / "objects"

        if not pathlib.Path.exists(obj_path / hash[:2]):
            (obj_path / hash[:2]).mkdir()

        if not pathlib.Path.exists(obj_path / hash[:2] / hash[2:]):
            (obj_path / f"{hash[:2]}/{hash[2:]}").write_bytes(zlib.compress(store.encode()))
    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    objs = []

    if len(obj_name) > 40 or len(obj_name) < 4:
        raise Exception(f"Not a valid object name {obj_name}")

    blob_path = gitdir / "objects" / obj_name[:2]

    for obj in blob_path.iterdir():
        objs.append(find_object(obj_name, obj))

    if not objs or objs[0] is None:
        raise Exception(f"Not a valid object name {obj_name}")

    return objs


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    if obj_name[2:] in gitdir.parts[-1]:
        return str(gitdir.parts[-2] + str(gitdir.parts[-1]))
    else:
        return None


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    blob_path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(blob_path, mode="rb") as f:
        blob_contents = zlib.decompress(f.read())

    srez = blob_contents.find(b"\x00")
    fmt = blob_contents[:srez]
    fmt = fmt[: fmt.find(b" ")]
    data = blob_contents[(srez + 1) :]

    return fmt.decode(), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(pathlib.Path("."))

    for obj in resolve_object(obj_name, gitdir):
        header, data = read_object(obj, gitdir)

    if pretty:
        print(data.decode())
    else:
        print(data)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
