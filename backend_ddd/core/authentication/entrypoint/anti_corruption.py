import firebase_admin

from firebase_admin import auth

from dataclasses import dataclass
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.entrypoint import queries as pmt_qry
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.entrypoint import exceptions as auth_cmd_ex
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
    def firebase_create_user(
        self, phone_email: str, phone_number: str, password: str, full_name: str
    ) -> str:
        pass

    @abstractmethod
    def firebase_update_password(
        self, firebase_uid: str, new_password: str, new_full_name: str
    ):
        pass

    @abstractmethod
    def firebase_get_user(self, email: str) -> str:
        pass


@dataclass
class FakeFirebaseService(AbstractFirebaseService):
    def firebase_create_user(
        self, phone_email: str, phone_number: str, password: str, full_name: str
    ) -> str:
        return ""

    def firebase_update_password(
        self, firebase_uid: str, new_password: str, new_full_name: str
    ):
        pass

    def firebase_get_user(self, email: str) -> str:
        return ""


class FirebaseService(AbstractFirebaseService):
    def firebase_create_user(
        self, phone_email: str, phone_number: str, password: str, full_name: str
    ) -> str:
        user_record = firebase_admin.auth.create_user(
            email=phone_email,
            email_verified=False,
            phone_number=phone_number,
            password=password,
            display_name=full_name,
            disabled=False,
        )

        return user_record.uid

    def firebase_update_password(
        self, firebase_uid: str, new_password: str, new_full_name: str
    ):
        firebase_admin.auth.update_user(
            uid=firebase_uid,
            password=new_password,
            display_name=new_full_name,
        )

    def firebase_get_user(self, email: str) -> str:
        user_record = auth.get_user_by_email(email=email)

        return user_record.uid
