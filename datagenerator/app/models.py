import datetime
import uuid

from decimal import Decimal
from typing import List

from pydantic import BaseModel, condecimal


class Account(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime


class Attachment(BaseModel):
    id: uuid.UUID
    format: str
    active: bool
    added_at: datetime.datetime


class Category(BaseModel):
    id: uuid.UUID
    name: str
    added_at: datetime.datetime


class Transaction(BaseModel):
    id: uuid.UUID

    account: Account

    timestamp: datetime.datetime
    amount: condecimal(gt=Decimal('0'), decimal_places=2)
    currency: str = 'EUR'
    direction: str
    type: str

    category: Category = None
    vat_rate: str = None
    attachments: List[Attachment] = None
