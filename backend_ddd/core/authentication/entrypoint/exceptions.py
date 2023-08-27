class UserNotInFirestore(Exception):
    """User doesn't exist in users_firestore table"""


class WalletNotInFirestore(Exception):
    """Wallet doesn't exist in wallets_firestore table"""


class UniqueIdentifierAlreadyExistsException(Exception):
    """exception raised for when a unique identifier already exists in a particular closed loop"""
