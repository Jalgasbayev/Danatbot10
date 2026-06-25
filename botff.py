import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = "8714180608:AAFiKwNkGxVF3h1REnhSwXMEbOWARDIginA"
ADMIN_ID = 8568826078

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💎 Donat olish")],
        [KeyboardButton(text="📞 Admin")]
    ],
    resize_keyboard=True
)

donat_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💎105 Almaz")],
        [KeyboardButton(text="💎341 Almaz")],
        [KeyboardButton(text="💎572 Almaz")],
        [KeyboardButton(text="💳 Kunlik")],
        [KeyboardButton(text="💳 Haftalik")],
        [KeyboardButton(text="💳 Oylik")],
        [KeyboardButton(text="🏠 Bosh menyu")]
    ],
    resize_keyboard=True
)

confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Tasdiqlash")],
        [KeyboardButton(text="❌ Orqaga")]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):
    user_data[message.from_user.id] = {"step": None}

    await message.answer(
        "🎮 Free Fire Donat Bot\n\nXush kelibsiz!",
        reply_markup=menu
    )


@dp.message()
async def handler(message: Message):
    user_id = message.from_user.id
    text = message.text or ""

    if user_id not in user_data:
        user_data[user_id] = {"step": None}

    data = user_data[user_id]


    if text == "💎 Donat olish":
        await message.answer(
            "Kerakli paketni tanlang:",
            reply_markup=donat_menu
        )
        return


    if text == "🏠 Bosh menyu":
        await message.answer(
            "Bosh menyu",
            reply_markup=menu
        )
        return


    if text == "📞 Admin":
        await message.answer("@ValiantElite")
        return


    packages = {
        "💎105 Almaz": "13 000 so'm",
        "💎341 Almaz": "36 999 so'm",
        "💎572 Almaz": "59 999 so'm",
        "💳 Kunlik": "8 999 so'm",
        "💳 Haftalik": "24 999 so'm",
        "💳 Oylik": "85 999 so'm"
    }


    if text in packages:
        data["package"] = text
        data["price"] = packages[text]

        await message.answer(
            f"📦 {text}\n"
            f"💰 {packages[text]}\n\n"
            "Buyurtmani tasdiqlaysizmi?",
            reply_markup=confirm_menu
        )
        return


    if text == "❌ Orqaga":
        await message.answer(
            "Paket tanlang:",
            reply_markup=donat_menu
        )
        return


    if text == "✅ Tasdiqlash":
        data["step"] = "id"

        await message.answer(
            "💳 To'lov kartasi:\n\n"
            "KARTA RAQAMI\n"
            "👤 A/J\n\n"
            "To'lov qilgach Free Fire ID yuboring:"
        )
        return


    if data.get("step") == "id":
        data["game_id"] = text
        data["step"] = "nick"

        await message.answer(
            "👤 Nick yuboring:"
        )
        return


    if data.get("step") == "nick":
        data["nick"] = text
        data["step"] = "receipt"

        await message.answer(
            "📸 Endi chek rasmini yuboring:"
        )
        return


    if data.get("step") == "receipt" and message.photo:

        caption = (
            "🆕 YANGI BUYURTMA\n\n"
            f"📦 Paket: {data['package']}\n"
            f"💰 Narx: {data['price']}\n\n"
            f"🆔 ID: {data['game_id']}\n"
            f"👤 Nick: {data['nick']}\n\n"
            f"👤 Username: @{message.from_user.username}"
        )


        await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=caption
        )


        await message.answer(
            "✅ Buyurtmangiz qabul qilindi!",
            reply_markup=menu
        )

        user_data[user_id] = {"step": None}


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
