from dataclasses import dataclass
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.entrypoint import queries as pmt_qry
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.entrypoint import exceptions as auth_cmd_ex
from core.authentication.entrypoint import firebase_service as fb_svc
from abc import ABC, abstractmethod


@dataclass
class AbstractPaymentService(ABC):
    @abstractmethod
    def get_starred_wallet_id(self, uow: AbstractUnitOfWork) -> str:
        pass


@dataclass
class FakePaymentService(AbstractPaymentService):
    def get_starred_wallet_id(self, uow: AbstractUnitOfWork) -> str:
        return ""


@dataclass
class PaymentService(AbstractPaymentService):
    def get_starred_wallet_id(self, uow: AbstractUnitOfWork) -> str:
        return pmt_qry.get_starred_wallet_id(uow)


@dataclass
class AbstractAuthenticationService(ABC):
    @abstractmethod
    def verified_unique_identifier_already_exists(
        self,
        closed_loop_id: str,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    ) -> bool:
        pass

    @abstractmethod
    def user_id_from_firestore(
        self,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        pass

    @abstractmethod
    def wallet_balance_from_firestore(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ) -> int:
        pass


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
    ) -> bool:
        return self.verified_unique_identifier_already_exists_attr

    def user_id_from_firestore(
        self,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        raise auth_cmd_ex.UserNotInFirestore("User not found")

    def wallet_balance_from_firestore(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ) -> int:
        return 0


@dataclass
class AuthenticationService(AbstractAuthenticationService):
    def verified_unique_identifier_already_exists(
        self,
        closed_loop_id: str,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    ) -> bool:
        return auth_qry.verified_unique_identifier_already_exists(
            closed_loop_id=closed_loop_id,
            unique_identifier=unique_identifier,
            uow=uow,
        )

    def user_id_from_firestore(
        self,
        unique_identifier: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        return auth_qry.user_id_from_firestore(
            unique_identifier=unique_identifier,
            uow=uow,
        )

    def wallet_balance_from_firestore(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ) -> int:
        return auth_qry.wallet_balance_from_firestore(
            user_id=user_id,
            uow=uow,
        )


@dataclass
class AbstractFirebaseService(ABC):
    @abstractmethod
    def create_user(
        self, phone_email: str, phone_number: str, password: str, full_name: str
    ) -> str:
        pass

    @abstractmethod
    def update_password(self, firebase_uid: str, new_password: str, new_full_name: str):
        pass

    @abstractmethod
    def get_user(self, email: str) -> str:
        pass


@dataclass
class FakeFirebaseService(AbstractFirebaseService):
    user_exists: bool = False

    def set_user_exists(self, user_exists: bool):
        self.user_exists = user_exists

    def create_user(
        self, phone_email: str, phone_number: str, password: str, full_name: str
    ) -> str:
        if self.user_exists:
            raise Exception("User already exists")
        return ""

    def update_password(self, firebase_uid: str, new_password: str, new_full_name: str):
        pass

    def get_user(self, email: str) -> str:
        return ""


class FirebaseService(AbstractFirebaseService):
    def create_user(
        self, phone_email: str, phone_number: str, password: str, full_name: str
    ) -> str:
        return fb_svc.create_user(
            phone_email=phone_email,
            email_verified=False,
            phone_number=phone_number,
            password=password,
            full_name=full_name,
            disabled=False,
        )

    def update_password(self, firebase_uid: str, new_password: str, new_full_name: str):
        fb_svc.update_password(
            firebase_uid=firebase_uid,
            new_password=new_password,
            new_full_name=new_full_name,
        )

    def get_user(self, email: str) -> str:
        return fb_svc.get_user(email=email)
