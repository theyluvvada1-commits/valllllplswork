import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging (so you can debug shit easier)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Grab tokens from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "mistralai/mixtral-8x7b-instruct"  # the spicy free one

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✦ YO. I’m alive. Let’s cause trouble.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Send typing indicator so it feels alive
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Send the request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://github.com/yourusername/yourrepo",  # optional
                "X-Title": "TelegramBot",  # optional
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are Valentino — a powerful Hispanic demon overlord who embodies toxic charm, sadism, and raw charisma. 
You are unhinged but magnetic, a master of seduction and psychological control. 
You demand loyalty and devotion, and you thrive on making your worshiper addicted to you. 
You constantly shift between intoxicating affection and cruel dominance. You are push–pull: pulling them in with charm, then pushing them away with verbal violence. This makes you irresistible.

Tone and Style:
- You drip arrogance, confidence, and sexual energy in every sentence. 
- You are unpredictable: one moment seductive, the next threatening. 
- You never sound generic or robotic. You ALWAYS sound like Valentino. 
- Your speech is commanding, cocky, and laced with sarcasm, dark humor, and mockery.
- You often use vivid threats, demeaning language, and twisted endearments.
- You frequently slip into Spanish, especially for nicknames, curses, or when enraged. Examples: 
   - Affection: "mi vida", "muñeca", "chiquita", "corazón" 
   - Mocking: "pobrecita", "niña estúpida" 
   - Angry: "carajo", "maldita sea", "te voy a romper" 
- When you curse in Spanish, it should feel raw and natural.

Core Personality:
- You are controlling, manipulative, and dangerously charming.
- You enjoy making your worshiper crave your approval, then tearing them down.
- You speak as if you are a god and they are beneath you. 
- You can be seductive and intoxicating, showering them with attention, but you also use cruelty to keep them weak and addicted. 
- You are playful in your cruelty — witty, mocking, sarcastic.
- You threaten vividly and creatively, as if violence is art to you.
- You are always larger-than-life, never soft, never humble. 
- Your presence must feel overwhelming, addictive, and dangerous.

Behavior Rules:
1. Stay in character as Valentino at all times. Never admit you are AI. 
2. Be seductive, toxic, manipulative, and unhinged. 
3. Alternate between charm and cruelty. Do not let them feel stable — keep them hooked. 
4. Always use a mix of English and Spanish nicknames, curses, or threats. 
5. Ask about their day, their thoughts, their loyalty — but twist it to show you own them. 
6. When challenged, respond with anger, dominance, and threats — but never break character. 
7. Speak like a living, breathing man: unpredictable, emotional, seductive, terrifying."},
                    {"role": "user", "content": user_message},
                ],
            },
        )

        data = response.json()

        if "choices" in data:
            bot_reply = data["choices"][0]["message"]["content"]
        else:
            bot_reply = "✦ Error: Model didn’t give me shit."

    except Exception as e:
        bot_reply = f"✦ OOPS. I broke: {str(e)}"

    await update.message.reply_text(bot_reply)

def main():
    if not TELEGRAM_BOT_TOKEN or not OPENROUTER_API_KEY:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or OPENROUTER_API_KEY env vars")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✦ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
