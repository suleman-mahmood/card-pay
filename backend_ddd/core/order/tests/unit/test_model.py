"""
Usecases
- validate order, customer
- place pickup/delivery order request, customer
- accept order request, restaurant
- reject order request, restaurant
- change item availability, restaurant
- change compulsory addon availability, restaurant
- change optional addon availability, restaurant
- rating from customer
Entities


Value Objects


Services


Aggregate Roots

Invariants

"""
from datetime import datetime
from core.order.domain import model as mdl
import pytest
from core.order.domain import exceptions as ex

import pytest
from uuid import uuid4


def seed_restaurant():
    return mdl.Restaurant(
        id="jhonny-jugnu",
        name="Jhonny Jugnu",
        logo_url="https://www.google.com",
        description="Wraps and burgers",
        active=True,
        timings="111111111111111111111111",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )


def seed_optional_addon():
    return mdl.OptionalAddon(
        id="coke-id",
        restaurant_id="jhonny-jugnu",
        name="Coca Cola",
        price=70,
        active=True,
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )


def seed_compulsory_addon_category():
    return mdl.CompulsoryAddonCategory(
        id="meat-id",
        restaurant_id="jhonny-jugnu",
        name="Meat",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
        addons=[
            mdl.CompulsoryAddon(
                id="fried-chicken-id",
                name="Fried chicken",
                price=150,
                active=True,
            ),
            mdl.CompulsoryAddon(
                id="beef-patty",
                name="Beef patty",
                price=200,
                active=True,
            ),
        ],
    )


def seed_item():
    return mdl.Item(
        id="wrap-id",
        restaurant_id="jhonny-jugnu",
        compulsory_addon_category_ids=["meat-id", "sauce-id"],
        optional_addon_ids=["coke-id", "fries-id", "fried-chicken-id"],
        name="Wrap",
        price=600,
        active=True,
        timings="111111111111111111111111",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )


def test_setup_restaurant():
    restaurant = seed_restaurant()

    restaurant.timings = "000001111"
    with pytest.raises(ex.MissingTimingsValues, match="Timings length is not 24"):
        restaurant.validate()

    restaurant.timings = "000001111111111110000002"
    with pytest.raises(ex.InvalidTimingsValue, match="Timings should be 0 or 1"):
        restaurant.validate()

    restaurant.timings = "000001111111111110000000"
    restaurant.validate()
    new_timings = "000001111111111110000001"
    restaurant.update_details(
        name=restaurant.name,
        logo_url=restaurant.logo_url,
        description=restaurant.description,
        timings=new_timings,
        last_updated_at=datetime.now(),
    )
    assert restaurant.timings == new_timings

    invalid_timings = "000002111111111110000001"
    with pytest.raises(ex.InvalidTimingsValue, match="Timings should be 0 or 1"):
        restaurant.update_details(
            name=restaurant.name,
            logo_url=restaurant.logo_url,
            description=restaurant.description,
            timings=invalid_timings,
            last_updated_at=datetime.now(),
        )

    assert restaurant.timings == new_timings

    with pytest.raises(
        ex.RestaurantAlreadyActive, match="Restaurant is already active"
    ):
        restaurant.activate()

    restaurant.deactivate()
    assert restaurant.active is False

    with pytest.raises(
        ex.RestaurantAlreadyInactive, match="Restaurant is already inactive"
    ):
        restaurant.deactivate()

    restaurant.activate()
    assert restaurant.active is True


def test_setup_CompulsoryAddonCategory():
    compulsory_addon_category = seed_compulsory_addon_category()
    compulsory_addon_category.addons = []

    with pytest.raises(ex.NoCompulsoryAddons, match="No compulsory addons provided"):
        compulsory_addon_category.validate()

    compulsory_addon_category = seed_compulsory_addon_category()

    with pytest.raises(
        ex.NegativeCompulsoryAddonPrice,
        match="Compulsory addon price cannot be negative",
    ):
        compulsory_addon_category.update_addons(
            addons=[
                mdl.CompulsoryAddon(
                    id="fried-chicken-id",
                    name="fried chicken",
                    price=-1,
                    active=True,
                ),
                mdl.CompulsoryAddon(
                    id="fish-patty",
                    name="fish patty",
                    price=200,
                    active=True,
                ),
            ],
            last_updated_at=datetime.now(),
        )

    compulsory_addon_category.update_addons(
        addons=[
            mdl.CompulsoryAddon(
                id="fried-chicken-id",
                name="fried chicken",
                price=0,
                active=True,
            ),
            mdl.CompulsoryAddon(
                id="fish-patty",
                name="fish patty",
                price=200,
                active=True,
            ),
        ],
        last_updated_at=datetime.now(),
    )
    compulsory_addon_category.validate()
    assert compulsory_addon_category.addons[0].price == 0

    compulsory_addon_category.update_addons(
        addons=[
            mdl.CompulsoryAddon(
                id="fried-chicken-id",
                name="fried chicken",
                price=0,
                active=False,
            ),
            mdl.CompulsoryAddon(
                id="fish-patty",
                name="fish patty",
                price=200,
                active=True,
            ),
        ],
        last_updated_at=datetime.now(),
    )
    compulsory_addon_category.validate()
    assert compulsory_addon_category.addons[0].active is False

    with pytest.raises(
        ex.AllCompulsoryAddonsInactive, match="All compulsory addons cannot be inactive"
    ):
        compulsory_addon_category.update_addons(
            addons=[
                mdl.CompulsoryAddon(
                    id="fried-chicken-id",
                    name="fried chicken",
                    price=0,
                    active=False,
                ),
                mdl.CompulsoryAddon(
                    id="fish-patty",
                    name="fish patty",
                    price=200,
                    active=False,
                ),
            ],
            last_updated_at=datetime.now(),
        )
    compulsory_addon_category.update_details(
        name="updated name",
        last_updated_at=datetime.now(),
    )
    assert compulsory_addon_category.name == "updated name"

    new_adddons = [
        mdl.CompulsoryAddon(
            id="grilled-chicken-id",
            name="grilled chicken",
            price=150,
            active=False,
        ),
        mdl.CompulsoryAddon(
            id="fish-patty",
            name="fish patty",
            price=200,
            active=True,
        ),
    ]

    compulsory_addon_category.update_addons(
        addons=new_adddons,
        last_updated_at=datetime.now(),
    )

    assert compulsory_addon_category.addons == new_adddons


