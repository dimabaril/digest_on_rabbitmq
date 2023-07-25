from config import create_session
from models import Digest, Post, Subscription, Tag

session = create_session()


def generate_digest(user):
    popular_posts = (
        session.query(Post)
        .join(Post.tags)
        .join(Tag.subscriptions)
        .filter(Subscription.user_id == user)
        .filter(Post.popularity >= 50)
        .all()
    )

    # Создание дайджеста
    digest = Digest(user_id=user)
    session.add(digest)
    session.commit()

    # Добавление отобранных постов в дайджест
    # digest.posts.extend(popular_posts)
    for post in popular_posts:
        digest.posts.append(post)

    session.commit()

    # Формируем данные для ответа
    digest_data = {
        "digest_id": digest.id,
        "user_id": user,
        # "user_name": user.name,
        "posts": [],
    }

    for post in digest.posts:
        post_data = {
            "post_id": post.id,
            "content": post.content,
            "popularity": post.popularity,
            "tags": [tag.name for tag in post.tags],
        }

        digest_data["posts"].append(post_data)

    return digest_data
