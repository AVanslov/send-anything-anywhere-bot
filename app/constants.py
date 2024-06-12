from datetime import datetime
import json

IGNORE = 'Ignore'
NEXT_YEAR = 'Next_year'
NEXT_MONTH = 'Next_month'
PREVIOUS_YEAR = 'Previous_year'
PREVIOUS_MONTH = 'Previous_month'
YEARS = {
    str(datetime.now().year),
    str(datetime.now().year + 1),
}
MONTHS = {
    str(i) for i in range(1, 13)
}
MAIN_MENU_BUTTONS = {
    'Хочу отправить': 'want_to_send',
    'Хочу доставить': 'want_to_delivery',
    'Избранное': 'Favorite',
    'Посмотреть историю посылок': 'see_orders_history',
    'Посмотреть доступные направления': 'see_availible_routes',
    'Сделать донат': 'send_money',
    'Написать разработчику': 'contact_developer',
}

a = ord('А')
ALPHABET_RU = [chr(i) for i in range(a, a+32)]

TYPE_OF_REWARD_BUTTONS = {
    'Деньги': 'money',
    'Другое': 'other',

}
CURRENCIES = ['€', '$', '₩', '¥', 'RSD', '₽']

# получаем ключи словаря
with open("all_countries_and_cities.json", "r") as fh:
    countries_and_cities = json.load(fh)
# - получаем первую букву каждого ключа
# - формируем список
# - избавляемся от дубликатов
ALPHABET_EN = sorted(list(set(sorted(
    [i[:1] for i in countries_and_cities.keys()]
))))

