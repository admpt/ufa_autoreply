import asyncio
import datetime
import json
import os
from pathlib import Path

from aiogram import Router, F
from aiogram.client import bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import DeleteBusinessMessages, PinChatMessage
from aiogram.types import Message, InlineKeyboardButton, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram import types
from dialogs import bot_settings
from states.user import Menu


start_router = Router()
# **********************************************************************************************************************
ufa_main = FSInputFile("images/menu/hi.jpg")
ufa = FSInputFile("images/uslugi_ufa/ufa.jpg")
getcontact = FSInputFile("images/getcontact/getcontact.png")
numbuster = FSInputFile("images/numbuster/numbuster.png")
yandex_direct = FSInputFile("images/ads_yandex_direct/yandex_direct.jpg")
site = FSInputFile("images/development/site.jpg")
money = FSInputFile("images/images/money.jpg")
email = FSInputFile("images/email/email.jpg")
other = FSInputFile("images/other/other.jpg")


getcontact_text = """<b>GetContact</b>\n\nВ приложении Getcontact мы можем опубликовывать для вас теги и отзывы, именно те - которые Вы захотите, а при необходимости — полностью удалить выбранные теги или комментарии - вдруг они Вам не нравятся или же они негативного формата.\n\n<b><a href="tg://resolve?domain=ufazdes_sale">Актуальные акции</a> <b>l</b> <a href="tg://resolve?domain=ufazdesvpn_bot">Лучший VPN</a> <b>l</b> <a href="https://ufazdes.ru/">Наш сайт</a></b>"""
numbuster_text = """<b>Numbuster</b>\n\nВ приложении NumBuster мы можем повысить ваш рейтинг с помощью накрутки меток (смайликов), а также разместить для вас отзывы и теги — подробности уточняйте у нашего менеджера. При желании мы готовы удалить отдельные негативные метки, отзывы или теги. Однако стоит учитывать, что не все отзывы и теги подлежат удалению — наш менеджер подробно проконсультирует вас по этому вопросу.\n\n<b><a href="tg://resolve?domain=ufazdes_sale">Актуальные акции</a> <b>l</b> <a href="tg://resolve?domain=ufazdesvpn_bot">Лучший VPN</a> <b>l</b> <a href="https://ufazdes.ru/">Наш сайт</a></b>"""
yandex_direct_text = """<b>Яндекс Директ</b>\n\nОзнакомьтесь с актуальной стоимостью услуг по настройке контекстной рекламы в Яндексе. Все цены приведены без учета акций и специальных предложений.\n\n<b><a href="tg://resolve?domain=ufazdes_sale">Актуальные акции</a> <b>l</b> <a href="tg://resolve?domain=ufazdesvpn_bot">Лучший VPN</a> <b>l</b> <a href="https://ufazdes.ru/">Наш сайт</a></b>"""
development_text = """<b>Web Разработка</b>\n\nОзнакомьтесь с актуальной стоимостью услуг по разработке. Все цены приведены без учета акций и специальных предложений.\nИтоговая цена зависит от требований проекта и уточняется после консультации с менеджером.\n\n<b><a href="tg://resolve?domain=ufazdes_sale">Актуальные акции</a> <b>l</b> <a href="tg://resolve?domain=ufazdesvpn_bot">Лучший VPN</a> <b>l</b> <a href="https://ufazdes.ru/">Наш сайт</a></b>"""
money_text = """<b>Оплата</b>\n\nВы можете оплатить услугу любым удобным для вас способом. Перед оплатой мы отправляем индивидуальную форму заявки. Наш менеджер с удовольствием предоставит вам все необходимые инструкции и форму оплаты, адаптированную под выбранный вами вид услуги.\n\n<b><a href="tg://resolve?domain=ufazdes_sale">Актуальные акции</a> <b>l</b> <a href="tg://resolve?domain=ufazdesvpn_bot">Лучший VPN</a> <b>l</b> <a href="https://ufazdes.ru/">Наш сайт</a></b>"""
other_text = """<b>Другие услуги</b>\n\nУ нас множество услуг, и они к сожалению не помещаются, полный список можно посмотреть в нашем канале с услугами и ценами, для этого нажмите кнопку "все услуги\"\n\n<b><a href="tg://resolve?domain=ufazdes_sale">Актуальные акции</a> <b>l</b> <a href="tg://resolve?domain=ufazdesvpn_bot">Лучший VPN</a> <b>l</b> <a href="https://ufazdes.ru/">Наш сайт</a></b>"""
email_text = """<b>E-mail рассылки</b>\n\nМы более 5 лет занимаемся эффективными e-mail рассылками. Используем надежные SMTP-серверы с выделенными IP и высокой доставляемостью (до 97% писем во «Входящие»). Стабильную доставку гарантируют выделенные IP-адреса и тщательно подобранный POOL IP с безупречной репутацией. Организуем рассылку «под ключ» и при желании обучим вас всем этапам процесса — чтобы вы могли самостоятельно запускать свои кампании.\n\n<b><a href="tg://resolve?domain=ufazdes_sale">Актуальные акции</a> <b>l</b> <a href="tg://resolve?domain=ufazdesvpn_bot">Лучший VPN</a> <b>l</b> <a href="https://ufazdes.ru/">Наш сайт</a></b>"""
# **********************************************************************************************************************
OWNER_ID = 7162682842

