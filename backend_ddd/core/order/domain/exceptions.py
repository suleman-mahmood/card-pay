class MissingTimingsValues(Exception):
    """Missing timings values exception"""


class InvalidTimingsValue(Exception):
    """Invalid timings value exception"""


class RestaurantAlreadyActive(Exception):
    """Restaurant already active exception"""


class RestaurantAlreadyInactive(Exception):
    """Restaurant already inactive exception"""


class NoCompulsoryAddons(Exception):
    """No compulsory addons exception"""


class NegativeCompulsoryAddonPrice(Exception):
    """Negative compulsory addon price exception"""

class AllCompulsoryAddonsInactive(Exception):
    """All compulsory addons inactive exception"""


class NegativeOptionalAddonPrice(Exception):
    """Negative optional addon price exception"""


class OptionalAddonAlreadyActive(Exception):
    """Optional addon already active exception"""


class OptionalAddonAlreadyInactive(Exception):
    """Optional addon already inactive exception"""


class InvalidItemPrice(Exception):
    """Invalid item price exception"""


class ItemAlreadyActive(Exception):
    """Item already active exception"""

class ItemAlreadyInactive(Exception):
    """Item already inactive exception"""

class OrderStatusIsNotPending(Exception):
    """Order status is not pending exception"""

class OrderStatusIsNotValidated(Exception):
    """Order status is not validated exception"""

class OrderStatusIsNotAccepted(Exception):
    """Order status is not accepted exception"""

class OrderRestaurantMismatch(Exception):
    """Order restaurant mismatch exception"""

class NoItemsProvided(Exception):
    """No items provided exception"""

class RestaurantInactive(Exception):
    """Restaurant inactive exception"""  

class RestaurantClosed(Exception):
    """Restaurant closed exception"""

class OrderedItemDetailsNotPassed(Exception):
    """Ordered item details not passed exception"""

class ItemRestaurantMismatch(Exception):
    """Item restaurant mismatch exception"""

class ItemInactive(Exception):
    """Item inactive exception"""

class ItemNotAvailable(Exception):
    """Item not available exception"""

class OptionalAddonRestaurantMismatch(Exception):
    """Optional addon restaurant mismatch exception"""

class OptionalAddonInactive(Exception):
    """Optional addon inactive exception"""

class CompulsoryAddonCategoryMismatch(Exception):
    """Compulsory addon category mismatch exception"""

class InvalidCompulsoryAddonsSelected(Exception):
    """Invalid compulsory addons selected exception"""

class CompulsoryAddonCategoryAndRestaurantMismatch(Exception):
    """Compulsory addon category restaurant mismatch exception"""

class CompulsoryAddonNotFound(Exception):
    """Compulsory addon not found exception"""

class CompulsoryAddonInactive(Exception):
    """Compulsory addon inactive exception"""

class IncorrectNumberOfItemsPassed(Exception):
    """Incorrect number of items passed exception"""

class IncorrectCompulsoryAddonCategoriesPassedForValidation(Exception):
    """Incorrect categories passed for validation exception"""

class ItemAndOrderItemCompulsaryAddonCategoryMismatch(Exception):
    """Item and order item compulsory addon category mismatch exception"""

class OrderAndPassedCompulsaryAddonCategoriesMismatch(Exception):
    """Order and passed compulsory addon categories mismatch exception"""

class ActualAndPassedCompulsaryAddonCategoriesMismatch(Exception):
    """Actual and passed compulsory addon categories mismatch exception"""

class ActualAndOrderedCompulsaryAddonCategoriesMismatch(Exception):
    """Actual and ordered compulsory addon categories mismatch exception"""

class CompulsoryAddonPriceCannotBeAbove1000(Exception):
    """Compulsory addon price cannot be above 1000 exception"""

class OptionalAddonPriceCannotBeAbove1000(Exception):
    """Optional addon price cannot be above 1000 exception"""

class ItemPriceCannotBeAbove1000(Exception):
    """Item price cannot be above 1000 exception"""

class ItemAndPassedCompulsoryAddonCategoriesMismatch(Exception):
    """Item and passed compulsory addon categories mismatch exception"""

class ItemAndPassesOptionalAddonCategoriesMismatch(Exception):
    """Item and passed optional addon categories mismatch exception"""