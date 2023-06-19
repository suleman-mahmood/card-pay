# referral_roll_number: Optional[str] = None

"""marketing microservices domain model"""
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from .exceptions import InactiveDealException
from typing import List

@dataclass(frozen = True)
class Deal_status(str, Enum):
    """Value Object"""

    ACTIVE = 1
    INACTIVE = 2

@dataclass
class Deal():
    """Entity"""

    vendor_id : str
    name : str
    description: str = ""
    status: Deal_status = Deal_status.ACTIVE
    type: str = ""
    skus_id: List[str] = field(default_factory=list)
    discounts: List[float] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class User():
    """Entity"""

    id: str = field(default_factory=lambda: str(uuid4()))
    loyalty_points: int = 0
    number_of_transactions: int = 0
    number_of_deals_redeemed: int = 0
    cashback: int = 0
    referral_id: str = None
   
    def redeem_deal(self, deal: Deal) -> None:

        if deal.status == Deal_status.INACTIVE:
            raise InactiveDealException("Deal is inactive")
        self.number_of_deals_redeemed += 1
        loyalty_points = _calculate_loyalty_points(self.number_of_transactions, self.total_amount, self.number_of_deals_redeemed)
        self.loyalty_points = loyalty_points

    def use_reference(self,referral_id: str) -> None:
        self.referral_id = referral_id

  
        


@dataclass
class Vendor():
    """Entity"""

    deals : list[str] = field(default_factory = list)
    id: str = field(default_factory=lambda: str(uuid4()))

    def create_deal(self, name: str) -> Deal:
        """Create a deal"""
        deal = Deal(vendor_id = self.id, name = name)
        self.deals.append(deal.id)
        return deal