async def send_main_menu(message: Message, dialog_manager: DialogManager, state: FSMContext) -> None:
    data = await state.get_data()
    previous_message_id = data.get("previous_message_id")

    user = dialog_manager.event.from_user
    full_name = f"{user.first_name or 'Гость'} {user.last_name or ''}".strip()
    auto_reply_text = f"<b><i>{full_name}, приветствуем в нашем меню агентства ufazdes.ru!</i></b>"


    business_connection_id = getattr(message, 'business_connection_id', None)
    if previous_message_id and business_connection_id:
        try:
            print(f"Попытка удалить сообщение ID: {previous_message_id} через DeleteBusinessMessages")
            await message.bot.delete_business_messages(
                business_connection_id=business_connection_id,
                message_ids=[previous_message_id]
            )
        except Exception as e:
            print(f"Ошибка при удалении предыдущего сообщения: {e}")

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Услуги и цены",
            callback_data="team"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Отзывы",
            url="https://t.me/otzyv_ufazdes"
        ),
        InlineKeyboardButton(
            text="Акции",
            url="https://t.me/ufazdes_sale"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Оплата",
            callback_data="money"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" 🫵Позвать менеджера",
            callback_data="give_me_manager"
        )
    )

    sent_message = await message.answer_photo(
        photo=ufa_main,
        caption=auto_reply_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await state.update_data(previous_message_id=sent_message.message_id)


@start_router.business_message()
async def start(message: Message, dialog_manager: DialogManager, state: FSMContext) -> None:
    if message.from_user.id == OWNER_ID:
        return
    await send_main_menu(message, dialog_manager, state)


@start_router.callback_query(lambda c: c.data == "back")
async def back_to_main(callback_query: types.CallbackQuery, dialog_manager: DialogManager, state: FSMContext) -> None:
    try:
        await callback_query.message.delete()
    except Exception as e:
        print(f"[back_to_main] Ошибка при удалении сообщения: {e}")
    await send_main_menu(callback_query.message, dialog_manager, state)



@start_router.callback_query(lambda c: c.data == "team")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Getcontact",
            callback_data="getcontact"
        ),
        InlineKeyboardButton(
            text="Numbuster",
            callback_data="numbuster"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Реклама",
            callback_data="yandex_direct"
        ),
        InlineKeyboardButton(
            text="Рассылки",
            callback_data="email"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Cайты",
            callback_data="development"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Другие услуги",
            callback_data="other"
        ),
    )

    await callback_query.message.answer_photo(
        photo=ufa,
        caption="Возможности нашей команды:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@start_router.callback_query(lambda c: c.data == "getcontact")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    caption = getcontact_text

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оплата",
            callback_data="money"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" 🫵Позвать менеджера",
            callback_data="give_me_manager"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔙 Вернуться",
            callback_data="back"
        )
    )

    await callback_query.message.answer_photo(
        photo=FSInputFile("images/getcontact/getcontact.png"),
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@start_router.callback_query(lambda c: c.data == "numbuster")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    caption = numbuster_text

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оплата",
            callback_data="money"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" 🫵Позвать менеджера",
            callback_data="give_me_manager"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔙 Вернуться",
            callback_data="back"
        )
    )

    await callback_query.message.answer_photo(
        photo=FSInputFile("images/numbuster/numbuster.png"),
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@start_router.callback_query(lambda c: c.data == "yandex_direct")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    caption = yandex_direct_text

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оплата",
            callback_data="money"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" 🫵Позвать менеджера",
            callback_data="give_me_manager"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔙 Вернуться",
            callback_data="back"
        )
    )

    await callback_query.message.answer_photo(
        photo=FSInputFile("images/ads_yandex_direct/ads.png"),
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@start_router.callback_query(lambda c: c.data == "development")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    caption = development_text

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оплата",
            callback_data="money"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" 🫵Позвать менеджера",
            callback_data="give_me_manager"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔙 Вернуться",
            callback_data="back"
        )
    )


    await callback_query.message.answer_photo(
        photo=FSInputFile("images/development/site.png"),
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@start_router.callback_query(lambda c: c.data == "email")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    caption = email_text

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оплата",
            callback_data="money"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" 🫵Позвать менеджера",
            callback_data="give_me_manager"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔙 Вернуться",
            callback_data="back"
        )
    )


    await callback_query.message.answer_photo(
        photo=FSInputFile("images/email/email.jpg"),
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )



@start_router.callback_query(lambda c: c.data == "money")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    caption = money_text

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🔙 Вернуться",
            callback_data="back"
        )
    )

    await callback_query.message.answer_photo(
        photo=FSInputFile("images/images/money.jpg"),
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@start_router.callback_query(lambda c: c.data == "other")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    if callback_query.from_user.id != OWNER_ID:
        return
    caption = other_text

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Все услуги",
            url="https://t.me/price_ufazdes"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔙 Вернуться",
            callback_data="back"
        )
    )

    await callback_query.message.answer_photo(
        photo=FSInputFile("images/other/other.jpg"),
        caption=caption,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


BOSS_ID = 7208555539
@start_router.callback_query(lambda c: c.data == "give_me_manager")
async def greet_button_pressed(callback_query: types.CallbackQuery, dialog_manager: DialogManager) -> None:
    user = callback_query.from_user
    user_mention = f"@{user.username}" if user.username else f"<code>{user.id}</code>"

    await callback_query.message.answer(
        text="Менеджер подойдет в ближайшее время.",
        parse_mode="HTML"
    )

    await callback_query.bot.send_message(
        BOSS_ID,
        f"Клиент {user_mention} вызывает вас!",
        parse_mode="HTML"
    )