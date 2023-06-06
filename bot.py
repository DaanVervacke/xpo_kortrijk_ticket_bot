import logging
import qrcode
import os

from io import BytesIO

from dotenv import load_dotenv

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from datetime import datetime as dt

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ENV stuff
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')  # Your own Telegram bot API token
BASE = os.getenv('BASE')  # 540513002 (for now)
END = os.getenv('END')  # 515 (for now)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Create custom keyboard
ticket_button = KeyboardButton('🎟️  Genereer parkeerticket  🎟️')
bot_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True).add(ticket_button)

# Wait for start command and show keyboard


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hallo!\nKlaar om gratis te parkeren?!\n", reply_markup=bot_kb)

# Wait for ticket command, create ticket and respond with qr

@dp.message_handler(commands=['ticket'])
@dp.message_handler(regexp='Genereer parkeerticket')
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
    code = f'{BASE}{year}{month}{day}{hour}{minute}{second}{END}'

    # Create caption
    caption = f"Code: {code}\n\nScan de QR aan de uitgang van de parking!\n\n\nt.me/XpoKortrijkTicketBot"

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

    # Send
    await message.reply_photo(photo=bio)

# Run bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
