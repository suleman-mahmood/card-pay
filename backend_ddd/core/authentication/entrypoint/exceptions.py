class UserNotInFirestore(Exception):
    """User doesn't exist in users_firestore table"""


class WalletNotInFirestore(Exception):
    """Wallet doesn't exist in wallets_firestore table"""
