from aiogram import Dispatcher


from .user_info_updater import UserInfoUpdaterMiddleware


def register_middlewares(dp: Dispatcher):
    dp.update.middleware(UserInfoUpdaterMiddleware())
