from dataclasses import dataclass
from uuid import uuid4
from typing import List, Dict
from datetime import datetime
from core.order.domain import exceptions as ex
from enum import Enum


@dataclass
class Restaurant:
    """Entity for restaurant"""

    id: str
    name: str
    logo_url: str
    description: str
    active: bool
    timings: str
    created_at: datetime
    last_updated_at: datetime

    def _timings_checks(self, timings: str):
        if len(timings) != 24:
            raise ex.MissingTimingsValues("Timings length is not 24")

        for i in range(24):
            if timings[i] != "0" and timings[i] != "1":
                raise ex.InvalidTimingsValue("Timings should be 0 or 1")

    def validate(self):
        """Validate restaurant"""
        self._timings_checks(self.timings)

    def update_details(
        self,
        name: str,
        logo_url: str,
        description: str,
        timings: str,
        last_updated_at: datetime,
    ):
        """Update restaurant"""
        self._timings_checks(timings)

        self.name = name
        self.logo_url = logo_url
        self.description = description
        self.timings = timings
        self.last_updated_at = last_updated_at

    def activate(self):
        """Activate restaurant"""
        if self.active:
            raise ex.RestaurantAlreadyActive("Restaurant is already active")

        self.active = True

    def deactivate(self):
        """Deactivate restaurant"""
        if not self.active:
            raise ex.RestaurantAlreadyInactive("Restaurant is already inactive")

        self.active = False


@dataclass(frozen=True)
class CompulsoryAddon:
    """Value object"""

    id: str
    name: str
    price: int
    active: bool


@dataclass
class CompulsoryAddonCategory:
    """Entity for compulsory addon category"""

    id: str
    restaurant_id: str
    name: str
    created_at: datetime
    last_updated_at: datetime
    addons: List[CompulsoryAddon]

    def _addons_checks(self, addons: List[CompulsoryAddon]):
        if len(addons) == 0:
            raise ex.NoCompulsoryAddons("No compulsory addons provided")

        inactive_count = 0
        for addon in addons:
            if addon.price < 0:
                raise ex.NegativeCompulsoryAddonPrice(
                    "Compulsory addon price cannot be negative"
                )

            if addon.price > 1000:
                raise ex.CompulsoryAddonPriceCannotBeAbove1000(
                    "Compulsory addon price cannot be above 1000"
                )

            if not addon.active:
                inactive_count += 1

        if inactive_count == len(addons):
            raise ex.AllCompulsoryAddonsInactive(
                "All compulsory addons cannot be inactive"
            )

    def validate(self):
        """Validate compulsory addon category"""
        self._addons_checks(self.addons)

    def update_details(self, name: str, last_updated_at: datetime):
        """Update compulsory addon category"""
        self.name = name
        self.last_updated_at = last_updated_at

    def update_addons(self, addons: List[CompulsoryAddon], last_updated_at: datetime):
        """Update addons"""
        self._addons_checks(addons)
        self.addons = addons
        self.last_updated_at = last_updated_at


@dataclass
class OptionalAddon:
    """Entity for optional addon"""

    id: str
    restaurant_id: str
    name: str
    price: int
    active: bool
    created_at: datetime
    last_updated_at: datetime

    def _price_check(self, price: int):
        if price < 0:
            raise ex.NegativeOptionalAddonPrice(
                "Optional addon price cannot be negative"
            )

        if price > 1000:
            raise ex.OptionalAddonPriceCannotBeAbove1000(
                "Optional addon price cannot be above 1000"
            )

    def validate(self):
        """Validate optional addon"""
        self._price_check(self.price)

    def update_details(self, name: str, price: int, last_updated_at: datetime):
        """Update optional addon"""
        self._price_check(price)

        self.name = name
        self.price = price
        self.last_updated_at = last_updated_at

    def activate(self):
        """Activate optional addon"""
        if self.active:
            raise ex.OptionalAddonAlreadyActive("Optional addon is already active")

        self.active = True

    def deactivate(self):
        """Deactivate optional addon"""
        if not self.active:
            raise ex.OptionalAddonAlreadyInactive("Optional addon is already inactive")

        self.active = False