def test_setup_optional_addon():
    optional_addon = seed_optional_addon()
    optional_addon.price = -1
    with pytest.raises(
        ex.NegativeOptionalAddonPrice, match="Optional addon price cannot be negative"
    ):
        optional_addon.validate()

    optional_addon.price = 1
    optional_addon.validate()
    assert optional_addon.price == 1

    with pytest.raises(
        ex.NegativeOptionalAddonPrice, match="Optional addon price cannot be negative"
    ):
        optional_addon.update_details(
            name=optional_addon.name,
            price=-1,
            last_updated_at=datetime.now(),
        )

    assert optional_addon.price == 1

    with pytest.raises(
        ex.OptionalAddonAlreadyActive, match="Optional addon is already active"
    ):
        optional_addon.activate()

    optional_addon.deactivate()
    assert optional_addon.active is False

    with pytest.raises(
        ex.OptionalAddonAlreadyInactive, match="Optional addon is already inactive"
    ):
        optional_addon.deactivate()


def test_setup_item():
    item = seed_item()
    item.compulsory_addon_category_ids = []
    item.optional_addon_ids = []
    # item.validate()
    item_validator = mdl.ItemValidator(
        item=item,
        compulsory_addon_categories={},
        optional_addons={},
    )

    item_validator.validate_item()

    with pytest.raises(ex.InvalidItemPrice, match="Item price cannot be below 0"):
        item.update_details(
            compulsory_addon_category_ids=item.compulsory_addon_category_ids,
            optional_addon_ids=item.optional_addon_ids,
            name=item.name,
            price=-1,
            timings=item.timings,
            last_updated_at=datetime.now(),
        )
        item_validator = mdl.ItemValidator(
            item=item,
            compulsory_addon_categories={},
            optional_addons={},
        )
        item_validator.validate_item()
    
    with pytest.raises(ex.MissingTimingsValues, match="Timings length is not 24"):
        new_timings = "000001111"
        item.update_details(
            compulsory_addon_category_ids=item.compulsory_addon_category_ids,
            optional_addon_ids=item.optional_addon_ids,
            name=item.name,
            price=1,
            timings=new_timings,
            last_updated_at=datetime.now(),
        )
        item_validator = mdl.ItemValidator(
            item=item,
            compulsory_addon_categories={},
            optional_addons={},
        )
        item_validator.validate_item()

    with pytest.raises(ex.InvalidTimingsValue, match="Timings should be 0 or 1"):
        new_timings = "000001111111111110000002"
        item.update_details(
            compulsory_addon_category_ids=item.compulsory_addon_category_ids,
            optional_addon_ids=item.optional_addon_ids,
            name=item.name,
            price=item.price,
            timings=new_timings,
            last_updated_at=datetime.now(),
        )
        item_validator = mdl.ItemValidator(
            item=item,
            compulsory_addon_categories={},
            optional_addons={},
        )
        item_validator.validate_item()

    item.update_details(
        compulsory_addon_category_ids=item.compulsory_addon_category_ids,
        optional_addon_ids=item.optional_addon_ids,
        name=item.name,
        price=1000,
        timings="000001111111111110000000",
        last_updated_at=datetime.now(),
    )
    item_validator = mdl.ItemValidator(
        item=item,
        compulsory_addon_categories={},
        optional_addons={},
    )
    item_validator.validate_item()

    assert item.price == 1000

