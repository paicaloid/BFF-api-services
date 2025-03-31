import requests
from app import models
from app.db import SessionLocal, engine
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


def main():
    models.Base.metadata.create_all(bind=engine)
    init_post()


if __name__ == "__main__":
    main()
