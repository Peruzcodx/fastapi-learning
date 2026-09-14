from pydantic import BaseModel


class OrderCreate(BaseModel):
    product: str
    amount: float


class AllOrder(BaseModel):
    id: int
    user_id: int
    product: str
    amount: float