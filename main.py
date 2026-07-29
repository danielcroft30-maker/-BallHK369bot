import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable not set!")

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Conversion Logic ---
def convert_base(number: str, from_base: int, to_base: int) -> str:
    """Convert a number from one base to another. Supports bases 2-36."""
    try:
        # Convert from source base to decimal (base 10)
        decimal_value = int(number, from_base)
        
        # Convert decimal to target base
        if to_base == 10:
            return str(decimal_value)
        
        # Handle base conversion for bases 2-36
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""
        temp = decimal_value
        
        if temp == 0:
            return "0"
            
        while temp > 0:
            result = digits[temp % to_base] + result
            temp //= to_base
            
        return result
    except ValueError:
        return "❌ Invalid input. Please check the number and bases."

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("🔄 Convert Number", callback_data="convert")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to Number Base Converter Bot!\n\n"
        "I can convert numbers between any bases from 2 to 36.\n\n"
        "🔢 Examples:\n"
        "• '1010 2 10' → Converts binary 1010 to decimal\n"
        "• 'FF 16 2' → Converts hex FF to binary\n"
        "• '42 10 16' → Converts decimal 42 to hex\n\n"
        "Click the button below to start converting!",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "convert":
        await query.edit_message_text(
            "📝 Please send your conversion in this format:\n\n"
            "<number> <from_base> <to_base>\n\n"
            "Example: `1010 2 10`\n\n"
            "Supported bases: 2 to 36"
        )
    elif query.data == "help":
        await query.edit_message_text(
            "ℹ️ *How to use this bot:*\n\n"
            "Send a message with three parts:\n"
            "1️⃣ The number to convert\n"
            "2️⃣ The base it's currently in (2-36)\n"
            "3️⃣ The base you want to convert to (2-36)\n\n"
            "Example commands:\n"
            "• `1010 2 10` → 10\n"
            "• `FF 16 2` → 11111111\n"
            "• `42 10 16` → 2A\n\n"
            "Use `/start` anytime to return to the main menu."
        )

async def handle_conversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the user's conversion request."""
    try:
        parts = update.message.text.strip().split()
        if len(parts) != 3:
            await update.message.reply_text(
                "❌ Please send exactly 3 values: `<number> <from_base> <to_base>`\n\n"
                "Example: `1010 2 10`"
            )
            return
        
        number = parts[0]
        from_base = int(parts[1])
        to_base = int(parts[2])
        
        # Validate base ranges
        if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
            await update.message.reply_text("❌ Bases must be between 2 and 36.")
            return
        
        result = convert_base(number, from_base, to_base)
        
        response = (
            f"🔢 *Conversion Result*\n\n"
            f"📥 Input: `{number}` (base {from_base})\n"
            f"📤 Output: `{result}` (base {to_base})"
        )
        await update.message.reply_text(response)
        
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Please use numbers for the bases and a valid number for the first value.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    await update.message.reply_text(
        "ℹ️ *How to use this bot:*\n\n"
        "Send a message with three parts:\n"
        "1️⃣ The number to convert\n"
        "2️⃣ The base it's currently in (2-36)\n"
        "3️⃣ The base you want to convert to (2-36)\n\n"
        "Example: `1010 2 10` → Converts binary 1010 to decimal (10)"
    )

# --- Main Function ---
def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_conversion))
    
    # Start the bot with long polling
    logger.info("Starting bot with long polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
