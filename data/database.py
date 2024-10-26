from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, host):
        self.client = AsyncIOMotorClient(host=host)
        self.db = self.client.get_database("support_bot")
        self.questions = self.db.get_collection("questions")
        self.banned_users = self.db.get_collection("banned_users")
        self.users = self.db.get_collection("users")

    async def check_user_exists(self, user_id):
        user = await self.users.find_one({"user_id": user_id})

        return user is not None

    async def add_question(self, user_id, question):
        insert_query = {
            "user_id": user_id,
            "question": question
        }

        try:
            await self.questions.insert_one(insert_query)
        except Exception as _err:
            raise _err

    async def answer_the_question(self, user_id):
        delete_query = {
            "user_id": user_id
        }

        try:
            await self.questions.delete_one(delete_query)
        except Exception as _err:
            raise _err

    async def get_all_questions(self):
        questions = await self.questions.find({}, {"_id": 0, "user_id": 1, "question": 1}).to_list(length=None)

        return questions
    
    async def get_question_by_id(self, user_id):
        question = await self.questions.find_one({"user_id": user_id})

        return question

    async def ban_user(self, user_id):
        query = {
            "user_id": user_id
        }

        await self.users.delete_one(query)
        await self.banned_users.insert_one(query)

    async def get_banned_users(self, user_id):
        banned_user = await self.banned_users.find_one({"user_id": user_id})

        return banned_user

    async def get_users(self):
        users = await self.users.find({}, {"_id": 0, "user_id": 1}).to_list(length=None)

        return users
    
    async def add_user(self, user_id):
        insert_query = {
            "user_id": user_id
        }

        if not await self.check_user_exists(user_id=user_id):
            await self.users.insert_one(insert_query)
