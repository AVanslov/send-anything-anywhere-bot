from aiogram.fsm.state import State, StatesGroup


class SendersData(StatesGroup):
    delivery_date = State()
    departure_country = State()
    departure_city = State()
    arrival_country = State()
    arrival_city = State()
    type_of_reward = State()
    size = State()
    weight = State()
    cargo_type = State()
    transport = State()
