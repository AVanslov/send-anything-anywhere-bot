from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

MAX_LENGTH = 100

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

# class Comments(Base):

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    # рейтинг
    # отзывы


class SenderAdd(Base):
    __tablename__ = 'sender_adds'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    publish_date = mapped_column(String(MAX_LENGTH))
    delivery_date = mapped_column(String(MAX_LENGTH))
    departure_country = mapped_column(String(MAX_LENGTH))
    departure_city = mapped_column(String(MAX_LENGTH))
    departure_details = mapped_column(String(MAX_LENGTH))
    arrival_country = mapped_column(String(MAX_LENGTH))
    arrival_city = mapped_column(String(MAX_LENGTH))
    arrival_details = mapped_column(String(MAX_LENGTH))
    type_of_reward = mapped_column(String(MAX_LENGTH))
    type_of_reward_currency = mapped_column(String(MAX_LENGTH))
    type_of_reward_value: Mapped[int] = mapped_column()
    type_of_reward_message = mapped_column(String(MAX_LENGTH))
    size = mapped_column(String(MAX_LENGTH))
    weight = mapped_column(String(MAX_LENGTH))
    cargo_type = mapped_column(String(MAX_LENGTH))
    transport = mapped_column(String(MAX_LENGTH))
    # is_favorite


class CarrierAdd(Base):
    __tablename__ = 'carrier_adds'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    publish_date = mapped_column(String(MAX_LENGTH))
    delivery_date = mapped_column(String(MAX_LENGTH))
    departure_country = mapped_column(String(MAX_LENGTH))
    departure_city = mapped_column(String(MAX_LENGTH))
    arrival_country = mapped_column(String(MAX_LENGTH))
    arrival_city = mapped_column(String(MAX_LENGTH))
    type_of_reward = mapped_column(String(MAX_LENGTH))
    type_of_reward_currency = mapped_column(String(MAX_LENGTH))
    type_of_reward_value: Mapped[int] = mapped_column()
    size = mapped_column(String(MAX_LENGTH))
    weight = mapped_column(String(MAX_LENGTH))
    cargo_type = mapped_column(String(MAX_LENGTH))
    transport = mapped_column(String(MAX_LENGTH))
    # is_favorite


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
