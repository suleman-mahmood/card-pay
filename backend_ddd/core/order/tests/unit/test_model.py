import pytest
from ...domain.model import (
    OrderStatus,
    OrderCategory,
    OrderItem,
    Order,
    Category,
    Vendor,
    AddOn,
    MenuItem,
)

lettuce = AddOn(
    add_on_id="ADD456",
    vendor_id="VDR123",
    name="lettuce",
    description="green leaves",
    quantity=1
)

mayo = AddOn(
        add_on_id="ADD123",
        vendor_id="VDR123",
        name="mayo",
        description="white sauce",
        quantity=1
    )

    

menu_item = MenuItem(
    vendor_id="VDR123",
    menu_item_id="MITM123",
    name="zinger",
    description="crispy chicken burger",
    category= Category(name="main course", description=None),
    optional_add_on=None,
    compulsary_add_on={lettuce, mayo},
    date_range=[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]

)

order_item = OrderItem(
    order_item_id="OITM123",
    menu_item_id="MITM123",
    quantity=2,
    compulsory_add_on=mayo,
    optional_add_ons=None
)

my_order = Order(
    user_id="USR123",
    vendor_id= "VDR123",
    order_id="ODR123",
    category=OrderCategory.PICKUP,
    status=OrderStatus.INITIATE,
    comment="prepare fast",
    cancellation_reason=None,
    cart={order_item}
    )

def test_create_order():
    assert my_order.vendor_id == menu_item.vendor_id
    assert my_order.category == OrderCategory.PICKUP
    assert my_order.status == OrderStatus.INITIATE
    assert len(my_order.cart) > 0

def test_accept_order():
    my_order.status = OrderStatus.ACCEPT
    assert my_order.status == OrderStatus.ACCEPT

def test_decline_order():
    my_order.status = OrderStatus.DECLINE
    assert my_order.status == OrderStatus.DECLINE
