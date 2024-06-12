from aiogram.fsm.state import State, StatesGroup


class SendersData(StatesGroup):
    delivery_date_year = State()
    delivery_date_month = State()
    delivery_date = State()
    departure_country_letter = State()
    departure_country = State()
    departure_city_letter = State()
    departure_city = State()
    departure_details = State()
    arrival_country_letter = State()
    arrival_country = State()
    arrival_city = State()
    arrival_details = State()  # new
    type_of_reward = State()
    type_of_reward_currency = State()
    type_of_reward_value = State()
    type_of_reward_message = State()
    size = State()
    weight = State()
    cargo_type = State()
    transport = State()
