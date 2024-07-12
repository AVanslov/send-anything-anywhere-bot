from datetime import datetime

from app.database.models import async_session
from app.database.models import User, SenderAdd, CarrierAdd
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_sender_add(
    tg_id,
    delivery_date,
    departure_country,
    departure_city,
    departure_details,
    arrival_country,
    arrival_city,
    arrival_details,
    type_of_reward,
    type_of_reward_currency,
    type_of_reward_value,
    type_of_reward_message,
    size,
    weight,
    cargo_type,
    transport,
):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        sender_add = await session.scalar(select(SenderAdd).where(SenderAdd.user == user.id))

        if not sender_add:
            session.add(
                SenderAdd(
                    user=user.id,
                    publish_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    delivery_date=delivery_date.strftime("%m/%d/%Y, %H:%M:%S"),
                    departure_country=departure_country,
                    departure_city=departure_city,
                    departure_details=departure_details,
                    arrival_country=arrival_country,
                    arrival_city=arrival_city,
                    arrival_details=arrival_details,
                    type_of_reward=type_of_reward,
                    type_of_reward_currency=type_of_reward_currency,
                    type_of_reward_value=type_of_reward_value,
                    type_of_reward_message=type_of_reward_message,
                    size=size,
                    weight=weight,
                    cargo_type=cargo_type,
                    transport=transport,
                )
            )
            await session.commit()


async def set_carrier_add(
    tg_id,
    delivery_date,
    departure_country,
    departure_city,
    arrival_country,
    arrival_city,
    type_of_reward,
    type_of_reward_currency,
    type_of_reward_value,
    size,
    weight,
    cargo_type,
    transport,
):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        carrier_add = await session.scalar(select(CarrierAdd).where(CarrierAdd.user == user.id))

        if not carrier_add:
            session.add(
                CarrierAdd(
                    user=user.id,
                    publish_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    delivery_date=delivery_date.strftime("%m/%d/%Y, %H:%M:%S"),
                    departure_country=departure_country,
                    departure_city=departure_city,
                    arrival_country=arrival_country,
                    arrival_city=arrival_city,
                    type_of_reward=type_of_reward,
                    type_of_reward_currency=type_of_reward_currency,
                    type_of_reward_value=type_of_reward_value,
                    size=size,
                    weight=weight,
                    cargo_type=cargo_type,
                    transport=transport,
                )
            )
            await session.commit()


async def get_carrier_add_items():
    async with async_session() as session:
        return await session.scalars(select(CarrierAdd))


async def get_sender_add_items():
    async with async_session() as session:
        return await session.scalars(select(SenderAdd))
