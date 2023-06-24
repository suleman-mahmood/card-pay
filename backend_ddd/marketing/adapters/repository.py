from abc import ABC, abstractmethod
from ..domain.model import (
   User,
   CashbackSlab,
   CashbackType,
   Weightage,
)
from ...payment.domain.model import TransactionType

from typing import List, Dict

class MarkteingUserAbstractRepository(ABC):

    @abstractmethod
    def get(self, id: str) -> User:
        pass
    
    @abstractmethod
    def save(self, user: User):
        pass
    
class FakeMarketingUserRepository(MarkteingUserAbstractRepository):

    def __init__(self):
        self.users: Dict[str, User] = {}
    
    def get(self, id: str) -> User:
        return self.users[id]
    
    def save(self, user: User):
        self.users[user.id] = user

class MarketingUserRepository(MarkteingUserAbstractRepository):

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    
    def get(self, id: str) -> User:
        sql = """
            select id, loyalty_points, referral_id, marketing_user_verified
            from users
            where id = %s
        """
        self.cursor.execute(
            sql,
            [
                 id
            ]
        )

        row = self.cursor.fetchone()

        return User(
            id=row[0],
            loyalty_points=row[1],
            referral_id=row[2],
            marketing_user_verified=row[3],
        )

    def save(self, user: User):
        sql = """
            update users
            set loyalty_points = %s,
            referral_id = %s,
            marketing_user_verified = %s
            where id = %s
        """
        # Here users is the same table as in authentication microservice

        self.cursor.execute(
            sql,
            [
                user.loyalty_points,
                user.referral_id,
                user.marketing_user_verified,
                user.id
            ]
        )

class WeightageAbstractRepository(ABC):
    
    @abstractmethod
    def get(self, id: str) -> Weightage:
        pass
    
    @abstractmethod
    def save(self, weightage: Weightage):
        pass

class FakeWeightageRepository(WeightageAbstractRepository):

    def __init__(self):
        self.weightages: Dict[str, Weightage] = {}
    
    def get(self, id: str) -> Weightage:
        return self.weightages[id]
    
    def save(self, weightage: Weightage):
        self.weightages[weightage.id] = weightage

class WeightageRepository(WeightageAbstractRepository):

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    
    def get(self, id: str) -> Weightage:
        sql = """
            select id, weightage_type, weightage_value
            from weightages
            where id = %s
        """
        self.cursor.execute(
            sql,
            [
                 id
            ]
        )

        row = self.cursor.fetchone()

        return Weightage(
            id=row[0],
            weightage_type=TransactionType[row[1]],
            weightage_value=row[2],
        )

    def save(self, weightage: Weightage):
        sql = """
            insert into weightages (weightage_type, weightage_value, id)
            values (%s, %s, %s)
            on conflict (id) do update
            set weightage_type = excluded.weightage_type,
            weightage_value = excluded.weightage_value,
            id = excluded.id
        """
        self.cursor.execute(
            sql,
            [
                weightage.weightage_type.name,
                weightage.weightage_value,
                weightage.id
            ]
        )

class CashbackSlabAbstractRepository(ABC):

    @abstractmethod
    def get(self, id: str) -> CashbackSlab:
        pass
    
    @abstractmethod
    def save(self, cashback_slab: CashbackSlab):
        pass

class FakeCashbackSlabRepository(CashbackSlabAbstractRepository):
    
    def __init__(self):
        self.cashback_slabs: Dict[str, CashbackSlab] = {}
    
    def get(self, id: str) -> CashbackSlab:
        return self.cashback_slabs[id]
    
    def save(self, cashback_slab: CashbackSlab):
        self.cashback_slabs[cashback_slab.id] = cashback_slab

class CashbackSlabRepository(CashbackSlabAbstractRepository):
    
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    
    def get(self, id: str) -> CashbackSlab:
        sql = """
            select start_amount, end_amount, cashback_type, cashback_value, id
            from cashback_slabs
            where id = %s
        """
        self.cursor.execute(
            sql,
            [
                id
            ]
        )

        row = self.cursor.fetchone()

        return CashbackSlab(
            start_amount=row[0],
            end_amount=row[1],
            cashback_type=CashbackType[row[2]],
            cashback_value=row[3],
            id=row[4],
        )

    def save(self, cashback_slab: CashbackSlab):

        sql = """
            insert into cashback_slabs (start_amount, end_amount, cashback_type, cashback_value, id)
            values (%s, %s, %s, %s, %s)
            on conflict (id) do update
            set start_amount = excluded.start_amount,
            end_amount = excluded.end_amount,
            cashback_type = excluded.cashback_type,
            cashback_value = excluded.cashback_value,
            id = excluded.id
        """
        self.cursor.execute(
            sql,
            [
                cashback_slab.start_amount,
                cashback_slab.end_amount,
                cashback_slab.cashback_type.name,
                cashback_slab.cashback_value,
                cashback_slab.id
            ]
        )