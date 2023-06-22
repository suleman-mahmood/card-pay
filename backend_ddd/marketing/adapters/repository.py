from abc import ABC, abstractmethod
from ..domain.model import (
   User,
   CashbackSlab,
   Weightage,
)
from typing import List, Dict

class MarkteingUserAbstractRepository(ABC):

    @abstractmethod
    def get(self, id: str) -> User:
        pass
    
    @abstractmethod
    def save(self, user: User):
        pass
    
class FakeMarketingUserRepository():

    def __init__(self):
        self.users: Dict[str, User] = {}
    
    def get(self, id: str) -> User:
        return self.users[id]
    
    def save(self, user: User):
        self.users[user.id] = user

class MarketingUserRepository():

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    
    def get(self, id: str) -> User:
        sql = """
            select id, loyalty_points, referral_id, is_phone_number_verified
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
            user_verified=row[3],
        )

    def save(self, user: User):
        sql = """
            insert into users (id, loyalty_points, referral_id, is_phone_number_verified)
            values (%s, %s, %s, %s)
            on conflict (id) do update
            set loyalty_points = %s,
            referral_id = %s,
            is_phone_number_verified = %s
        """
        self.cursor.execute(
            sql,
            [
                user.id,
                user.loyalty_points,
                user.referral_id,
                user.user_verified
            ]
        )




