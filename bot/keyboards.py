from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils import TRANSLATIONS


def start_keyboard():
    keyboard = InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="Выбрать категорию", callback_data="choose_category"
        )
    )
    return keyboard.as_markup()


def paginated_keyboard(
        items: dict[str, dict],
        stage: str,
        page: int = 0,
        page_size: int = 8,
        back_callback: str = "main_menu"
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    total_pages = (len(items) - 1) // page_size + 1
    start = page * page_size
    end = start + page_size

    for item in list(items.keys())[start:end]:
        item_name = TRANSLATIONS.get(item, item)

        builder.button(
            text=item_name,
            callback_data=f"choose:{stage}:{item}"
        )

    builder.adjust(2)

    # Навигация по страницам
    nav_row = []
    if page > 0:
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"page:{stage}:{page-1}"
            )
        )
    if page < total_pages - 1:
        nav_row.append(
            InlineKeyboardButton(
                text="➡️ Далее",
                callback_data=f"page:{stage}:{page+1}"
            )
        )
    if nav_row:
        builder.row(*nav_row)

    # Кнопка назад
    builder.row(
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=back_callback
        )
    )

    return builder.as_markup()


def filter_keyboard(
    filters: dict[str, dict],
    state_data: dict,
    stage: str,
    page: int = 0,
    page_size: int = 6,
    back_callback: str = "main_menu"
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    total_pages = (len(filters) - 1) // page_size + 1
    start = page * page_size
    end = start + page_size

    for key in list(filters.keys())[start:end]:
        label = TRANSLATIONS.get(key, key)
        is_active = state_data.get(key)
        prefix = "➖" if not is_active else "➕"
        builder.button(
            text=f"{prefix} {label}",
            callback_data=f"toggle_filter:{stage}:{key}"
        )

    builder.adjust(2)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"page:{stage}:{page - 1}"
        ))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(
            text="➡️ Далее",
            callback_data=f"page:{stage}:{page + 1}"
        ))
    if nav_row:
        builder.row(*nav_row)

    builder.row(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data=back_callback
    ))

    return builder.as_markup()