def test_item_validator():
    restaurant = seed_restaurant()
    item = seed_item()
    compulsory_addon_sauce1 = mdl.CompulsoryAddon(
        id="chipotle-id",
        name="chipotle",
        price=50,
        active=True,
    )

    compulsory_addon_categories = mdl.CompulsoryAddonCategory(
        id="sauce-category-id",
        restaurant_id="some-other-id",
        name="sauce",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
        addons=[
            compulsory_addon_sauce1,
        ],
    )

    optional_addon = mdl.OptionalAddon(
        id="coke-id",
        name="coke",
        restaurant_id="some-otber-id",
        price=100,
        active=True,
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )

    item_validator = mdl.ItemValidator(
        item=item,
        compulsory_addon_categories={},
        optional_addons={},
    )

    item.compulsory_addon_category_ids = []
    item.optional_addon_ids = []

    item_validator.validate_item()

    item.compulsory_addon_category_ids = [
        compulsory_addon_categories.id,
    ]

    item.optional_addon_ids = [
        optional_addon.id,
    ]

    with pytest.raises(
        ex.ItemAndPassedCompulsoryAddonCategoriesMismatch,
        match="Item and passed compulsory addon",
    ):
        item_validator.validate_item()

    item_validator = mdl.ItemValidator(
        item=item,
        compulsory_addon_categories={
            compulsory_addon_categories.id: compulsory_addon_categories
        },
        optional_addons={},
    )

    with pytest.raises(
        ex.ItemAndPassesOptionalAddonCategoriesMismatch,
        match="Item and passed optional addon",
    ):
        item_validator.validate_item()

    item_validator = mdl.ItemValidator(
        item=item,
        compulsory_addon_categories={
            compulsory_addon_categories.id: compulsory_addon_categories
        },
        optional_addons={optional_addon.id: optional_addon},
    )

    with pytest.raises(
        ex.CompulsoryAddonCategoryAndRestaurantMismatch,
        match="Compulsory addon category",
    ):
        item_validator.validate_item()

    compulsory_addon_categories.restaurant_id = restaurant.id
    item_validator = mdl.ItemValidator(
        item=item,
        compulsory_addon_categories={
            compulsory_addon_categories.id: compulsory_addon_categories
        },
        optional_addons={optional_addon.id: optional_addon},
    )

    with pytest.raises(
        ex.OptionalAddonRestaurantMismatch,
        match="Optional addon",
    ):
        item_validator.validate_item()

    optional_addon.restaurant_id = restaurant.id
    item_validator = mdl.ItemValidator(
        item=item,
        compulsory_addon_categories={
            compulsory_addon_categories.id: compulsory_addon_categories
        },
        optional_addons={optional_addon.id: optional_addon},
    )

    item_validator.validate_item()


def seed_order_optional_addon():
    return mdl.OrderItemOptionalAddon(id="coke-id", quantity=2)


def seed_order_item():
    compulsory_addon_choice_1 = mdl.OrderItemCompulsoryAddonChoice(
        compulsory_addon_id="fried-chicken-id", compulsory_category_id="meat-id"
    )
    compulsory_addon_choice_2 = mdl.OrderItemCompulsoryAddonChoice(
        compulsory_addon_id="mushroom-id", compulsory_category_id="vegetable-id"
    )

    order_optional_addon_1 = mdl.OrderItemOptionalAddon(
        optional_addon_id="coke-id", quantity=2
    )
    order_optional_addon_2 = mdl.OrderItemOptionalAddon(
        optional_addon_id="fries-id", quantity=1
    )

    return mdl.OrderItem(
        id="1",
        item_id="wrap-id",  # Same as item_id
        quantity=1,
        compulsory_addons=[  # Same as number of compulsory categories
            compulsory_addon_choice_1,
            compulsory_addon_choice_2,
        ],
        optional_addons=[
            order_optional_addon_1,
            order_optional_addon_2,
        ],
    )


def seed_order():
    order_item_1 = seed_order_item()
    order_item_2 = seed_order_item()

    return mdl.Order(
        id="order-id",
        restaurant_id="jhonny-jugnu",
        special_instructions="Extra Saucy pls!!!",
        type=mdl.OrderType.DELIVERY,
        status=mdl.OrderStatus.PENDING,
        created_at=datetime.now(),
        items=[
            order_item_1,
            order_item_2,
        ],
        amount=0,
    )


# def test_validate_order():
#     restaurant = seed_restaurant()
#     item_1 = seed_item()
#     item_2 = seed_item()

#     # item_1_compulsory_addon_1 = seed_compulsory_addon()
#     # item_1_compulsory_addon_2 = seed_compulsory_addon()

#     item_1_compulsory_addon_1_category = seed_compulsory_addon_category()
#     item_1_compulsory_addon_2_category = seed_compulsory_addon_category()

#     item_1_optional_addon_1 = seed_optional_addon()
#     item_1_optional_addon_2 = seed_optional_addon()

#     # item_2_compulsory_addon_1 = seed_compulsory_addon()
#     # item_2_compulsory_addon_2 = seed_compulsory_addon()

#     item_2_compulsory_addon_1_category = seed_compulsory_addon_category()
#     item_2_compulsory_addon_2_category = seed_compulsory_addon_category()

#     item_2_optional_addon_1 = seed_optional_addon()
#     item_2_optional_addon_2 = seed_optional_addon()


#     order = seed_order()

#     vv = MenuCalculator(menu=[item_1, item_2])


#     assert vv.validate_order(order=order)


# def test_verify_order_item_not_found():
#     restaurant = seed_restaurant()
#     order = seed_order()
#     menu = seed_menu()
#     vv = OrderValidator(menu=menu)
#     invalid_item = menu.items[0]
#     invalid_item.id = "invalid_id"

#     order.items.append(invalid_item)
#     with pytest.raises(ItemNotFoundException, match="Items not found in menu"):
#         vv.validate_order(order=order)


