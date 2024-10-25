from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data='registration'),
     InlineKeyboardButton(text='Нет(', callback_data='exit')]

], resize_keyboard=True, one_time_keyboard=True)
percent_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="100%", callback_data='100')],
    [InlineKeyboardButton(text="75%", callback_data='75')],
    [InlineKeyboardButton(text="50%", callback_data='50')],
    [InlineKeyboardButton(text="25%", callback_data='25')]
], resize_keyboard=True, one_time_keyboard=True)
settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Настройки', callback_data='settings')],
    [InlineKeyboardButton(text="Профиль", callback_data='profile')]
], resize_keyboard=True, one_time_keyboard=True)
markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Найти слово'), KeyboardButton(text='Сохранить в файл')]
], resize_keyboard=True, one_time_keyboard=True)

keyboard_with_end = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Закончил')]
], resize_keyboard=True, one_time_keyboard=True)
keyboard_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Назад")]
], resize_keyboard=True, one_time_keyboard=True)


async def keywoard_markup(words):
    keyboard = InlineKeyboardBuilder()
    for word in words:
        keyboard.add(InlineKeyboardButton(text=word, callback_data='texxxt'))
    return keyboard.adjust(1).as_markup()


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поиск слова'), KeyboardButton(text='Фишки')],
    [KeyboardButton(text='Профиль'), KeyboardButton(text='Служба поддержки')],
    [KeyboardButton(text='Настройки')]

], resize_keyboard=True, one_time_keyboard=True)

find_word_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поиск слова по сообщениям')],
    [KeyboardButton(text='Поиск по фото')],
    [KeyboardButton(text='Поиск по файлам')],
    [KeyboardButton(text='Назад')]
], resize_keyboard=True, one_time_keyboard=True)

replace_word = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Замена слова в тексте")]
])
profile_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Изменить имя')],
    [KeyboardButton(text="Количество запросов")],
    [KeyboardButton(text='Подписка')]
])

settings_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Капслок")],
    [KeyboardButton(text='Ввод нескольких файлов')],
    [KeyboardButton(text='Процент совпадения')],
    [KeyboardButton(text="Назад")]
])

replace_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="первый"),KeyboardButton(text="последний"),KeyboardButton(text="все предложения со словом")],

])

fishki_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Замена текста"),KeyboardButton(text="конверт message -> txt"),KeyboardButton(text="Назад")]
])