COUNTRIES_RU = [
    'Абхазия',
    'Австралия',
    'Австрия',
    'Азербайджан',
    'Албания',
    'Алжир',
    'Американское Самоа',
    'Ангилья',
    'Ангола',
    'Андорра',
    'Антарктида',
    'Антигуа и Барбуда',
    'Аргентина',
    'Армения',
    'Аруба',
    'Афганистан',
    'Багамы',
    'Бангладеш',
    'Барбадос',
    'Бахрейн',
    'Беларусь',
    'Белиз',
    'Бельгия',
    'Бенин',
    'Бермуды',
    'Болгария',
    'Боливия, Многонациональное Государство',
    'Бонайре, Саба и Синт-Эстатиус',
    'Босния и Герцеговина',
    'Ботсвана',
    'Бразилия',
    'Британская территория в Индийском океане',
    'Бруней-Даруссалам',
    'Буркина-Фасо',
    'Бурунди',
    'Бутан',
    'Вануату',
    'Венгрия',
    'Венесуэла Боливарианская Республика',
    'Виргинские острова, Британские',
    'Виргинские острова, США',
    'Вьетнам',
    'Габон',
    'Гаити',
    'Гайана',
    'Гамбия',
    'Гана',
    'Гваделупа',
    'Гватемала',
    'Гвинея',
    'Гвинея-Бисау',
    'Германия',
    'Гернси',
    'Гибралтар',
    'Гондурас',
    'Гонконг',
    'Гренада',
    'Гренландия',
    'Греция',
    'Грузия',
    'Гуам',
    'Дания',
    'Джерси',
    'Джибути',
    'Доминика',
    'Доминиканская Республика',
    'Египет',
    'Замбия',
    'Западная Сахара',
    'Зимбабве',
    'Израиль',
    'Индия',
    'Индонезия',
    'Иордания',
    'Ирак',
    'Иран, Исламская Республика',
    'Ирландия',
    'Исландия',
    'Испания',
    'Италия',
    'Йемен',
    'Кабо-Верде',
    'Казахстан',
    'Камбоджа',
    'Камерун',
    'Канада',
    'Катар',
    'Кения',
    'Кипр',
    'Киргизия',
    'Кирибати',
    'Китай',
    'Кокосовые (Килинг) острова',
    'Колумбия',
    'Коморы',
    'Конго',
    'Конго, Демократическая Республика',
    'Корея, Народно-Демократическая Республика',
    'Корея, Республика',
    'Коста-Рика',
    'Кот д Ивуар',
    'Куба',
    'Кувейт',
    'Кюрасао',
    'Лаос',
    'Латвия',
    'Лесото',
    'Ливан',
    'Ливийская Арабская Джамахирия',
    'Либерия',
    'Лихтенштейн',
    'Литва',
    'Люксембург',
    'Маврикий',
    'Мавритания',
    'Мадагаскар',
    'Майотта',
    'Макао',
    'Малави',
    'Малайзия',
    'Мали',
    'Малые Тихоокеанские отдаленные острова Соединенных Штатов',
    'Мальдивы',
    'Мальта',
    'Марокко',
    'Мартиника',
    'Маршалловы острова',
    'Мексика',
    'Микронезия, Федеративные Штаты',
    'Мозамбик',
    'Молдова, Республика',
    'Монако',
    'Монголия',
    'Монтсеррат',
    'Мьянма',
    'Намибия',
    'Науру',
    'Непал',
    'Нигер',
    'Нигерия',
    'Нидерланды',
    'Никарагуа',
    'Ниуэ',
    'Новая Зеландия',
    'Новая Каледония',
    'Норвегия',
    'Объединенные Арабские Эмираты',
    'Оман',
    'Остров Буве',
    'Остров Мэн',
    'Остров Норфолк',
    'Остров Рождества',
    'Остров Херд и острова Макдональд',
    'Острова Кайман',
    'Острова Кука',
    'Острова Теркс и Кайкос',
    'Пакистан',
    'Палау',
    'Палестинская территория, оккупированная',
    'Панама',
    'Папский Престол (Государство — город Ватикан)',
    'Папуа-Новая Гвинея',
    'Парагвай',
    'Перу',
    'Питкерн',
    'Польша',
    'Португалия',
    'Пуэрто-Рико',
    'Республика Македония',
    'Реюньон',
    'Россия',
    'Руанда',
    'Румыния',
    'Самоа',
    'Сан-Марино',
    'Сан-Томе и Принсипи',
    'Саудовская Аравия',
    'Святая Елена, Остров вознесения, Тристан-да-Кунья',
    'Северные Марианские острова',
    'Сен-Бартельми',
    'Сен-Мартен',
    'Сенегал',
    'Сент-Винсент и Гренадины',
    'Сент-Китс и Невис',
    'Сент-Люсия',
    'Сент-Пьер и Микелон',
    'Сербия',
    'Сейшелы',
    'Сингапур',
    'Синт-Мартен',
    'Сирийская Арабская Республика',
    'Словакия',
    'Словения',
    'Соединенное Королевство',
    'Соединенные Штаты',
    'Соломоновы острова',
    'Сомали',
    'Судан',
    'Суринам',
    'Сьерра-Леоне',
    'Таджикистан',
    'Таиланд',
    'Тайвань (Китай)',
    'Танзания, Объединенная Республика',
    'Тимор-Лесте',
    'Того',
    'Токелау',
    'Тонга',
    'Тринидад и Тобаго',
    'Тувалу',
    'Тунис',
    'Туркмения',
    'Турция',
    'Уганда',
    'Узбекистан',
    'Украина',
    'Уоллис и Футуна',
    'Уругвай',
    'Фарерские острова',
    'Фиджи',
    'Филиппины',
    'Финляндия',
    'Фолклендские острова (Мальвинские)',
    'Франция',
    'Французская Гвиана',
    'Французская Полинезия',
    'Французские Южные территории',
    'Хорватия',
    'Центрально-Африканская Республика',
    'Чад',
    'Черногория',
    'Чешская Республика',
    'Чили',
    'Швейцария',
    'Швеция',
    'Шпицберген и Ян Майен',
    'Шри-Ланка',
    'Эквадор',
    'Экваториальная Гвинея',
    'Эландские острова',
    'Эль-Сальвадор',
    'Эритрея',
    'Эсватини',
    'Эстония',
    'Эфиопия',
    'Южная Африка',
    'Южная Джорджия и Южные Сандвичевы острова',
    'Южная Осетия',
    'Южный Судан',
    'Ямайка',
    'Япония'
]
