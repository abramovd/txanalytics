from fastapi import APIRouter, Depends

from models import Transaction
from storages import get_transactions_storage
from utils.pagination import Pagination, get_paginated_response_model

router = APIRouter()


@router.get('/', response_model=get_paginated_response_model(Transaction))
async def get_transactions(pagination: Pagination = Depends()):
    storage = get_transactions_storage()
    txs = storage.list_transactions(
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return pagination.get_paginated_response(
        result=txs,
        count=storage.count_transactions(),
    )
