from aiogram import Dispatcher


from .db import DatabaseMiddleware
from .user_info_updater import UserInfoUpdaterMiddleware


def register_middlewares(dp: Dispatcher):
    # dp.update.middleware(DatabaseMiddleware())
    dp.update.middleware(UserInfoUpdaterMiddleware())