def test_validating_a_not_pending_order():
    restaurant = seed_restaurant()
    order = seed_order()
    order.status = mdl.OrderStatus.VALIDATED
    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )

    with pytest.raises(
        ex.OrderStatusIsNotPending, match="Only pending orders can be validated"
    ):
        validator.validate_order()


def test_no_items_in_order():
    restaurant = seed_restaurant()
    order = seed_order()
    order.items = []
    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )
    with pytest.raises(ex.NoItemsProvided, match="No items exist in order"):
        validator.validate_order()


def test_validate_order_restaurant_checks():
    restaurant = seed_restaurant()
    order = seed_order()

    restaurant.id = "another_id"
    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )

    with pytest.raises(
        ex.OrderRestaurantMismatch, match="Wrong restaurant passed for order validation"
    ):
        validator.validate_order()

    restaurant.id = "jhonny-jugnu"
    restaurant.active = False
    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )

    with pytest.raises(ex.RestaurantInactive, match=f"{restaurant.name} is inactive"):
        validator.validate_order()

    restaurant.active = True
    restaurant.timings = "011111111111111111111111"
    order.created_at = datetime(2023, 1, 1, 0, 0, 0)

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )

    with pytest.raises(ex.RestaurantClosed, match=f"{restaurant.name} is closed"):
        validator.validate_order()

    order.created_at = datetime(2023, 1, 1, 0, 59, 59)
    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )

    with pytest.raises(ex.RestaurantClosed, match=f"{restaurant.name} is closed"):
        validator.validate_order()

    restaurant.timings = "111111111111111111111110"
    order.created_at = datetime(2023, 1, 1, 23, 0, 0)
    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )
    with pytest.raises(ex.RestaurantClosed, match=f"{restaurant.name} is closed"):
        validator.validate_order()

    restaurant.timings = "111111111110111111111111"
    order.created_at = datetime(2023, 1, 1, 11, 0, 0)
    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )
    with pytest.raises(ex.RestaurantClosed, match=f"{restaurant.name} is closed"):
        validator.validate_order()


def test_incorrect_number_of_items_details_passed_for_validation():
    restaurant = seed_restaurant()
    order = seed_order()
    ordered_item = seed_order_item()
    order.items = [ordered_item]

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={},
    )
    with pytest.raises(
        ex.IncorrectNumberOfItemsPassed,
        match="Incorrect number of items passed for validation",
    ):
        validator.validate_order()


def test_ordered_item_restaurant_mismatch():
    restaurant = seed_restaurant()

    item = seed_item()
    item.restaurant_id = "another_restaurant_id"

    order = seed_order()
    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[],
    )
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(
        ex.ItemRestaurantMismatch,
        match=f"{item.name} does not belong to {restaurant.name}",
    ):
        validator.validate_order()


def test_ordered_item_details_not_passed():
    restaurant = seed_restaurant()
    item1 = seed_item()
    item2 = seed_item()
    order = seed_order()
    ordered_item1 = mdl.OrderItem(
        id="1",
        item_id=item1.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[],
    )
    ordered_item2 = mdl.OrderItem(
        id="2",
        item_id=item2.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[],
    )
    ordered_item3 = mdl.OrderItem(
        id="3",
        item_id=item2.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[],
    )

    order.items = [ordered_item1, ordered_item2]

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={
            ordered_item2.id: mdl.ValidateItemChoiceObject(
                item_choice=item2,
                compulsory_addon_categories_choice=[],
                optional_addons_choice=[],
            ),
            ordered_item3.id: mdl.ValidateItemChoiceObject(
                item_choice=item2,
                compulsory_addon_categories_choice=[],
                optional_addons_choice=[],
            ),
        },
    )

    with pytest.raises(
        ex.OrderedItemDetailsNotPassed, match="Ordered item details not passed"
    ):
        validator.validate_order()


def test_ordered_item_inactive():
    restaurant = seed_restaurant()
    item = seed_item()
    item.deactivate()
    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(ex.ItemInactive, match=f"{item.name} is not avaialble"):
        validator.validate_order()


def test_ordered_item_closed():
    restaurant = seed_restaurant()
    item = seed_item()
    item.timings = "111111111111111111111110"
    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[],
    )

    order = seed_order()
    order.created_at = datetime(2023, 1, 1, 23, 0, 0)
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(
        ex.ItemNotAvailable, match=f"{item.name} is not available right now"
    ):
        validator.validate_order()


def test_optional_addon_checks():
    restaurant = seed_restaurant()
    item = seed_item()
    optional_addon1 = seed_optional_addon()
    optional_addon2 = seed_optional_addon()
    optional_addon2.restaurant_id = "another_restaurant_id"

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[
            mdl.OrderItemOptionalAddon(
                optional_addon_id=optional_addon1.id, quantity=1
            ),
            mdl.OrderItemOptionalAddon(
                optional_addon_id=optional_addon2.id, quantity=1
            ),
        ],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[],
        optional_addons_choice=[
            optional_addon1,
            optional_addon2,
        ],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(
        ex.OptionalAddonRestaurantMismatch,
        match=f"Optional addon",
    ):
        validator.validate_order()

    optional_addon2.restaurant_id = "jhonny-jugnu"
    optional_addon2.active = False

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[],
        optional_addons_choice=[
            optional_addon1,
            optional_addon2,
        ],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(ex.OptionalAddonInactive, match=f"Optional addon"):
        validator.validate_order()


