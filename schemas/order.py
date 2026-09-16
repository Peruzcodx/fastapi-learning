from pydantic import BaseModel, Field 


class OrderCreate(BaseModel):
    product: str
    amount: float = Field(gt=0)


class AllOrder(BaseModel):
    id: int
    user_id: int
    product: str
    amount: float