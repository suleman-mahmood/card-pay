from abc import ABC, abstractmethod
from ..domain.model import (
    Weightage,
    User,
)
from typing import List


class WeightageAbstractRepository(ABC):
    """Weightage Abstract Repository"""

    @abstractmethod
    def add(self, weightage: Weightage):
        pass

    @abstractmethod
    def get(self) -> Weightage:
        pass

    @abstractmethod
    def save(self, weightage: Weightage):
        pass


class FakeWeightageRepository(WeightageAbstractRepository):

    def __init__(self):
        self.weightage: Dict[]

    def add(self, weightage: Weightage):
        
        self.weightage.append(weightage)
        
        # self.weightage["weightage_payment_gateway"] = weightage.weightage_payment_gateway
        # self.weightage["weightage_p2p_push"] = weightage.weightage_p2p_push
        # self.weightage["weightage_p2p_pull"] = weightage.weightage_p2p_pull
        # self.weightage["weightage_cashback"] = weightage.weightage_cashback
        # self.weightage["weightage_referral"] = weightage.weightage_referral

    def get(self) -> Weightage:
        
        return self.weightage[0]
        
        # return Weightage(
        #     weightage_payment_gateway=self.weightage["weightage_payment_gateway"],
        #     weightage_p2p_push=self.weightage["weightage_p2p_push"],
        #     weightage_p2p_pull=self.weightage["weightage_p2p_pull"],
        #     weightage_cashback=self.weightage["weightage_cashback"],
        #     weightage_referral=self.weightage["weightage_referral"],
        # )

    def save(self, weightage: Weightage):

        self.weightage[0] = weightage
        # self.weightage["weightage_payment_gateway"] = weightage.weightage_payment_gateway
        # self.weightage["weightage_p2p_push"] = weightage.weightage_p2p_push
        # self.weightage["weightage_p2p_pull"] = weightage.weightage_p2p_pull
        # self.weightage["weightage_cashback"] = weightage.weightage_cashback
        # self.weightage["weightage_referral"] = weightage.weightage_referral


def WeightageRepository(WeightageAbstractRepository):

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, weightage: Weightage):
        """call add only once, when launching the app"""

        
        sql1 = """
            insert into weightage (weightage_payment_gateway, weightage_p2p_push, weightage_p2p_pull, weightage_cashback, weightage_referral)
            values (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql1,
            [
                weightage.weightage_payment_gateway,
                weightage.weightage_p2p_push,
                weightage.weightage_p2p_pull,
                weightage.weightage_referral,
            ]
        )
        

        for slab in list(weightage.weightage_cashback.keys()):
            sql2 = """
                insert into weightage_cashback (slab, weightage)
                values (%s, %s)
            """
            self.cursor.execute(
                sql2,
                [
                    slab,
                    weightage.weightage_cashback[slab],
                ]
            )
        
       
    def get(self) -> Weightage:

        sql = """
            select * from weightage
        """
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return Weightage(
            weightage_payment_gateway=row[0],
            weightage_p2p_push=row[1],
            weightage_p2p_pull=row[2],
            weightage_cashback=row[3],
            weightage_referral=row[4],
        )

    def save(self, weightage: Weightage):

        sql = """
            insert into weightage (weightage_payment_gateway, weightage_p2p_push, weightage_p2p_pull, weightage_cashback, weightage_referral)
            values (%s, %s, %s, %s, %s)
            on conflict (weightage_payment_gateway, weightage_p2p_push, weightage_p2p_pull, weightage_cashback, weightage_referral) do update set
            weightage_payment_gateway = excluded.weightage_payment_gateway,
            weightage_p2p_push = excluded.weightage_p2p_push,
            weightage_p2p_pull = excluded.weightage_p2p_pull,
            weightage_cashback = excluded.weightage_cashback,
            weightage_referral = excluded.weightage_referral
        """

        self.cursor.execute(
            sql,
            [
                weightage.weightage_payment_gateway,
                weightage.weightage_p2p_push,
                weightage.weightage_p2p_pull,
                weightage.weightage_cashback,
                weightage.weightage_referral,
            ]
        )


class MarketingUserAbstractRepository(ABC):
    """Weightage Abstract Repository"""

    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def get(self, user_id: str) -> User:
        pass

    @abstractmethod
    def save(self, user: User):
        pass


def FakeMarketingUserAbstractRepository(MarketingUserAbstractRepository):
    def __init__(self):
        self.users = {}

    def add(self, user: User):
        self.users[user.id] = User

    def get(self, user_id: str) -> User:
        return self.users[user_id]

    def save(self, user: User):
        self.users[user.id] = user


def MarketingUserRepository(MarketingUserAbstractRepository):

    def add(self, user: User):
        sql = """
            insert into marketing_users (id, loyality_points, referral_id)
            values (%s,%s,%s)
        """
        self.cursor.execute(
            sql,
            [
                user.id,
                user.loyality_points,
                user.referral_id,
            ]
        )

    def get(self, user_id: str) -> User:
        sql = """
            select * from marketing_users where id = %s
        """
        self.cursor.execute(sql, [user_id])
        row = self.cursor.fetchone()
        return User(
            id=row[0],
            loyality_points=row[1],
            referral_id=row[2],
        )

    def save(self, user: User):
        sql = """
            insert into marketing_users (id, loyality_points, referral_id)
            values (%s,%s,%s)
            on conflict (id) do update set
            id = excluded.id,
            loyality_points = excluded.loyality_points = excluded,
            referral_id = excluded.referral_id
        """

        self.cursor.execute(
            sql,
            [
                user.id,
                user.loyality_points,
                user.referral_id,
            ]
        )