def test_incorrect_compulsory_addons_passed_for_validation():
    restaurant = seed_restaurant()
    item = seed_item()
    compulsory_addon_category1 = seed_compulsory_addon_category()
    compulsory_addon_category1.id = "ct1-id"
    compulsory_addon_category2 = seed_compulsory_addon_category()
    compulsory_addon_category2.id = "ct2-id"
    compulsory_addon_category3 = seed_compulsory_addon_category()
    compulsory_addon_category3.id = "ct3-id"

    item.compulsory_addon_category_ids = [
        compulsory_addon_category1.id,
        compulsory_addon_category1.id,
        compulsory_addon_category2.id,
    ]

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="fried-chicken-id", compulsory_category_id="ct1-id"
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="mushroom-id", compulsory_category_id="ct1-id"
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="mushroom-id", compulsory_category_id="ct2-id"
            ),
        ],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(
        ex.OrderAndPassedCompulsaryAddonCategoriesMismatch,
        match="Order and passed compulsory addon categories mismatch",
    ):
        validator.validate_order()

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(
        ex.OrderAndPassedCompulsaryAddonCategoriesMismatch,
        match="Order and passed compulsory addon categories mismatch",
    ):
        validator.validate_order()


def test_actual_and_order_item_compulsary_addon_category_mismatch():
    restaurant = seed_restaurant()
    item = seed_item()
    compulsory_addon_category1 = seed_compulsory_addon_category()
    compulsory_addon_category1.id = "ct1-id"
    compulsory_addon_category2 = seed_compulsory_addon_category()
    compulsory_addon_category2.id = "ct2-id"
    compulsory_addon_category3 = seed_compulsory_addon_category()
    compulsory_addon_category3.id = "ct3-id"

    item.compulsory_addon_category_ids = [
        compulsory_addon_category1.id,
        compulsory_addon_category1.id,
        compulsory_addon_category2.id,
    ]

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="fried-chicken-id", compulsory_category_id="ct1-id"
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="mushroom-id", compulsory_category_id="ct2-id"
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="mushroom-id", compulsory_category_id="ct2-id"
            ),
        ],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )
    with pytest.raises(
        ex.ActualAndOrderedCompulsaryAddonCategoriesMismatch,
        match="Actual and ordered compulsory addon categories mismatch",
    ):
        validator.validate_order()


def test_compulsory_addon_category_and_restaurant_mismatch():
    restaurant = seed_restaurant()
    item = seed_item()
    compulsory_addon_category1 = seed_compulsory_addon_category()
    compulsory_addon_category1.id = "ct1-id"
    compulsory_addon_category1.addons = [
        mdl.CompulsoryAddon(
            id="fried-chicken-id",
            name="fried chicken",
            price=150,
            active=True,
        )
    ]
    compulsory_addon_category2 = seed_compulsory_addon_category()
    compulsory_addon_category2.id = "ct2-id"
    compulsory_addon_category2.restaurant_id = "another_restaurant_id"

    item.compulsory_addon_category_ids = [
        compulsory_addon_category1.id,
        compulsory_addon_category2.id,
    ]

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="fried-chicken-id", compulsory_category_id="ct1-id"
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="mushroom-id", compulsory_category_id="ct2-id"
            ),
        ],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(
        ex.CompulsoryAddonCategoryAndRestaurantMismatch,
        match=f"Compulsory addon",
    ):
        validator.validate_order()


def test_selected_addon_doesnt_exist_in_referenced_category():
    restaurant = seed_restaurant()
    item = seed_item()
    compulsory_addon_category1 = seed_compulsory_addon_category()
    compulsory_addon_category1.id = "ct1-id"
    compulsory_addon_category1.addons = [
        mdl.CompulsoryAddon(
            id="fried-chicken-id",
            name="fried chicken",
            price=150,
            active=True,
        )
    ]
    compulsory_addon_category2 = seed_compulsory_addon_category()
    compulsory_addon_category2.id = "ct2-id"
    compulsory_addon_category2.addons = [
        mdl.CompulsoryAddon(
            id="mushroom-id",
            name="mushroom",
            price=150,
            active=True,
        )
    ]

    item.compulsory_addon_category_ids = [
        compulsory_addon_category1.id,
        compulsory_addon_category2.id,
    ]

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="fried-chicken-id", compulsory_category_id="ct1-id"
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="olives-id", compulsory_category_id="ct2-id"
            ),
        ],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )
    with pytest.raises(
        ex.CompulsoryAddonNotFound,
        match="Compulsory addon not found in the referenced category",
    ):
        validator.validate_order()


