import asyncio
import logging
import qrcode
import os

from io import BytesIO

from dotenv import load_dotenv

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from datetime import datetime as dt

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import BufferedInputFile

# ENV stuff
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')  # Your own Telegram bot API token
VIVES_BASE = os.getenv('VIVES_BASE')
VIVES_END = os.getenv('VIVES_END')
MCDO_BASE = os.getenv('MCDO_BASE')
MCDO_END = os.getenv('MCDO_END')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Create custom keyboard
vives_ticket_button = KeyboardButton(text='📚  VIVES parkeerticket  📚')
mcdo_ticket_button = KeyboardButton(text='🍔  McDo parkeerticket  🍔')
bot_kb = ReplyKeyboardMarkup(keyboard=[[vives_ticket_button], [mcdo_ticket_button]],
                             resize_keyboard=True, one_time_keyboard=True)

# Wait for start command and show keyboard
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hallo!\nKlaar om gratis te parkeren?!\n", reply_markup=bot_kb)

# Wait for ticket command, create ticket and respond with qr
@dp.message(Command('ticket'))
@dp.message(F.text.contains('parkeerticket'))
async def english(message: types.Message):

    await message.answer('Code en QR genereren..')

    # Prepare time stuff
    now = dt.now()
    year = now.year
    month = now.strftime('%m')
    day = now.strftime('%d')
    hour = now.strftime('%H')
    minute = now.strftime('%M')
    second = now.strftime('%S')

    # Create code with base + time + end
    if 'VIVES' in message.text:
        code = f'{VIVES_BASE}{year}{month}{day}{hour}{minute}{second}{VIVES_END}'
        type = 'VIVES'

    elif 'McDo' in message.text:
        code = f'{MCDO_BASE}{year}{month}{day}{hour}{minute}{second}{MCDO_END}'
        type = "McDonald's"

    # Create caption
    caption = f"Type: {type}\n\nCode: {code}\n\nScan de QR aan de uitgang van de parking!\n\n\nt.me/XpoKortrijkTicketBot"

    # Create QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        border=0
    )

    # Add data to QR
    qr.add_data(code)

    # Create image from QR
    qr_code = qr.make_image(
        fill_color="black", back_color="white").resize((500, 500))

    # Create white background
    background = Image.new("RGB", (1080, 1920), (255, 255, 255))

    # Load double arrow
    arrow = Image.open("arrow_up.png").resize((100, 100))

    # Paste qr code on background
    background.paste(qr_code, (290, 85))

    # Paste double arrow on background
    background.paste(arrow, (490, 910), mask=arrow)

    # Create font from .tff file
    font = ImageFont.truetype("open_sans.ttf", 45)

    # Create drawing context
    context = ImageDraw.Draw(background)

    context.multiline_text(xy=(540, 1500), text=caption, font=font, fill=(
        0, 0, 0), anchor="ms", align="center")

    # Convert to Bytes
    bio = BytesIO()
    bio.name = "qr.png"
    background.save(bio, 'PNG')
    bio.seek(0)

    qr_file = BufferedInputFile(bio.read(), filename="file.txt")

    # Send
    await message.reply_photo(photo=qr_file)

# Run bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
