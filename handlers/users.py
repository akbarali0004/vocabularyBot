import asyncio
import random

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import StateFilter

from config import words
from keyboards import * #main_menu, menu2, direction_btn, ready_btn, cancel_btn, view_categories_btn
from states import addWord, quizWord
from utils import * #save_user, add_word, add_category, get_category


router = Router()


@router.message(F.text=="/start")
async def start_answer(message:types.Message):
    nik_name = message.from_user.first_name
    username = message.from_user.username
    tg_id = message.from_user.id
    await save_user(nik_name, username, tg_id)

    await message.answer("👋 Hello! Welcome to <b>Word Master Bot</b>.\n"
                         "Here you can build your own English–Uzbek dictionary and test yourself anytime.\n\n"
                         "<i>Choose an option below 👇</i>", reply_markup=main_menu)


@router.message(F.text=="/cancel", StateFilter(addWord.category_title, addWord.wait_word))
async def cancel_funk(message:types.Message,state:FSMContext):
    await state.clear()
    await message.answer("<b>❌ Action canceled.</b>", reply_markup=ReplyKeyboardRemove())
    await message.answer("<b>This is the Main Menu</b>\n\n<i>Choose an option below 👇</i>", reply_markup=main_menu)


@router.callback_query(F.data=="add_word")
async def create_catagory(call:types.CallbackQuery, state:FSMContext):
    await call.message.answer("<b>🌟 Great! Let’s add a new word to your vocabulary.</b>\n\n"
                              "But first — please enter a <b>category name</b> for this vocabulary 🗂️\n\n"
                              "<i>(Example: Animals, Technology, Food, Day1, Level1...)</i>")
    await state.set_state(addWord.category_title)
    await call.answer()


@router.message(F.text, addWord.category_title)
async def add_word_ans(message:types.Message, state:FSMContext):
    if len(message.text) > 35:
        await message.answer("⚠️ Please keep your category title <b>under 35 characters</b>.\nTry a shorter and more meaningful title 😊")
    else:
        await message.answer("<b>📝 Please send me a word pair like this:</b>\n\n<i>apple - olma</i>", reply_markup=cancel_btn)
        await state.set_state(addWord.wait_word)
        await state.update_data(category_title=message.text)


@router.message(F.text=="/save", addWord.wait_word)
async def save_words(message:types.Message, state:FSMContext):
    data = await state.get_data()
    global words 
    words = data.get("word_pairs", [])
    category_title = data.get("category_title", '')

    #so'zlarni bazaga saqlash
    category_id = await add_category(category_title, message.from_user.id)
    for i in words:
        await add_words(i[0], i[1][0], message.from_user.id, category_id[0])

    await state.clear()
    await message.answer("<b>✅ All items have been saved successfully!</b>\nThank you. You can now return to the main menu or add new ones anytime.", reply_markup=menu2)


@router.message(F.text, addWord.wait_word)
async def add_word_funk(message:types.Message, state:FSMContext):
    text = message.text
    
    # har bir qatordagi juftlikni ro'yxatga ajratish
    items = []
    word_pairs = []
    for line in text.split("\n"):
        if "-" in line:
            parts = line.split("-")
            english = parts[0].strip()
            uzbek = parts[1].strip()

            if ',' in parts[1]:
                items = parts[1].split(",")

            items.append(uzbek)
            word_pairs.append((english, items))
            items = []
    
    # FSM ga saqlash
    data = await state.get_data()
    existing_pairs = data.get("word_pairs", [])
    existing_pairs.extend(word_pairs)
    await state.update_data(word_pairs=existing_pairs)

    total_pairs = len(existing_pairs)

    if total_pairs<1:
        await message.answer("<b>⚠️ Please use the correct format: english - uzbek</b>\n\n<i><b>Example:</b> book - kitob</i>")
    else:
        await message.answer(f"<b>✅ Added successfully!</b> Total: <b>{total_pairs}</b> word pairs.\n\nYou can keep adding more, use /undo to delete the last word, or /save when you’re done.")


@router.callback_query(F.data=="start_quiz")
async def strat_quiz(call:types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>🌍 Please choose the direction of translation:</b>", reply_markup=direction_btn)


@router.callback_query(F.data.in_(["eng_uz", "uz_eng"]))
async def eng_uz_quiz(call:types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>🚀 Are you ready to start learning new words?</b>", reply_markup=ready_btn)


@router.callback_query(F.data=="ready")
async def start_quiz(call:types.CallbackQuery, state:FSMContext):
    await call.message.delete()
    msg = await call.message.answer("1️⃣ ...")
    await asyncio.sleep(1)
    await msg.edit_text("2️⃣ Wait ...")
    await asyncio.sleep(1)
    await msg.edit_text("3️⃣ Preparing...")
    await asyncio.sleep(1)
    await msg.edit_text("<b>🚀 Let's go!</b>")
    await asyncio.sleep(1)
    await msg.delete()

    word_pair = random.choice(words)
    word = random.choice(word_pair[1])
    question_words = (word_pair[0], word)
    await call.message.answer(f"<b>1. {word.capitalize()} - ...</b>")
    # global words
    # words.remove()

    await state.set_state(quizWord.wait_answer)
    await state.update_data(question=question_words)
    await state.update_data(counter = 1)


@router.message(F.text=="/stop", quizWord.wait_answer)
async def stop_quiz(message:types.Message):
    await message.answer("🏁 The “<b>Technology and its Teaching Methodology</b>” quiz has ended!\n\n"
                         "You answered <b>1</b> question:\n\n"
                         "✅ Correct – 0\n❌ Wrong – 1\n⌛ Skipped – 0\n⏱️ Time spent – 2.1 seconds\n\n"
                         "📊 Your rank: <b>1</b. out of 1 participants.", reply_markup=stop_quiz_btn)


@router.message(F.text, quizWord.wait_answer)
async def check_answer(message:types.Message, state:FSMContext):
    text = message.text.lower()
    data = await state.get_data()
    question = data.get("question")
    result_text = f"❌ Wrong answer. <b><i>{question[1]} - {question[0]}</i></b>"
    
    if text == question[0].lower():
        result_text = "✅ Correct answer!"

    word_pair = random.choice(words)
    word = random.choice(word_pair[1])

    counter = await state.get_data()
    num = counter.get("counter", 0)

    question_words = (word_pair[0], word)
    await state.update_data(counter=num+1)
    await state.update_data(question=question_words)

    await message.answer(f"{result_text}\n\n<b>{num+1}. {word.capitalize()} - ...</b>")



@router.callback_query(F.data=="view_words")
async def view_words(call:types.CallbackQuery):
    await call.answer()
    categories = await get_category(call.from_user.id)

    await call.message.answer("<b>Your words:</b>", reply_markup=view_categories_btn(categories))


@router.callback_query(F.data.startswith("cat_"))
async def get_words_handler(call:types.CallbackQuery):
    category_id = int(call.data.split("_")[1])
    words = await get_words(category_id, call.from_user.id)

    words_list_text = f"<b>__title__ Words:</b>\n\n"
    for indeks, (en, uz) in enumerate(words, start=1):
        words_list_text += f"<b>{indeks}</b>. {en} - {uz}\n"

    await call.message.answer(words_list_text)

    await call.answer()

