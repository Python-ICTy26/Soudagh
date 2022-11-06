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
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    hash = hashlib.sha1(store).hexdigest()

    if write:
        gitdir = repo_find(".")
        obj_path = gitdir / "objects"

        if not pathlib.Path.exists(obj_path / hash[:2]):
            (obj_path / hash[:2]).mkdir()

        if not pathlib.Path.exists(obj_path / hash[:2] / hash[2:]):
            (obj_path / f"{hash[:2]}/{hash[2:]}").write_bytes(zlib.compress(store))
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
    result = []
    while len(data) != 0:
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        result.append((mode, name, sha))
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(pathlib.Path("."))

    for obj in resolve_object(obj_name, gitdir):
        header, content = read_object(obj, gitdir)
        if header == "tree":
            result = ""
            tree_files = read_tree(content)
            for f in tree_files:
                result += str(f[0]).zfill(6) + " "
                result += read_object(f[2], repo_find())[0] + " "
                result += f[2] + "\t"
                result += f[1] + "\n"
            print(result)
        else:
            print(content.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            tree = find_tree_files(f[2], gitdir)
            for blob in tree:
                name = f[1] + "/" + blob[0]
            result.append((name, blob[1]))
        else:
            result.append((f[1], f[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    return data[data.find(b"tree") + 5 : data.find(b"tree") + 45]
