import time

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app import keyboards as kb
from library_poisk import Search_word
from aiogram import types
import os

router = Router()

keyboards_main = {
    'Поиск слова': kb.main_keyboard,
    'search_menu': kb.find_word_keyboard,
    "Поиск слова по сообщениям": kb.find_word_keyboard
}


class Txt(StatesGroup):
    txt_rout = State()


class Replace_text(StatesGroup):
    word = State()
    new_word = State()
    text = State()
    text_ind = State()


class States(StatesGroup):
    name = State()


class Search_File(StatesGroup):
    word = State()
    file = State()


class Search_Photo(StatesGroup):
    word = State()
    photo = State()


class Search(StatesGroup):
    word = State()
    any_message = State()


class Settings(StatesGroup):
    caps = State()
    multiply_files = State()

class Support(StatesGroup):
    name = State()
    text = State()
messages = []
caps = ['off']
more_files = ['off']
percent_word = [0]
menu_word = ['']


def find_people_in_db(user_id):
    with open('db/db.txt', 'r+', encoding='utf-8') as file:
        res = file.readlines()
        for i in res:
            if user_id in i:
                return True
        return False


@router.message(CommandStart())
async def start(message: Message):
    res = find_people_in_db(str(message.from_user.username))
    if res:
        await message.answer(f"Добрый день", reply_markup=kb.main_keyboard)
    else:
        await message.answer(
            f"Добрый день {message.from_user.username}, если хотите продолжить то пройдите регистрацию",
            reply_markup=kb.start_keyboard)


