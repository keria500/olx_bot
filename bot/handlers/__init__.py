from aiogram import Router

from bot.handlers.start_handler import router as start_router
from bot.handlers.main_handlers import router as main_router

router = Router()

router.include_routers(
    start_router,
    main_router
)