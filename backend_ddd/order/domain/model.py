from dataclasses import dataclass
from typing import List, Set
from uuid import uuid4


@dataclass(frozen=True)
class Item:
    user_id: str
    vendor_id: str
    item_id: str
    name:str
    quantity: int
    description: str
    optional_add_on: Set
    compulsary_add_on: Set

    # def increase_quantity(self):
    #     self.quantity += 1

    # def decrease_quantity(self):
    #     self.quantity -= 1

    # def choose_compulsory(self, add_on_id):
    #     self.compulsary_add_on.add(add_on_id)
    
    # def choose_optional(self, add_on_ids : list()):
    #     for i in add_on_ids:
    #         self.optional_add_on.add(i)

@dataclass
class Order:
    user_id: str
    order_id: str
    category: bool #0 is for pickup and 1 is for delivery
    cart: Set[Item] #Collection of item ids to order

    def add_to_cart(self, item_id):
        self.cart.add(item_id)



@dataclass
class AddOn:
    add_on_id: str
    name:str
    description:str
    quantity:int