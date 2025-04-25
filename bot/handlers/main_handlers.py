from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards import paginated_keyboard, start_keyboard, filter_keyboard

from bot.utils import CATEGORIES

router = Router()


@router.callback_query(F.data == "main_menu")
async def main_menu(call: CallbackQuery):
    await call.message.edit_text(
        "Главное меню",
        reply_markup=start_keyboard()
    )

@router.callback_query(F.data == "choose_category")
async def ChooseCategory(call: CallbackQuery):
    await call.message.edit_text(
        "Выберите категорию",
        reply_markup=paginated_keyboard(
            items=CATEGORIES,
            stage="categories"
        )
    )
    print(1, call.data)

@router.callback_query(F.data.startswith("choose:categories"))
async def handle_step(call: CallbackQuery, state: FSMContext):
    category = call.data.split(":")[2]
    await state.update_data(category=category)
    await call.message.edit_text(
        "Выберите подкатегорию",
        reply_markup=paginated_keyboard(
            items=CATEGORIES[category],
            stage="sub_categories",
            back_callback="choose_category"
        )
    )
    print(2, call.data)


@router.callback_query(F.data.startswith("choose:sub_categories"))
async def ChooseSubCategories(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sub_category = call.data.split(":")[2]

    category = data["category"]
    await call.message.edit_text(
        "Выберите подподкатегорию:",
        reply_markup=paginated_keyboard(
            items=CATEGORIES[category][sub_category],
            stage="sub_sub_categories",
            back_callback=f"choose:categories:{category}",
        )
    )
    await state.update_data(sub_category=sub_category)
    print(3, call.data, data)

@router.callback_query(F.data.startswith("choose:sub_sub_categories"))
async def ChooseSubSubCategory(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")
    sub_category = data.get("sub_category")
    sub_sub_category = call.data.split(":")[2]
    await call.message.edit_text(
        "Выберите фильтр",
        reply_markup=paginated_keyboard(
            items=CATEGORIES[category][sub_category][sub_sub_category],
            stage="filters",
            back_callback=f"choose:sub_categories:{sub_category}"
        )
    )
    await state.update_data(sub_sub_category=sub_sub_category)
    print(4, call.data, data)

@router.callback_query(F.data.startswith("choose:filters"))
async def ChooseFilter(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    sub_category = data["sub_category"]
    sub_sub_category = data["sub_sub_category"]
    filters = call.data.split(":")[2]
    await call.message.edit_text(
        "Выберите фильтр",
        reply_markup=filter_keyboard(
            CATEGORIES[category][sub_category][sub_sub_category][filters],
            stage="filter",
            back_callback=f"choose:sub_sub_categories:{sub_sub_category}",
            state_data=data
        )
    )
    await state.update_data(filters=filters)
    print(5, call.data, data)


@router.callback_query(F.data.startswith("choose:filter"))
async def ChooseFilters(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    sub_category = data["sub_category"]
    sub_sub_category = data["sub_sub_category"]
    filters = data["filters"]
    await call.message.edit_reply_markup(
        reply_markup=filter_keyboard(
            filters=CATEGORIES[category][sub_category][sub_sub_category][filters],
            state_data=data,
            stage="filter",
            back_callback=f"choose:filters:{filters}"
        )
    )
    print(6, call.data, data)


@router.callback_query(F.data.startswith("toggle_filter:"))
async def toggle_filter_handler(call: CallbackQuery, state: FSMContext):
    _, stage, key = call.data.split(":")
    data = await state.get_data()
    current_value = data.get(key)

    if current_value:
        data.pop(key)
    else:
        data[key] = True

    category = data["category"]
    sub_category = data["sub_category"]
    sub_sub_category = data["sub_sub_category"]
    filters = data["filters"]

    await state.set_data(data)
    await call.message.edit_reply_markup(
        reply_markup=filter_keyboard(
            filters=CATEGORIES[category][sub_category][sub_sub_category][filters],
            state_data=data,
            stage=stage,
            back_callback=f"choose:sub_sub_categories:{sub_sub_category}"
        )
    )
    await call.answer()
    print(7, call.data, data)

@router.callback_query(F.data.startswith("page:categories"))
async def Page(call: CallbackQuery):
    page = int(call.data.split(":")[2])
    await call.message.edit_reply_markup(
        reply_markup=paginated_keyboard(
            items=CATEGORIES,
            page=page,
            stage="categories"
        )
    )
    print(11, call.data)

@router.callback_query(F.data.startswith("page:sub_categories"))
async def PageSubCategories(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    page = int(call.data.split(":")[2])
    await call.message.edit_reply_markup(
        reply_markup=paginated_keyboard(
            items=CATEGORIES[category],
            page=page,
            stage="sub_categories",
            back_callback=f"choose:categories:{category}"
        )
    )
    print(22, call.data, data)

@router.callback_query(F.data.startswith("page:sub_sub_categories"))
async def PageSubSubcategories(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    sub_category = data["sub_category"]
    page = int(call.data.split(":")[2])
    await call.message.edit_reply_markup(
        reply_markup=paginated_keyboard(
            items=CATEGORIES[category][sub_category],
            page=page,
            stage="sub_sub_categories",
            back_callback=f"choose:sub_categories:{sub_category}"
        )
    )
    print(33, call.data, data)

@router.callback_query(F.data.startswith("page:filters"))
async def PageFilters(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    sub_category = data["sub_category"]
    sub_sub_category = data["sub_sub_category"]
    page = int(call.data.split(":")[2])
    await call.message.edit_reply_markup(
        reply_markup=paginated_keyboard(
            items=CATEGORIES[category][sub_category][sub_sub_category],
            stage="filters",
            page=page,
            back_callback=f"choose:sub_categories:{sub_sub_category}",
        )
    )
    print(44, call.data, data)

@router.callback_query(F.data.startswith("page:filter"))
async def PageFilter(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    sub_category = data["sub_category"]
    sub_sub_category = data["sub_sub_category"]
    filters = data["filters"]
    page = int(call.data.split(":")[2])
    await call.message.edit_reply_markup(
        reply_markup=filter_keyboard(
            filters=CATEGORIES[category][sub_category][sub_sub_category][filters],
            stage="filter",
            page=page,
            back_callback=f"choose:sub_categories:{sub_sub_category}",
            state_data=data
        )
    )
    print(55, call.data, data)

@router.callback_query()
async def handler(call: CallbackQuery):
    print(call.data)
