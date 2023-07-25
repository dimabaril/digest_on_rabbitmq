import random

import requests
from loguru import logger


from config import Config, create_session
from models import Post, Subscription, Tag, User, Base


session = create_session()

logger.add("populate_database.log")


def populate_database_from_api():
    """Функция для наполнения базы данных данными из API 'newsapi.org'."""
    Base.metadata.drop_all(Config.ENGINE)
    Base.metadata.create_all(Config.ENGINE)

    # Добавим пользователей
    user1 = User(name="Alice")
    user2 = User(name="Bob")
    user3 = User(name="Charlie")
    user4 = User(name="Dave")
    user5 = User(name="Eve")

    session.add_all([user1, user2, user3, user4, user5])
    session.commit()

    # Добавим посты
    base_url = "https://newsapi.org/v2/everything/"
    params = {
        "q": "*",
        "from": "2023-07-21",
        "sortBy": "popularity",
        "apiKey": Config.NEWSAPI_KEY,
    }

    posts_objects = []
    tags_dict = {}

    try:
        response = requests.get(base_url, params=params)

        # можно попринтить или нет, вкусовщина
        # print(response.__dict__)

        response.raise_for_status()
        data = response.json()
        articles = data["articles"]

        for index, article in enumerate(articles):
            title = article["title"]
            content = article["content"]
            popularity = (
                100 - index
            )  # популярности в чистом виде у нас нет, в ответе приетает 100 постов отсортированных по популярности, для примера вернём популярность от 100 до 1, но эт конечно не так )
            tag_name = article["source"]["name"]

            tag = tags_dict.get(tag_name)

            if not tag:
                tag = Tag(name=tag_name)
                tags_dict[tag_name] = tag

            post = Post(title=title, content=content, popularity=popularity)

            post.tags.append(tag)
            posts_objects.append(post)

        session.add_all(posts_objects)
        session.commit()

    except requests.RequestException as error:
        logger.exception(
            "Произошла ошибка при выполнении запроса:",
            error,
        )
    except Exception as error:
        logger.exception(
            "Ой, неизвестная ошибка:",
            error,
        )

    # Добавим подписки, рандомно
    users = session.query(User).all()
    tags = session.query(Tag).all()
    subscriptions_objects = []

    for user in users:
        for tag in tags:
            if random.randint(0, 1):
                subscription = Subscription(user_id=user.id, tag_id=tag.id)
                subscriptions_objects.append(subscription)

    session.add_all(subscriptions_objects)
    session.commit()


if __name__ == "__main__":
    populate_database_from_api()
    logger.info("Database populated successfully.")
