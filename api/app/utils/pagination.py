from typing import Optional, Iterable, List, Type

from starlette.requests import Request
from pydantic import create_model, BaseModel

from config import DEFAULT_PAGE_LIMIT


class Pagination(object):

    def __init__(
        self, request: Request, offset: int = 0,
        limit: int = DEFAULT_PAGE_LIMIT,
    ):
        self.request = request
        self.offset = offset
        self.limit = limit

    def get_next_url(self, count) -> Optional[str]:
        """
        Constructs `next` parameter in resulting JSON,
        produces URL for next "page" of paginated results.
        """
        if self.offset + self.limit >= count:
            return None

        return str(
            self.request.url.include_query_params(
                limit=self.limit, offset=self.offset + self.limit
            )
        )

    def get_previous_url(self) -> Optional[str]:
        """
        Constructs `previous` parameter in resulting JSON,
        produces URL for previous "page" of paginated results.
        """
        if self.offset <= 0:
            return None

        if self.offset - self.limit <= 0:
            return str(self.request.url.remove_query_params(keys=["offset"]))

        return str(
            self.request.url.include_query_params(
                limit=self.limit, offset=self.offset - self.limit
            )
        )

    def get_paginated_response(self, result: Iterable, count: int) -> dict:
        return {
            "count": count,
            "next": self.get_next_url(count),
            "previous": self.get_previous_url(),
            "data": result,
        }


def get_paginated_response_model(response_model: Type[BaseModel]):
    return create_model(
        f'Paginated {response_model.__name__}s',
        count=(int, ...),
        next=(Optional[str], None),
        previous=(Optional[str], None),
        data=(List[response_model], ...),
    )