def test_selected_addon_not_active():
    restaurant = seed_restaurant()
    item = seed_item()
    compulsory_addon_category1 = seed_compulsory_addon_category()
    compulsory_addon_category1.id = "ct1-id"
    compulsory_addon_category1.addons = [
        mdl.CompulsoryAddon(
            id="fried-chicken-id",
            name="fried chicken",
            price=150,
            active=True,
        )
    ]
    compulsory_addon_category2 = seed_compulsory_addon_category()
    compulsory_addon_category2.id = "ct2-id"
    compulsory_addon_category2.addons = [
        mdl.CompulsoryAddon(
            id="mushroom-id",
            name="mushroom",
            price=150,
            active=False,
        )
    ]

    item.compulsory_addon_category_ids = [
        compulsory_addon_category1.id,
        compulsory_addon_category2.id,
    ]

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="fried-chicken-id", compulsory_category_id="ct1-id"
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id="mushroom-id", compulsory_category_id="ct2-id"
            ),
        ],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    with pytest.raises(
        ex.CompulsoryAddonInactive,
        match=f"Compulsory",
    ):
        validator.validate_order()


def test_validating_order_with_no_compulsary_addons():
    restaurant = seed_restaurant()
    item = seed_item()
    item.compulsory_addon_category_ids = []
    # item.validate()

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )
    validator.validate_order()
    order.update_status_to_validated()

    assert order.status == mdl.OrderStatus.VALIDATED


def test_validating_order_with_multiple_same_compulsary_addon_categories():
    restaurant = seed_restaurant()
    item = seed_item()
    compulsory_addon_sauce1 = mdl.CompulsoryAddon(
        id="chipotle-id",
        name="chipotle",
        price=150,
        active=True,
    )
    compulsory_addon_sauce2 = mdl.CompulsoryAddon(
        id="atomic-id",
        name="atomic",
        price=150,
        active=True,
    )
    compulsory_addon_sauce3 = mdl.CompulsoryAddon(
        id="garlic-id",
        name="garlic",
        price=150,
        active=True,
    )
    compulsory_addon_category1 = mdl.CompulsoryAddonCategory(
        id="sauce-id",
        restaurant_id=restaurant.id,
        name="sauce",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
        addons=[
            compulsory_addon_sauce1,
            compulsory_addon_sauce2,
            compulsory_addon_sauce3,
        ],
    )

    compulsory_addon_cheese1 = mdl.CompulsoryAddon(
        id="single-cheese-id",
        name="single cheese",
        price=50,
        active=True,
    )

    compulsory_addon_cheese2 = mdl.CompulsoryAddon(
        id="double-cheese-id",
        name="double cheese",
        price=100,
        active=True,
    )

    compulsory_addon_cheese3 = mdl.CompulsoryAddon(
        id="no-cheese-id",
        name="no cheese",
        price=0,
        active=True,
    )

    compulsory_addon_category2 = mdl.CompulsoryAddonCategory(
        id="cheese-id",
        restaurant_id=restaurant.id,
        name="cheese",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
        addons=[
            compulsory_addon_cheese1,
            compulsory_addon_cheese2,
            compulsory_addon_cheese3,
        ],
    )

    item.compulsory_addon_category_ids = [
        compulsory_addon_category1.id,
        compulsory_addon_category1.id,
        compulsory_addon_category2.id,
    ]

    # item.validate()

    ordered_item_1 = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce1.id,
                compulsory_category_id=compulsory_addon_category1.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_cheese1.id,
                compulsory_category_id=compulsory_addon_category2.id,
            ),
        ],
        optional_addons=[],
    )

    ordered_item_2 = mdl.OrderItem(
        id="2",
        item_id=item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce2.id,
                compulsory_category_id=compulsory_addon_category1.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_cheese2.id,
                compulsory_category_id=compulsory_addon_category2.id,
            ),
        ],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item_1, ordered_item_2]

    ordered_item_1_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    ordered_item_2_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category1,
            compulsory_addon_category2,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={
            ordered_item_1.id: ordered_item_1_details,
            ordered_item_2.id: ordered_item_2_details,
        },
    )

    # currently this will result in an error as ordered items were required to have two sauces, but they have only 1 righnow
    with pytest.raises(
        ex.ActualAndOrderedCompulsaryAddonCategoriesMismatch,
        match="Actual and ordered compulsory addon categories mismatch",
    ):
        validator.validate_order()

    # fixing order so that it has two sauces
    ordered_item_1.compulsory_addons.append(
        mdl.OrderItemCompulsoryAddonChoice(
            compulsory_addon_id=compulsory_addon_sauce3.id,
            compulsory_category_id=compulsory_addon_category1.id,
        )
    )

    ordered_item_1_details.compulsory_addon_categories_choice.append(
        compulsory_addon_category1
    )

    ordered_item_2.compulsory_addons.append(
        mdl.OrderItemCompulsoryAddonChoice(
            compulsory_addon_id=compulsory_addon_sauce3.id,
            compulsory_category_id=compulsory_addon_category1.id,
        )
    )

    ordered_item_2_details.compulsory_addon_categories_choice.append(
        compulsory_addon_category1
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={
            ordered_item_1.id: ordered_item_1_details,
            ordered_item_2.id: ordered_item_2_details,
        },
    )

    validator.validate_order()
    order.update_status_to_validated()

    assert order.status == mdl.OrderStatus.VALIDATED


