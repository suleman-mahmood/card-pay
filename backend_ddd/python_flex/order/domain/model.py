from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    INITIATE = 0
    ACCEPT = 1
    DECLINE = 2
    PREPARING = 3
    PREPARED = 4
    DELIVERING_PICKUP = 5
    COMPLETED = 6

class OrderCategory(Enum):
    PICKUP = 0
    DELIVERY = 1

@dataclass
class Category:
    name:str
    description: str

@dataclass
class Vendor:
    vendor_id: str
    vendor_name: str
    available_categories : List[Category]

@dataclass
class AddOn:
    add_on_id: str
    vendor_id:str
    name:str
    description:str
    quantity:int

    def __hash__(self) -> int:
        return hash(self.add_on_id)

    def __eq__(self, o) -> bool:
        return(
            self.add_on_id == o.add_on_id and self.vendor_id == o.vendor_id
        )

    

@dataclass
class MenuItem:
    vendor_id: str
    menu_item_id: str
    name:str
    description: str
    optional_add_on: Set[AddOn]
    compulsary_add_on: Set[AddOn]
    category: Category
    date_range : List[int] #Should be a list of 24 elements of 1s and 0s

@dataclass(frozen=True)
class OrderItem:
    order_item_id: str
    menu_item_id: str #References Menu Item class object
    quantity: int
    compulsory_add_on: AddOn
    optional_add_ons: Set[AddOn]
    

@dataclass
class Order:
    user_id: str
    vendor_id: str
    order_id: str
    category: OrderCategory #0 is for pickup and 1 is for delivery convert to enum
    cart: Set[OrderItem] #Collection of order items
    status: OrderStatus
    comment: str
    cancellation_reason: str

    def AcceptOrder(self): #Do we check for date range of items here or on command level?? PRIORITY
        if len(self.cart) <= 0:
            raise ValueError("Cart is empty")
        self.status = OrderStatus.ACCEPT
            

    def DeclineOrder(self, reason):
        self.status = OrderStatus.DECLINE
        self.cancellation_reason = reason


        #Place order not an explicit function because it will be placed when object of order class will be made




