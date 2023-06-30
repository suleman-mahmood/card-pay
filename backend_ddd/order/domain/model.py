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
class Vendor:
    vendor_id: str
    vendor_name: str
    available_categories : List

@dataclass
class AddOn:
    add_on_id: str
    name:str
    description:str
    quantity:int

@dataclass
class MenuItem:
    vendor_id: str
    item_id: str
    name:str
    quantity: int
    description: str
    optional_add_on: Set[AddOn]
    compulsary_add_on: Set[AddOn]
    category: str 
    date_range : List #Should be a list of 24 elements of 1s and 0s

@dataclass(frozen=True)
class OrderItem:
    vendor_id: str
    item_id: str
    name:str
    quantity: int
    description: str
    optional_add_on: Set[AddOn]
    compulsary_add_on: Set[AddOn]
    category: str 

@dataclass
class Order:
    user_id: str
    order_id: str
    category: OrderCategory #0 is for pickup and 1 is for delivery convert to enum
    cart: Set[str] #Collection of item ids to order, item ids belong to order item not menu item
    status: OrderStatus
    comment: str

    def AcceptOrder(self): #Do we check for date range of items here or on command level?? PRIORITY
        if len(self.cart) > 0:
            self.status = OrderStatus.INITIATE
        else:
            raise ValueError("Cart is empty")

    def DeclineOrder(self, reason):
        self.status = OrderStatus.DECLINE
        self.comment = reason


        #Place order not an explicit function because it will be placed when object of order class will be made




