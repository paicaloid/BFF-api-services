import requests
from app.db import SessionLocal
from app.models import Post


def init_post():
    db = SessionLocal()

    # Check if the database is empty
    if db.query(Post).count() > 0:
        print("Database already initialized with posts.")
        return

    # Fetch posts from the API
    res = requests.get("https://jsonplaceholder.typicode.com/posts")
    if res.status_code == 200:
        posts = res.json()
        for post in posts:
            post_in = Post(
                id=post["id"],
                title=post["title"],
                body=post["body"],
                userId=post["userId"],
            )
            db.add(post_in)
        db.commit()
        db.close()
    else:
        raise Exception("Failed to fetch posts from API", res.status_code)
