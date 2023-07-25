from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.name}>"


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tag {self.name}>"


class Subscription(Base):
    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=False)
    user = relationship("User", backref="subscriptions")
    tag = relationship("Tag", backref="subscriptions")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Subscription {self.user_id} - {self.tag_id}>"


# Промежуточная таблица для связи постов и тегов, тег в текущем исполнении по сути источник новостей и в данном случае многие ко многим не требуется, но изначально тег задумался как тег, пока оставлю так.
post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False, default="")
    popularity = Column(
        Integer,
        nullable=False,
    )
    tags = relationship("Tag", secondary="post_tag", backref="posts")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post {self.id} - {self.title}>"


digest_post = Table(
    "digest_post",
    Base.metadata,
    Column("digest_id", Integer, ForeignKey("digest.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("post.id"), primary_key=True),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
)


class Digest(Base):
    __tablename__ = "digest"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="digests")
    posts = relationship("Post", secondary=digest_post, backref="digests")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Digest {self.id}>"
