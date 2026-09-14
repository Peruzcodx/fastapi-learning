from multiprocessing import connection

from fastapi import APIRouter,HTTPException, Depends
from schemas import order
from security import get_current_user
from schemas.order import OrderCreate, AllOrder
from services.order_service import create_order, get_orders,get_order,delete_order,update_order
from database import get_db
router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=AllOrder)
def create_new_order(
    order: OrderCreate,
    current_user: int = Depends(get_current_user),
    connection = Depends(get_db)):
    return create_order(order, current_user, connection)

@router.get("/", response_model=list[AllOrder])
def get_all_orders(
    current_user: int = Depends(get_current_user),
    connection=Depends(get_db)
):
    return get_orders(connection, current_user)
@router.get("/{order_id}", response_model=AllOrder)
def get_single_order(order_id: int,
                     current_user: int = Depends(get_current_user),
                     connection =Depends(get_db)):
    order = get_order(order_id, current_user, connection)    
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    return order 
@router.delete("/{order_id}")
def delete_single_orders(
    order_id: int,
    current_user: int = Depends(get_current_user),
    connection =Depends(get_db)):

    deleted_id = delete_order(order_id,current_user,connection)

    if deleted_id is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "message": "Order deleted successfully",
        "id": deleted_id
    }


@router.put("/{order_id}", response_model=AllOrder)
def update_single_order(
    order_id: int,
    order: OrderCreate,
    current_user: int = Depends(get_current_user),
    connection =Depends(get_db)):

    updated_order = update_order(order_id, order, current_user, connection)

    if updated_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return updated_order
