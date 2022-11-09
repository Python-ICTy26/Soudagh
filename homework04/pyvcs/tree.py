import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    notes = b""
    for file in index:
        if "/" in file.name:
            notes += b"40000 "
            subdir_files = b""
            dir_name = file.name[: file.name.find("/")]
            notes += dir_name.encode() + b"\0"
            subdir_files += oct(file.mode)[2:].encode() + b" "
            subdir_files += file.name[file.name.find("/") + 1 :].encode() + b"\0"
            subdir_files += file.sha1
            sha = hash_object(subdir_files, fmt="tree", write=True)
            notes += bytes.fromhex(sha)
        else:
            notes += oct(file.mode)[2:].encode() + b" "
            notes += file.name.encode() + b"\0"
            notes += file.sha1
    return hash_object(notes, fmt="tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if "GIT_DIR" not in os.environ:
        os.environ["GIT_DIR"] = ".git"
    if not author:
        author = f"{os.environ['GIT_AUTHOR_NAME']} <{os.environ['GIT_AUTHOR_EMAIL']}>"
    timestamp = int(time.mktime(time.localtime()))
    utc_offset = -time.timezone
    author_time = "{} {}{:02}{:02}".format(
        timestamp,
        "+" if utc_offset > 0 else "-",
        abs(utc_offset) // 3600,
        (abs(utc_offset) // 60) % 60,
    )
    content = f"tree {tree}\n"
    if parent:
        content += f"parent {parent}\n"
    content += f"author {author} {author_time}\ncommitter {author} {author_time}\n\n{message}\n"
    sha = hash_object(content.encode("ascii"), "commit", True)
    return sha
