import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("credentials-prod.json")
firebase_admin.initialize_app(cred)

# List all users
all_users = auth.list_users()

# Delete each user
for user in all_users.users:
    try:
        auth.delete_user(user.uid)
        print(f"Deleted user: {user.uid}")
    except auth.AuthError as e:
        print(f"Error deleting user {user.uid}: {e}")