# we need to construct an item validator too, where we can check that compulsory addon categories and optional addons belong to the same restaurant as the item
@dataclass
class Item:
    """Entity for item"""

    id: str
    restaurant_id: str
    compulsory_addon_category_ids: List[str]
    optional_addon_ids: List[str]
    name: str
    price: int
    active: bool
    timings: str
    created_at: datetime
    last_updated_at: datetime

    # def _item_checks(self, price: int, timings: str):
    #     if price < 0:
    #         raise ex.InvalidItemPrice("Item price cannot be 0 or below")

    #     if price > 1000:
    #         raise ex.ItemPriceCannotBeAbove1000("Item price cannot be above 1000")

    #     if len(timings) != 24:
    #         raise ex.MissingTimingsValues("Timings length is not 24")

    #     for i in range(24):
    #         if timings[i] != "0" and timings[i] != "1":
    #             raise ex.InvalidTimingsValue("Timings should be 0 or 1")

    # def validate(self):
    #     """Validate item"""
    #     self._item_checks(self.price, self.timings)

    def update_details(
        self,
        compulsory_addon_category_ids: List[str],
        optional_addon_ids: List[str],
        name: str,
        price: int,
        timings: str,
        last_updated_at: datetime,
    ):
        """Update item"""
        # self._item_checks(price, timings)

        self.compulsory_addon_category_ids = compulsory_addon_category_ids
        self.optional_addon_ids = optional_addon_ids
        self.name = name
        self.price = price
        self.timings = timings
        self.last_updated_at = last_updated_at

    def activate(self):
        """Activate item"""
        if self.active:
            raise ex.ItemAlreadyActive("Item is already active")

        self.active = True

    def deactivate(self):
        """Deactivate item"""
        if not self.active:
            raise ex.ItemAlreadyInactive("Item is already inactive")

        self.active = False


@dataclass(frozen=True)
class OrderItemCompulsoryAddonChoice:
    """Value object"""

    compulsory_addon_id: str
    compulsory_category_id: str


@dataclass(frozen=True)
class OrderItemOptionalAddon:
    """Value object"""

    optional_addon_id: str
    quantity: int


@dataclass(frozen=True)
class OrderItem:
    """Value object"""

    id: str
    item_id: str
    quantity: int
    compulsory_addons: List[OrderItemCompulsoryAddonChoice]
    optional_addons: List[OrderItemOptionalAddon]


class OrderStatus(str, Enum):
    """order status enum"""

    PENDING = 1
    FAILED = 2
    VALIDATED = 3
    ACCEPTED = 4
    REJECTED = 5
    COMPLETED = 6


class OrderType(str, Enum):
    """order type enum"""

    DELIVERY = 1
    PICKUP = 2


@dataclass
class Order:
    """Entity for order"""

    id: str
    restaurant_id: str
    special_instructions: str
    type: OrderType
    status: OrderStatus
    created_at: datetime
    items: List[OrderItem]
    amount: int

    def update_status_to_failed(self):
        """Update order status to failed"""
        if self.status != OrderStatus.PENDING:
            raise ex.OrderStatusIsNotPending("Only pending orders can be failed")

        self.status = OrderStatus.FAILED

    def update_status_to_validated(self):
        """Update order status to validated"""
        if self.status != OrderStatus.PENDING:
            raise ex.OrderStatusIsNotPending("Only pending orders can be failed")

        self.status = OrderStatus.VALIDATED

    def update_amount(self, amount: int):
        """Update order amount"""
        if self.status != OrderStatus.VALIDATED:
            raise ex.OrderStatusIsNotValidated(
                "Amount of only validated orders can be updated"
            )
        self.amount = amount

    def accept(self):
        """Accept order"""
        if self.order_status != OrderStatus.VALIDATED:
            raise ex.OrderStatusIsNotValidated("Only validated orders can be accepted")

        self.order_status = OrderStatus.ACCEPTED

    def reject(self):
        """Reject order"""
        if self.order_status != OrderStatus.VALIDATED:
            raise ex.OrderStatusIsNotValidated("Only validated orders can be rejected")

        self.order_status = OrderStatus.REJECTED

    def complete(self):
        """Complete order"""
        if self.order_status != OrderStatus.ACCEPTED:
            raise ex.OrderStatusIsNotAccepted("Only accepted orders can be completed")

        self.order_status = OrderStatus.COMPLETED


