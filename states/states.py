from aiogram.fsm.state import StatesGroup, State

class addWord(StatesGroup):
    category_title = State()
    wait_word = State()


class quizWord(StatesGroup):
    wait_answer = State()