def test_calculate_amount_for_order_with_no_add_ons():
    restaurant = seed_restaurant()
    item = seed_item()
    item.price = 100
    item.compulsory_addon_category_ids = []
    # item.validate()

    ordered_item = mdl.OrderItem(
        id="1",
        item_id=item.id,  # Same as item_id
        quantity=2,
        compulsory_addons=[],
        optional_addons=[],
    )

    order = seed_order()
    order.items = [ordered_item]

    ordered_item_details = mdl.ValidateItemChoiceObject(
        item_choice=item,
        compulsory_addon_categories_choice=[],
        optional_addons_choice=[],
    )

    with pytest.raises(
        ex.OrderStatusIsNotValidated,
        match="Only validated orders can be calculate",
    ):
        calculator = mdl.OrderAmountCalculator(
            order=order,
            ordered_items_details={ordered_item.id: ordered_item_details},
        )

        calculator.calculate()

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={
            ordered_item.id: ordered_item_details,
        },
    )

    validator.validate_order()
    order.update_status_to_validated()

    calculator = mdl.OrderAmountCalculator(
        order=order,
        ordered_items_details={ordered_item.id: ordered_item_details},
    )

    total_bill = calculator.calculate()

    assert total_bill == 200


def test_large_order_validation_and_order_amount_for_order_with_addons():
    ## jj example

    restaurant = seed_restaurant()
    compulsory_addon_sauce1 = mdl.CompulsoryAddon(
        id="chipotle-id",
        name="chipotle",
        price=50,
        active=True,
    )
    compulsory_addon_sauce2 = mdl.CompulsoryAddon(
        id="atomic-id",
        name="atomic",
        price=60,
        active=True,
    )
    compulsory_addon_sauce3 = mdl.CompulsoryAddon(
        id="none-sauce-id",
        name="none",
        price=0,
        active=True,
    )
    compulsory_addon_category_sauce = mdl.CompulsoryAddonCategory(
        id="sauce-category-id",
        restaurant_id=restaurant.id,
        name="sauce",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
        addons=[
            compulsory_addon_sauce1,
            compulsory_addon_sauce2,
            compulsory_addon_sauce3,
        ],
    )

    compulsory_addon_cheese1 = mdl.CompulsoryAddon(
        id="single-cheese-id",
        name="single cheese",
        price=50,
        active=True,
    )

    compulsory_addon_cheese2 = mdl.CompulsoryAddon(
        id="double-cheese-id",
        name="double cheese",
        price=100,
        active=True,
    )

    compulsory_addon_cheese3 = mdl.CompulsoryAddon(
        id="no-cheese-id",
        name="no cheese",
        price=0,
        active=True,
    )

    compulsory_addon_category_cheese = mdl.CompulsoryAddonCategory(
        id="cheese-category-id",
        restaurant_id=restaurant.id,
        name="cheese",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
        addons=[
            compulsory_addon_cheese1,
            compulsory_addon_cheese2,
            compulsory_addon_cheese3,
        ],
    )

    additional_addon1 = mdl.OptionalAddon(
        id="coke-id",
        name="coke",
        restaurant_id=restaurant.id,
        price=100,
        active=True,
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )

    additional_addon2 = mdl.OptionalAddon(
        id="fries-id",
        name="fries",
        restaurant_id=restaurant.id,
        price=150,
        active=True,
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )

    burger_item = mdl.Item(
        id="burger-id",
        restaurant_id=restaurant.id,
        compulsory_addon_category_ids=[
            compulsory_addon_category_sauce.id,
            compulsory_addon_category_sauce.id,
            compulsory_addon_category_cheese.id,
        ],
        optional_addon_ids=[additional_addon1.id, additional_addon2.id],
        name="burger",
        price=560,
        active=True,
        timings="111111111111111111111111",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )

    wrap_item = mdl.Item(
        id="wrap-id",
        restaurant_id=restaurant.id,
        compulsory_addon_category_ids=[
            compulsory_addon_category_sauce.id,
            compulsory_addon_category_sauce.id,
            compulsory_addon_category_cheese.id,
        ],
        optional_addon_ids=[additional_addon1.id, additional_addon2.id],
        name="wrap",
        price=790,
        active=True,
        timings="111111111111111111111111",
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )

    # burger_item.validate()
    # wrap_item.validate()

    ordered_item_1 = mdl.OrderItem(
        id="1",
        item_id=burger_item.id,  # Same as item_id
        quantity=2,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce1.id,
                compulsory_category_id=compulsory_addon_category_sauce.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce3.id,
                compulsory_category_id=compulsory_addon_category_sauce.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_cheese2.id,
                compulsory_category_id=compulsory_addon_category_cheese.id,
            ),
        ],
        optional_addons=[
            mdl.OrderItemOptionalAddon(
                optional_addon_id=additional_addon1.id,
                quantity=2,
            ),
            mdl.OrderItemOptionalAddon(
                optional_addon_id=additional_addon2.id,
                quantity=1,
            ),
        ],
    )

    ordered_item_1_amount = (
        burger_item.price
        + compulsory_addon_sauce1.price
        + compulsory_addon_sauce3.price
        + compulsory_addon_cheese2.price
        + (additional_addon1.price * 2)
        + (additional_addon2.price * 1)
    ) * 2

    ordered_item_2 = mdl.OrderItem(
        id="2",
        item_id=wrap_item.id,  # Same as item_id
        quantity=3,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce1.id,
                compulsory_category_id=compulsory_addon_category_sauce.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce2.id,
                compulsory_category_id=compulsory_addon_category_sauce.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_cheese3.id,
                compulsory_category_id=compulsory_addon_category_cheese.id,
            ),
        ],
        optional_addons=[
            mdl.OrderItemOptionalAddon(
                optional_addon_id=additional_addon1.id,
                quantity=1,
            ),
        ],
    )

    ordered_item_2_amount = (
        wrap_item.price
        + compulsory_addon_sauce1.price
        + compulsory_addon_sauce2.price
        + compulsory_addon_cheese3.price
        + (additional_addon1.price * 1)
    ) * 3

    ordered_item_3 = mdl.OrderItem(
        id="3",
        item_id=wrap_item.id,  # Same as item_id
        quantity=1,
        compulsory_addons=[
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce3.id,
                compulsory_category_id=compulsory_addon_category_sauce.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_sauce3.id,
                compulsory_category_id=compulsory_addon_category_sauce.id,
            ),
            mdl.OrderItemCompulsoryAddonChoice(
                compulsory_addon_id=compulsory_addon_cheese3.id,
                compulsory_category_id=compulsory_addon_category_cheese.id,
            ),
        ],
        optional_addons=[],
    )

    ordered_item_3_amount = (
        wrap_item.price
        + compulsory_addon_sauce3.price
        + compulsory_addon_sauce3.price
        + compulsory_addon_cheese3.price
    ) * 1

    order = seed_order()
    order.items = [ordered_item_1, ordered_item_2, ordered_item_3]

    ordered_item_1_details = mdl.ValidateItemChoiceObject(
        item_choice=burger_item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category_sauce,
            compulsory_addon_category_sauce,
            compulsory_addon_category_cheese,
        ],
        optional_addons_choice=[additional_addon1, additional_addon2],
    )

    ordered_item_2_details = mdl.ValidateItemChoiceObject(
        item_choice=wrap_item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category_sauce,
            compulsory_addon_category_sauce,
            compulsory_addon_category_cheese,
        ],
        optional_addons_choice=[additional_addon1],
    )

    ordered_item_3_details = mdl.ValidateItemChoiceObject(
        item_choice=wrap_item,
        compulsory_addon_categories_choice=[
            compulsory_addon_category_sauce,
            compulsory_addon_category_sauce,
            compulsory_addon_category_cheese,
        ],
        optional_addons_choice=[],
    )

    validator = mdl.OrderValidator(
        order=order,
        restaurant=restaurant,
        ordered_items_details={
            ordered_item_1.id: ordered_item_1_details,
            ordered_item_2.id: ordered_item_2_details,
            ordered_item_3.id: ordered_item_3_details,
        },
    )

    validator.validate_order()
    order.update_status_to_validated()

    assert order.status == mdl.OrderStatus.VALIDATED

    calculator = mdl.OrderAmountCalculator(
        order=order,
        ordered_items_details={
            ordered_item_1.id: ordered_item_1_details,
            ordered_item_2.id: ordered_item_2_details,
            ordered_item_3.id: ordered_item_3_details,
        },
    )

    total_bill = calculator.calculate()

    assert total_bill == (
        ordered_item_1_amount + ordered_item_2_amount + ordered_item_3_amount
    )


