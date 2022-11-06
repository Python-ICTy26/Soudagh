import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        values = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )

        return struct.pack(f">10i20sh{len(self.name)}s3x", *values)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        fmt = f">10i20sh{len(data) - 62}s"
        unpacked = struct.unpack(fmt, data)
        unpacked_list = list(unpacked)
        unpacked_list[-1] = unpacked_list[-1][:-3].decode()

        return GitIndexEntry(*unpacked_list)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index: tp.List[GitIndexEntry] = []
    path_index = gitdir / "index"

    try:
        with open(path_index, "rb") as f:
            data = f.read()
    except:
        return index

    count = int.from_bytes(data[8:12], "big")
    pointer = b"\x00\x00\x00"
    content = data[12:-20]
    counter = 0
    for i in range(count):
        name_len_start = counter + 62
        name_len_end = content[name_len_start:].find(pointer) + name_len_start + 3
        index.append(GitIndexEntry.unpack(content[counter:name_len_end]))
        counter = name_len_end
    return index


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    index_path = gitdir / "index"
    with open(index_path, "wb") as f:
        values = (b"DIRC", 2, len(entries))
        info = struct.pack(">4s2i", *values)
        hash = info
        f.write(info)
        for file in entries:
            f.write(file.pack())
            hash += file.pack()
        new_hash = str(hashlib.sha1(hash).hexdigest())
        f.write(struct.pack(f">{len(bytearray.fromhex(new_hash))}s", bytearray.fromhex(new_hash)))


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    files = read_index(gitdir)
    for file in files:
        if not details:
            print(file.name)
        else:
            print(f"{str(oct(file.mode))[2:]} {file.sha1.hex()} 0	{file.name}")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    files = []
    for file in paths:
        try:
            f = file.open()
            f_content = f.read()
        except:
            raise Exception("Wrong path")

        sha1 = hash_object(f_content.encode(), "blob", True)
        stat = os.stat(file)
        files.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(sha1),
                flags=7,
                name=str(file).replace("\\", "/"),
            )
        )
    files = sorted(files, key=lambda x: x.name)
    if not (gitdir / "index").exists():
        write_index(gitdir, files)
    else:
        index = read_index(gitdir)
        index += files
        write_index(gitdir, index)
