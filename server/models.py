from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    age = Column(Integer)
    email = Column(String(200), unique=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    hobbies = relationship("Hobby", secondary='user_hobbies', backref="users")

class Hobby(Base):
    __tablename__ = 'hobbies'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(Text)
    popularity = Column(Integer)
    cost = Column(Integer)
    tags = relationship("Tag", secondary='hobby_tags', backref="hobbies")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(Text)

user_hobbies_association = Table('user_hobbies', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('hobby_id', Integer, ForeignKey('hobbies.id'))
)

hobby_tags_association = Table('hobby_tags', Base.metadata,
    Column('hobby_id', Integer, ForeignKey('hobbies.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)