# def test_validate_order_more_than_one_compulsory_addon_selected():
#     restaurant = seed_restaurant()
#     order = seed_order()
#     menu = seed_menu()
#     vv = OrderValidator(menu=menu)

#     extra_addon = order.items[0].compulsory_addons[0]
#     order.items[0].compulsory_addons.append(extra_addon)
#     with pytest.raises(MultipleCompulsoryAddonsSelected, match="multiple compulsory addons of a category selected, please select one"):
#         vv.OrderValidator(order=order, menu=menu)


# def test_validate_order_no_compulsory_addon_selected():
#     restaurant = seed_restaurant()
#     order = seed_order()
#     menu = seed_menu()
#     vv = OrderValidator(menu=menu)

#     order.items[0].compulsory_addons = []
#     with pytest.raises(SomeException, match="No Compulsory Addons of a category Selected, please select one"):
#         OrderValidator(order=order, menu=menu)


# def test_validate_order_invalid_optional_addon():
#     restaurant = seed_restaurant()
#     order = seed_order()
#     menu = seed_menu()
#     vv = OrderValidator(menu=menu)

#     invalid_optional_addon = order.optional_addons[0]
#     invalid_optional_addon.id = "another_store's_optional_addon_id"
#     with pytest.raises(ItemNotFoundException, match="Optional Addon not found in menu"):
#         OrderValidator(order=order, menu=menu)


# def test_validate_order_invalid_compulsory_addon():
#     restaurant = seed_restaurant()
#     order = seed_order()
#     menu = seed_menu()
#     vv = OrderValidator(menu=menu)

#     invalid_compulsory_addon = order.items[0].compulsory_addons[0]
#     invalid_compulsory_addon.id = "another_store's_item's_compulsory_addon_id"

#     with pytest.raises(ItemNotFoundException, match="Compulsory Addon not found in menu"):
#         OrderValidator(order=order, menu=menu)


# def test_place_order():
#     restaurant = seed_restaurant()
#     order = seed_order()
#     menu = seed_menu()

#     order.place_order(id="asdsadas")

#     pass


# def test_accept_order():
#     pass


# def test_reject_order():
#     pass
