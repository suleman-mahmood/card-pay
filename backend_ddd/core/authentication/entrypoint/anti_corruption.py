from dataclasses import dataclass
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import queries as pmt_qry
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.entrypoint import exceptions as auth_cmd_ex
from abc import ABC, abstractmethod


@dataclass
class AbstractPaymentService(ABC):
    
    @abstractmethod
    def create_wallet(self, user_id: str, uow: AbstractUnitOfWork):
        pass

    @abstractmethod
    def execute_transaction(
        self, 
        sender_wallet_id: str,
        recipient_wallet_id: str,
        amount: int,
        transaction_mode: pmt_mdl.TransactionMode,
        transaction_type: pmt_mdl.TransactionType,
        uow: AbstractUnitOfWork,
    ):
        pass

    @abstractmethod
    def get_starred_wallet_id(self, uow: AbstractUnitOfWork)-> str:
        pass


@dataclass
class PaymentService(AbstractPaymentService):

    def create_wallet(self, user_id: str, uow: AbstractUnitOfWork):
        pmt_cmd.create_wallet(user_id, uow)

    def execute_transaction(
        self, 
        sender_wallet_id: str,
        recipient_wallet_id: str,
        amount: int,
        transaction_mode: pmt_mdl.TransactionMode,
        transaction_type: pmt_mdl.TransactionType,
        uow: AbstractUnitOfWork,
    ):
        pmt_cmd.execute_transaction(
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=recipient_wallet_id,
            amount=amount,
            transaction_mode=transaction_mode,
            transaction_type=transaction_type,
            uow=uow,
        )

    def get_starred_wallet_id(self, uow: AbstractUnitOfWork)-> str:
        return pmt_qry.get_starred_wallet_id(uow)


@dataclass
class FakePaymentService(AbstractPaymentService):

    def create_wallet(self, user_id: str, uow: AbstractUnitOfWork):
        pass

    def execute_transaction(
        self, 
        sender_wallet_id: str,
        recipient_wallet_id: str,
        amount: int,
        transaction_mode: pmt_mdl.TransactionMode,
        transaction_type: pmt_mdl.TransactionType,
        uow: AbstractUnitOfWork,
    ):
        pass

    def get_starred_wallet_id(self, uow: AbstractUnitOfWork)-> str:
        return ""

@dataclass
class AbstractAuthenticationService(ABC):
   
    @abstractmethod
    def verified_unique_identifier_already_exists(
        self,
        closed_loop_id: str,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    )-> bool:
        pass


@dataclass
class AuthenticationService(AbstractAuthenticationService):

    def verified_unique_identifier_already_exists(
        self,
        closed_loop_id: str,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    )-> bool:
        return auth_qry.verified_unique_identifier_already_exists(
            closed_loop_id=closed_loop_id,
            unique_identifier=unique_identifier,
            uow=uow,
        )


@dataclass
class FakeAuthenticationService(AbstractAuthenticationService):
    verified_unique_identifier_already_exists_attr: bool = False

    def set_verified_unique_identifier_already_exists(self, value: bool):
        self.verified_unique_identifier_already_exists_attr = value

    def verified_unique_identifier_already_exists(
        self,
        closed_loop_id: str,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    )-> bool:
        return self.verified_unique_identifier_already_exists_attr


@dataclass
class AbstractFirebaseService(ABC):

    @abstractmethod
    def user_id_from_firestore(
        self,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    )->str:
        pass

    @abstractmethod
    def wallet_balance_from_firestore(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ):
        pass

@dataclass
class FirebaseService(AbstractFirebaseService):

    def user_id_from_firestore(
        self,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    )->str:
        return auth_qry.user_id_from_firestore(
            unique_identifier=unique_identifier,
            uow=uow,
    )

    def wallet_balance_from_firestore(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ):
        return auth_qry.wallet_balance_from_firestore(
            user_id=user_id,
            uow=uow,
    )

@dataclass
class FakeFirebaseService(AbstractFirebaseService):

    def user_id_from_firestore(
        self,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    )->str:
        raise auth_cmd_ex.UserNotInFirestore("User not found")

    def wallet_balance_from_firestore(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ):
        pass