@router.callback_query(F.data == 'registration')
async def router_registr(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'Введите свое имя', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(States.name)


@router.message(States.name)
async def router_state_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer("Поздравляю вы прошли регистрацию")
    await state.clear()
    with open(f"db/db.txt", 'a+', encoding='utf-8') as file:
        file.write(f"{message.from_user.username} {data['name']}\n")
        file.close()
    await message.answer(f"Имя {data['name']}", reply_markup=kb.main_keyboard)





@router.message(F.text == "Назад")
async def back(message: Message, state: FSMContext):
    global menu_word
    await message.answer('Назад', reply_markup=kb.main_keyboard)


###### Поиск слова ########

@router.message(F.text == 'Поиск слова')
async def find_word(message: Message, state: FSMContext):
    global menu_word
    menu_word[0] = "Поиск слова"
    await message.answer("Вы в меню 'Поиск слова'", reply_markup=kb.find_word_keyboard)


@router.message(F.text == 'Поиск слова по сообщениям')
async def send_emails(message: Message, state: FSMContext):
    global messages, menu_word
    messages = []
    menu_word[0] = "Поиск слова по сообщениям"
    await message.answer('Введите сообщение для поиска', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Search.word)


@router.message(Search.word)
async def search_word(message: Message, state: FSMContext):
    data = await state.update_data(word=message.text)
    await message.answer('Введите текст для поиска', reply_markup=kb.keyboard_with_end)
    await state.set_state(Search.any_message)


@router.message(Search.any_message)
async def collection_messages(message: Message, state: FSMContext):
    global messages, more_files, percent_word

    if more_files[0] == 'on':
        if percent_word[0] != 0:
            percent = percent_word[0]
        else:
            percent = 100
        messages.append(message.text)
        if message.text == 'Закончил':
            data = await state.update_data(any_message=messages)
            full_states = await state.get_data()
            result = Search_word.find_word_for_percent(full_states['word'], full_states['any_message'], percent=percent,
                                                       register=True)

            await message.answer(f"Вот ваши сообщения: ", reply_markup=await kb.keywoard_markup(result))
            await message.answer("Поиск закончен", reply_markup=kb.find_word_keyboard)
            await state.clear()
    else:
        if percent_word[0] != 0:
            percent = percent_word[0]
        else:
            percent = 100
        data = await state.update_data(any_message=message.text)
        full_states = await state.get_data()
        result = Search_word.find_word_for_percent(full_states['word'], [data['any_message']], percent=percent,
                                                   register=False)
        await message.answer(f"Вот ваши сообщения: ", reply_markup=await kb.keywoard_markup(result))
        await message.answer("Поиск закончен", reply_markup=kb.find_word_keyboard)
        await state.clear()


@router.message(F.text == 'Поиск по файлам')
async def find_file(message: Message, state: FSMContext):
    global messages
    messages = []
    await message.answer('Введите слово для поиска', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Search_File.word)


@router.message(Search_File.word)
async def word_files(message: Message, state: FSMContext):
    data = await state.update_data(word=message.text)

    if more_files[0] == 'on':
        await message.answer('Введите файлы для поиска', reply_markup=kb.keyboard_with_end)
    else:
        await message.answer('Введите файл для поиска', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Search_File.file)


@router.message(Search_File.file)
async def accept_files(message: Message, state: FSMContext):
    global messages, more_files

    name_file = message.document
    if more_files[0] == 'on':
        if message.text == 'Закончил':

            data = await state.update_data(text=messages)
            full_states = await state.get_data()
            result = Search_word.find_for_file_txt(full_states['word'], data['text'])
            await message.answer(f'Обработка файла закончена', reply_markup=await kb.keywoard_markup(result))
            await message.answer("Меню", reply_markup=kb.main_keyboard)
            await state.clear()
        elif str(name_file.file_name).endswith('.txt'):
            directory_path = 'file'
            file_name = message.from_user.username
            file_path = os.path.join(directory_path, file_name)
            if not os.path.isdir(file_path):
                os.makedirs(os.path.join(directory_path, file_name))
            all_path = f"file/{message.from_user.username}/{message.document.file_name}"
            messages.append(all_path)
            v = open(all_path, 'w', encoding='utf-8')
            await message.bot.download(name_file, all_path)

        else:
            await message.answer("Вы ввели некоректный файл", reply_markup=types.ReplyKeyboardRemove())
    else:
        if str(name_file.file_name).endswith('.txt'):
            directory_path = 'file'
            file_name = message.from_user.username
            file_path = os.path.join(directory_path, file_name)
            if not os.path.isdir(file_path):
                os.makedirs(os.path.join(directory_path, file_name))
            all_path = f"file/{message.from_user.username}/{message.document.file_name}"
            messages.append(all_path)
            v = open(all_path, 'w', encoding='utf-8')
            await message.bot.download(name_file, all_path)
            data = await state.update_data(text=messages)
            full_states = await state.get_data()
            result = Search_word.find_for_file_txt(full_states['word'], data['text'])
            await message.answer(f'Обработка файла закончена', reply_markup=await kb.keywoard_markup(result))
            await message.answer("Меню", reply_markup=kb.main_keyboard)
            time.sleep(1)

            await state.clear()


@router.message(F.text == "Поиск по фото")
async def find_photo(message: Message, state: FSMContext):
    global messages
    messages = []
    await message.answer("Введите любое текста", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Search_Photo.word)


@router.message(Search_Photo.word)
async def word_photo(message: Message, state: FSMContext):
    data = await state.update_data(word=message.text)
    if more_files[0] == 'on':
        await message.answer('Введите фото для поиска', reply_markup=kb.keyboard_with_end)
    else:
        await message.answer('Введите фото для поиска', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Search_Photo.photo)


@router.message(Search_Photo.photo)
async def accept_photo(message: Message, state: FSMContext):
    global messages

    if more_files[0] == 'on':
        if message.text == 'Закончил':
            data = await state.update_data(photo=messages)
            full_states = await state.get_data()
            res = Search_word.find_for_photo(full_states['photo'], full_states['word'])
            if len(res)>1:
                list_res = []
                for i in res:
                    for j in i:
                        list_res.append(j)
                await message.answer(f'бот считал текст с фото и готов вывести его', reply_markup=await kb.keywoard_markup(list_res))
                await message.answer('Меню',reply_markup=kb.main_keyboard)

                await state.clear()
            else:
                await message.answer(f'бот считал текст с фото и готов вывести его', reply_markup=await kb.keywoard_markup(*res))
                await message.answer('Меню',reply_markup=kb.main_keyboard)
                await state.clear()

        else:
            directory_path = 'file'
            file_name = message.from_user.username
            file_path = os.path.join(directory_path, file_name)
            if not os.path.isdir(file_path):
                os.makedirs(os.path.join(directory_path, file_name))
            all_path = f"file/{message.from_user.username}/{message.photo[-1].file_id}.jpg"
            messages.append(all_path)
            file = await message.bot.get_file(message.photo[-1].file_id)
            await message.bot.download_file(file.file_path, all_path)
    else:
        directory_path = 'file'
        file_name = message.from_user.username
        file_path = os.path.join(directory_path, file_name)
        if not os.path.isdir(file_path):
            os.makedirs(os.path.join(directory_path, file_name))
        all_path = f"file/{message.from_user.username}/photo-1.jpg"
        data = await state.update_data(photo=all_path)
        full_states = await state.get_data()
        file = await message.bot.get_file(message.photo[-1].file_id)
        await message.bot.download_file(file.file_path, all_path)
        res = Search_word.find_for_photo([all_path], full_states['word'])
        if res:
            await message.answer("бот считал текст с фото и готов вывести его",
                                 reply_markup=await kb.keywoard_markup(*res))
        else:
            await message.answer('Результат -> список пуст')
        os.remove(all_path)
        await message.answer("Поиск закончен", reply_markup=kb.find_word_keyboard)
        print('файл удален')
        await state.clear()


# Настройки
@router.message(F.text == 'Настройки')
async def find_word(message: Message):
    return message.answer("Вы в меню 'Настройки'", reply_markup=kb.settings_keyboard)


@router.message(F.text == 'Капслок')
async def switch_caps(message: Message, state: FSMContext):
    global caps

    if caps == 'off':
        caps[0] = 'on'
    else:
        caps[0] = 'off'
    await message.answer(f"Капс {caps[0]}", reply_markup=kb.main_keyboard)


@router.message(F.text == 'Ввод нескольких файлов')
async def switch_caps(message: Message, state: FSMContext):
    global more_files
    if more_files[0] == 'off':
        more_files[0] = 'on'
    else:
        more_files[0] = 'off'
    await message.answer(f"Ввод нескольких файлов {more_files[0]}", reply_markup=kb.main_keyboard)


@router.message(F.text == "конверт message -> txt")
async def convert_message_for_txt(message: Message, state: FSMContext):
    await message.answer("Вы в конвертере")
    await state.set_state(Txt.txt_rout)


@router.message(Txt.txt_rout)
async def convert_text(message: Message, state: FSMContext):
    await message.answer("Запишите текст")
    data = await state.update_data(txt_rout=message.text)
    res = await state.get_data()
    file_res = Search_word.copy_text_for_txt(str(res['txt_rout']), "text.txt")
    doc = FSInputFile(file_res)
    await message.bot.send_document(message.chat.id, doc)
    os.remove(file_res)
    await state.clear()


@router.message(F.text == "Процент совпадения")
async def percent_coincidences(message: Message):
    await message.answer("Проценты совпадения", reply_markup=kb.percent_keyboard)

@router.callback_query(F.data == '100')
async def percent_seventy_five(message: Message):
    global percent_word
    percent_word[0] = 100
    await message.answer("Процент поменян", reply_markup=kb.main_keyboard)
@router.callback_query(F.data == '75')
async def percent_seventy_five(message: Message):
    global percent_word
    percent_word[0] = 75
    await message.answer("Процент поменян", reply_markup=kb.main_keyboard)


@router.callback_query(F.data == '50')
async def percent_seventy_five(message: Message):
    global percent_word
    percent_word[0] = 50
    await message.answer("Процент поменян", reply_markup=kb.main_keyboard)

@router.message(F.text == 'Фишки')
async def fishki_menu(message: Message):
    await message.answer("Вы в меню 'Фишки'",reply_markup=kb.fishki_keyboard)

@router.message(F.text == 'Замена текста')
async def replace_text(message: Message, state: FSMContext):
    await message.answer("Введите слово для замены")
    await state.set_state(Replace_text.word)


@router.message(Replace_text.word)
async def replace_text_word(message: Message, state: FSMContext):
    await state.update_data(word=message.text)
    await message.answer("Введите новое слово")
    await state.set_state(Replace_text.new_word)

@router.message(Replace_text.new_word)
async def replace_text_new_word(message: Message, state: FSMContext):
    await state.update_data(new_word=message.text)
    await message.answer("Введите текст")
    await state.set_state(Replace_text.text)

@router.message(Replace_text.text)
async def replace_text_new_word(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Выберите предложение для замены в меню",reply_markup=kb.replace_keyboard)
    await state.set_state(Replace_text.text_ind)

@router.message(Replace_text.text_ind)
async def replace_text_new_word(message: Message, state: FSMContext):
    await state.update_data(text_ind=message.text)
    res = await state.get_data()

    result = Search_word.replace_word_in_message(res['word'],res['new_word'],res['text'],res['text_ind'])
    await message.answer(result,reply_markup=kb.main_keyboard)
    await state.clear()


@router.message(F.text == "Профиль")
async def profile(message: Message):
    with open(f"db/db.txt", 'r+', encoding='utf-8') as file:
        res = file.readlines()
        print(res)
        lin_res = ''
        for i in res:
            print(i)
            if message.from_user.username in i:
                lin_res = i
                break
        lists = lin_res.split()
    await message.answer(f"Имя {lists[1]}", reply_markup=kb.main_keyboard)

@router.message(F.text == "Служба поддержки")
async def support_service(message:Message,state:FSMContext):
    await message.answer('Введите свое имя',reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Support.name)

@router.message(Support.name)
async def support_name(message:Message,state:FSMContext):
    data = state.update_data(name=message.text)
    await message.answer('Введите текст об ошибке',reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Support.text)


@router.message(Support.text)
async def support_name(message:Message,state:FSMContext):
    data = await state.update_data(text=message.text)
    await message.answer('Спасибо за ваш запрос :)',reply_markup=kb.main_keyboard)
    await state.clear()