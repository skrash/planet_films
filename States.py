from aiogram.dispatcher.filters.state import State, StatesGroup


class Step(StatesGroup):
    main_state = State()
    search_state = State()
    search_from_year_state = State()
    add_affix = State()
    genre_state = State()
    author_state = State()
    actor_state = State()
