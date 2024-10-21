import ppp
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, KeyboardButtonPollType)
from environs import Env

env = Env()
env.read_env()
BOT_TOKEN = env("token")

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем кнопки
btn_1 = KeyboardButton(text='Создать опрос')
btn_2 = KeyboardButton(text='Создать викторину')
btn_3 = KeyboardButton(text='Пицца Шляпа')

# Создаем объект клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[[btn_1, btn_2, btn_3]],
    resize_keyboard=True,
    input_field_placeholder='Нажмите кнопку 1'
)

# Хранение состояния викторины
quiz_state = {}

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Что вы хотите создать?',
        reply_markup=keyboard
    )

# Обработчик для создания опроса
@dp.message(F.text == 'Создать опрос')
async def create_poll(message: Message):
    questions = [
        ("Сколько вам лет?", ["16+", "20+", "52+"]),
        ("Какая следующая пара?", ["Физра", "Да", "Физра"]),
        ("Ваш любимый цвет?", ["Красный", "Чёрный", "Да"])
    ]

    for question, options in questions:
        await message.answer_poll(
            question=question,
            options=options,
            is_anonymous=False
        )

# Обработчик для создания викторины
@dp.message(F.text == 'Создать викторину')
async def create_quiz(message: Message):
    questions = [
        ("2+2*2", ["6", "8", "52"], 0),
        ("Сколько стоит проезд на автобусе?", ["17", "25", "52"], 1),
        ("10/2", ["5", "2", "52"], 0),
    ]

    # Инициализация состояния викторины
    user_id = message.from_user.id
    quiz_state[user_id] = {'current_question': 0, 'correct_answers': 0, 'questions': questions}

    await ask_question(user_id)

async def ask_question(user_id):
    questions = quiz_state[user_id]['questions']
    current_question = quiz_state[user_id]['current_question']

    if current_question < len(questions):
        question, options, correct_index = questions[current_question]
        await bot.send_poll(
            chat_id=user_id,
            question=question,
            options=options,
            is_anonymous=False,
            type='quiz',
            correct_option_id=correct_index
        )
    else:
        # Завершение викторины
        await bot.send_message(
            chat_id=user_id,
            text=f"Вы ответили правильно на {quiz_state[user_id]['correct_answers']} из {len(questions)} вопросов."
        )
        del quiz_state[user_id]

@dp.poll_answer()
async def handle_poll_answer(poll_answer: Message):
    user_id = poll_answer.user.id
    if user_id in quiz_state:
        current_question = quiz_state[user_id]['current_question']
        questions = quiz_state[user_id]['questions']

        if poll_answer.option_ids[0] == questions[current_question][2]:
            quiz_state[user_id]['correct_answers'] += 1

        quiz_state[user_id]['current_question'] += 1
        await ask_question(user_id)


#
@dp.message(F.text == 'Пицца Шляпа')
async def process_pizza(message: Message):
    for img, i in ppp.get_pizza_menu():
        await message.answer_photo(img)
        await message.answer(i)



# Правильная проверка
if __name__ == '__main__':
    print("Бот запущен")
    dp.run_polling(bot)