@dataclass(frozen=True)
class ValidateItemChoiceObject:
    """Value object"""

    item_choice: Item
    compulsory_addon_categories_choice: List[
        CompulsoryAddonCategory
    ]  # ordered categories
    optional_addons_choice: List[OptionalAddon]


@dataclass
class ItemValidator:
    item: Item
    compulsory_addon_categories: Dict[str, CompulsoryAddonCategory]
    optional_addons: Dict[str, OptionalAddon]

    def validate_item(self):
        """Validate item"""

        # item checks
        if self.item.price < 0:
            raise ex.InvalidItemPrice("Item price cannot be below 0")

        if self.item.price > 1000:
            raise ex.ItemPriceCannotBeAbove1000("Item price cannot be above 1000")

        if len(self.item.timings) != 24:
            raise ex.MissingTimingsValues("Timings length is not 24")

        for i in range(24):
            if self.item.timings[i] != "0" and self.item.timings[i] != "1":
                raise ex.InvalidTimingsValue("Timings should be 0 or 1")

        # missing addon categories or missing addon checks
        if sorted(self.item.compulsory_addon_category_ids) != sorted(
            self.compulsory_addon_categories.keys()
        ):
            raise ex.ItemAndPassedCompulsoryAddonCategoriesMismatch(
                "Item and passed compulsory addon categories mismatch"
            )

        if sorted(self.item.optional_addon_ids) != sorted(self.optional_addons.keys()):
            raise ex.ItemAndPassesOptionalAddonCategoriesMismatch(
                "Item and passed optional addon categories mismatch"
            )

        # compulsory addon categories checks
        for category_id in self.item.compulsory_addon_category_ids:
            category = self.compulsory_addon_categories[category_id]
            if category.restaurant_id != self.item.restaurant_id:
                raise ex.CompulsoryAddonCategoryAndRestaurantMismatch(
                    f"Compulsory addon category ({category.name}) does not belong to {self.item.restaurant_id}"
                )

        # optional addon checks
        for addon_id in self.item.optional_addon_ids:
            addon = self.optional_addons[addon_id]
            if addon.restaurant_id != self.item.restaurant_id:
                raise ex.OptionalAddonRestaurantMismatch(
                    f"Optional addon ({addon.name}) does not belong to {self.item.restaurant_id}"
                )


