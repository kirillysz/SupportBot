from aiogram.fsm.state import State, StatesGroup

class QuestionForm(StatesGroup):
    question = State()

class AnswerForm(StatesGroup):
    answer = State()
    question_user_id = State()
    question = State()