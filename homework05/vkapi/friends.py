import dataclasses
import time
import typing as tp

import requests
from vkapi import config, session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.List[tp.Dict[str, tp.Any]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    get = requests.get(
        f"{domain}/friends.get",
        params={
            "access_token": access_token,
            "user_id": user_id,
            "count": count,
            "offset": offset,
            "fields": fields,
            "v": v,
        },
    )

    response = get.json()["response"]
    return FriendsResponse(count=response["count"], items=response["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.List[MutualFriends]:

    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    mutual_friends = []

    if target_uids is None:
        ln = 1
    else:
        ln = (len(target_uids) / 100).__ceil__()

    for i in range(ln):
        get = requests.get(
            f"{domain}/friends.getMutual",
            params={
                "access_token": access_token,
                "source_uid": source_uid,
                "target_uid": target_uid,
                "target_uids": target_uids,
                "order": order,
                "count": count,
                "offset": i * 100,
                "v": v,
            },
        )
        response = get.json()["response"]
        mutual_friends += response

        if i % 2 == 0:
            time.sleep(1)

    return mutual_friends
