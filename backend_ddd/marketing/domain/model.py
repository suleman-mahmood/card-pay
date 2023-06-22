# referral_roll_number: Optional[str] = None

"""marketing microservices domain model"""
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from .exceptions import InvalidReferenceException
from ...payment.domain.model import TransactionType
from typing import List, Dict

class CashbackType(str, Enum):
    PERCENTAGE = 1,
    ABSOLUTE = 2

@dataclass
class WeightageCashback:
    """Entity"""
    
    start_amount: int
    end_amount: int
    cashback_type: CashbackType
    cashback_value: float

class WeightageType(TransactionType):
    


@dataclass
class Weightage:
    """Entity"""
    id:int = 1
    weightage_payment_gateway: int = 0.1 
    weightage_p2p_push: int = 2
    weightage_p2p_pull: int = 3
    weightage_referral: int = 0.1
    weightage_cashback: List[WeightageCashback] = field(default_factory=list)

    def change_weightage(self, weightage_type: str, amount: int):
        if weightage_type == "PAYMENT_GATEWAY":
            self.weightage_payment_gateway = amount
        elif weightage_type == "P2P_PUSH":
            self.weightage_p2p_push = amount
        elif weightage_type == "P2P_PULL":
            self.weightage_p2p_pull = amount
        elif weightage_type == "REFERRAL":
            self.weightage_referral = amount
        else:
            raise Exception("Invalid weightage type")
    
    def change_cashback_weightage(self, weightage_cashback:Dict[int, float]):
        self.weightage_cashback = weightage_cashback

    
@dataclass
class User():
    """Entity"""
    id: str
    loyalty_points: int = 0
    referral_id: str = ""

    def use_reference(self, referral_id: str):
        if self.referral_id :
            raise InvalidReferenceException(
                "User has already been referred"
            )
        if self.id == referral_id:
            raise InvalidReferenceException(
                "User cannot refer themselves"
            )

        self.referral_id = referral_id

    def add_loyalty_points(self, loyalty_type: str, amount: int, weightage: Weightage):
        
        if loyalty_type == "PAYMENT_GATEWAY":
            self.loyalty_points += amount * weightage.weightage_payment_gateway

        elif loyalty_type == "P2P_PUSH":
            self.loyalty_points += amount * weightage.weightage_p2p_push

        elif loyalty_type == "P2P_PULL":
            self.loyalty_points += amount * weightage.weightage_p2p_pull
    
    def add_referral_loyalty_points(self, weightage: Weightage):
        self.loyalty_points += weightage.weightage_referral

    def calculate_cashback(self, deposit_amount: int, weightage: Weightage) -> float:
        
        weightage_cashback = weightage.weightage_cashback
        slabs = list(weightage_cashback.keys())
        slab = slabs[-1]
        for i in range(len(slabs)):
            if deposit_amount >= slabs[i]:
                continue
            else:
                slab = slabs[i-1]
                break
                    
        if weightage_cashback[slab] <= 1:
            return deposit_amount * weightage_cashback[slab]
        else:
            return weightage_cashback[slab]
