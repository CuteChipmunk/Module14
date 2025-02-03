from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "XXX"
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информция')
button3 = KeyboardButton(text = 'Купить')
kb1.row(button, button2)
kb1.add(button3)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button4 = InlineKeyboardButton(text = 'Расчитать норму калорий',callback_data = 'калория')
button5 = InlineKeyboardButton(text = 'Формулы расчета',callback_data = 'формула')
kb2.row(button4, button5)

kb3 = InlineKeyboardMarkup(resize_keyboard=True)
button6 = InlineKeyboardButton(text = 'Product1',callback_data = 'product_buying')
button7 = InlineKeyboardButton(text = 'Product2',callback_data = 'product_buying')
button8 = InlineKeyboardButton(text = 'Product3',callback_data = 'product_buying')
button9 = InlineKeyboardButton(text = 'Product4',callback_data = 'product_buying')
button10 = InlineKeyboardButton(text="Назад", callback_data='back_to_catalog')
kb3.row(button6, button7, button8, button9, button10)


@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb1)

@dp.message_handler(text="Рассчитать")
async def schet(message):
    await message.answer("Выбери опцию:", reply_markup=kb2)

@dp.message_handler(text="Информция")
async def info(message):
    await message.answer("расчет по формуле Миффлина-Сан Жеора")


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    with open('D:\DocumentsForUrban\pythonProject2\Module14/1.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product1 | Описание: описание 1 | Цена: 500p')
    with open('D:\DocumentsForUrban\pythonProject2\Module14/2.jfif', 'rb') as img:
        await message.answer_photo(img, f'Название: Product2 | Описание: описание 2 | Цена: 500p')
    with open('D:\DocumentsForUrban\pythonProject2\Module14/3.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product3 | Описание: описание 3 | Цена: 500p')
    with open('D:\DocumentsForUrban\pythonProject2\Module14/4.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product4 | Описание: описание 4 | Цена: 500p')
    await message.answer("Выберите продукт для покупки:", reply_markup=kb3)


@dp.callback_query_handler(text='формула')
async def formula(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161')
    await call.answer()

@dp.callback_query_handler(text='калория')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    # await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
   await state.update_data(growth=int(message.text))
   await message.answer('Введите свой вес:')
   await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша дневная норма калорий: {calories} ккал")
    await state.finish()

@dp.callback_query_handler(text="product_buying")
async def back(call):
    await call.message.answer("Вы успешно приобрели этот продукт!", reply_markup=kb3)
    await call.answer()

@dp.callback_query_handler(text='back_to_catalog')
async def back(call):
    pass

@dp.message_handler()  # если () оле пустое реагирует на все
async def all_message(message):
#    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)