from core.payment.domain import model as pmt_mdl
from datetime import timedelta


def is_instant_transaction(transaction_type: pmt_mdl.TransactionType) -> bool:
    if (
        transaction_type == pmt_mdl.TransactionType.P2P_PULL
        or transaction_type == pmt_mdl.TransactionType.PAYMENT_GATEWAY
    ):
        return False

    return True


def get_min_sec_repr_of_timedelta(td: timedelta):
    total_seconds = int(td.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes}:{seconds:02d}"
