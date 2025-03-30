import requests
from app.db import SessionLocal
from app.models import User


def init_user():
    db = SessionLocal()

    # Check if the database is empty
    if db.query(User).count() > 0:
        print("Database already initialized with users.")
        return

    # Fetch users from the API
    res = requests.get("https://jsonplaceholder.typicode.com/users")
    if res.status_code == 200:
        users = res.json()
        for user in users:
            user_in = User(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                email=user["email"],
            )
            db.add(user_in)
        db.commit()
        db.close()
    else:
        raise Exception("Failed to fetch users from API", res.status_code)