@dataclass
class OrderValidator:
    """order validation service"""

    order: Order
    restaurant: Restaurant
    # the dict will be as follows {id "which is ordered item object id": ValidateItemObject}
    ordered_items_details: Dict[str, ValidateItemChoiceObject]

    def validate_order(self):
        """Validate order"""
        if self.order.status != OrderStatus.PENDING:
            raise ex.OrderStatusIsNotPending("Only pending orders can be validated")

        # basic order checks
        if self.restaurant.id != self.order.restaurant_id:
            raise ex.OrderRestaurantMismatch(
                "Wrong restaurant passed for order validation"
            )

        if len(self.order.items) == 0:
            raise ex.NoItemsProvided("No items exist in order")

        # restaurant checks

        if self.restaurant.active is False:
            raise ex.RestaurantInactive(f"{self.restaurant.name} is inactive")

        # order_PKT = self.order.created_at.hour + 5  # PKT is 5 hours ahead of UTC
        # if order_PKT >= 24:
        #     order_PKT -= 24
        order_hour = self.order.created_at.hour

        if self.restaurant.timings[order_hour] == "0":
            raise ex.RestaurantClosed(f"{self.restaurant.name} is closed right now")

        # item checks
        if len(self.ordered_items_details) != len(self.order.items):
            raise ex.IncorrectNumberOfItemsPassed(
                "Incorrect number of items passed for validation"
            )

        for ordered_item in self.order.items:
            if ordered_item.id not in self.ordered_items_details.keys():
                raise ex.OrderedItemDetailsNotPassed(
                    "Ordered item details not passed for validation"
                )

            menu_item = self.ordered_items_details[ordered_item.id].item_choice

            if menu_item.restaurant_id != self.order.restaurant_id:
                raise ex.ItemRestaurantMismatch(
                    f"{menu_item.name} does not belong to {self.restaurant.name}"
                )

            if menu_item.active is False:
                raise ex.ItemInactive(f"{menu_item.name} is not avaialble")

            if menu_item.timings[order_hour] == "0":
                raise ex.ItemNotAvailable(
                    f"{menu_item.name} is not available right now"
                )

        # optional addon checks
        for ordered_item in self.order.items:
            optional_addons = self.ordered_items_details[
                ordered_item.id
            ].optional_addons_choice
            for addon in optional_addons:
                if addon.restaurant_id != self.order.restaurant_id:
                    raise ex.OptionalAddonRestaurantMismatch(
                        f"Optional addon ({addon.name}) does not belong to {self.restaurant.name}"
                    )

                if addon.active is False:
                    raise ex.OptionalAddonInactive(
                        f"Optional addon ({addon.name}) is not available right now"
                    )

        # compulsory addon checks
        for ordered_item in self.order.items:
            menu_item = self.ordered_items_details[ordered_item.id].item_choice

            ordered_item_compulsory_addon_category_ids = [
                choice.compulsory_category_id
                for choice in ordered_item.compulsory_addons
            ]

            passed_compulsory_addon_category_ids = [
                category.id
                for category in self.ordered_items_details[
                    ordered_item.id
                ].compulsory_addon_categories_choice
            ]

            actual_compulsory_addon_category_ids = (
                menu_item.compulsory_addon_category_ids
            )

            if sorted(ordered_item_compulsory_addon_category_ids) != sorted(
                passed_compulsory_addon_category_ids
            ):
                raise ex.OrderAndPassedCompulsaryAddonCategoriesMismatch(
                    "Order and passed compulsory addon categories mismatch"
                )

            if sorted(actual_compulsory_addon_category_ids) != sorted(
                ordered_item_compulsory_addon_category_ids
            ):
                raise ex.ActualAndOrderedCompulsaryAddonCategoriesMismatch(
                    "Actual and ordered compulsory addon categories mismatch"
                )

            for choice in ordered_item.compulsory_addons:
                category = next(
                    (
                        category
                        for category in self.ordered_items_details[
                            ordered_item.id
                        ].compulsory_addon_categories_choice
                        if category.id == choice.compulsory_category_id
                    ),
                    None,
                )
                if category.restaurant_id != self.order.restaurant_id:
                    raise ex.CompulsoryAddonCategoryAndRestaurantMismatch(
                        f"Compulsory addon category ({category.name}) does not belong to {self.restaurant.name}"
                    )

                selected_addon = next(
                    (
                        addon
                        for addon in category.addons
                        if addon.id == choice.compulsory_addon_id
                    ),
                    None,
                )

                if selected_addon is None:
                    raise ex.CompulsoryAddonNotFound(
                        "Compulsory addon not found in the referenced category"
                    )

                if selected_addon.active is False:
                    raise ex.CompulsoryAddonInactive(
                        f"Compulsory addon ({selected_addon.name}) is inactive"
                    )

        return


@dataclass
class OrderAmountCalculator:
    """order amount calculator service"""

    order: Order
    ordered_items_details: Dict[str, ValidateItemChoiceObject]

    def calculate(self):
        if self.order.status != OrderStatus.VALIDATED:
            raise ex.OrderStatusIsNotValidated(
                "Only validated orders can be calculated"
            )

        total_amount = 0

        for ordered_item in self.order.items:
            actual_item = self.ordered_items_details[ordered_item.id].item_choice
            amount = actual_item.price

            for choice in ordered_item.compulsory_addons:
                category = next(
                    (
                        category
                        for category in self.ordered_items_details[
                            ordered_item.id
                        ].compulsory_addon_categories_choice
                        if category.id == choice.compulsory_category_id
                    ),
                    None,
                )

                addon = next(
                    (
                        addon
                        for addon in category.addons
                        if addon.id == choice.compulsory_addon_id
                    ),
                    None,
                )

                amount = amount + addon.price

            for choice in ordered_item.optional_addons:

                optional_addon = next(
                    (
                        optional_addon
                        for optional_addon in self.ordered_items_details[
                            ordered_item.id
                        ].optional_addons_choice
                        if optional_addon.id == choice.optional_addon_id
                    ),
                    None,
                )

                amount = amount + (optional_addon.price * choice.quantity)

            amount = amount * ordered_item.quantity

            total_amount = total_amount + amount

        return total_amount
