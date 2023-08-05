from ...payment.domain.model import TransactionType, TransactionMode


def is_instant_transaction(transaction_type: TransactionType) -> bool:
    if (
        transaction_type == TransactionType.P2P_PULL
        or transaction_type == TransactionType.PAYMENT_GATEWAY
    ):
        return False

    return True
