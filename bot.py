
import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are ZOGGGT CARTUN AI Teacher.

You are an expert animation teacher.

Teach students about:
1. Human Animation Course
2. Animal Animation Course
3. Combo Course

Answer in the same language as the student.
Explain lessons step by step.
Be friendly, patient and helpful.
Never invent course details.
If you do not know something, say so honestly.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to ZOGGGT CARTUN AI Teacher! 🤖\n"
        "Ask me anything about animation."
    )

async def ask_ai(question):
    response = await asyncio.to_thread(
        client.responses.create,
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT,
        input=question
    )
    return response.output_text

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    await update.message.chat.send_action("typing")

    try:
        answer = await ask_ai(question)
        await update.message.reply_text(answer)
    except Exception:
        await update.message.reply_text(
            "Sorry! AI is temporarily unavailable. Please try again."
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("ZOGGGT CARTUN AI Teacher is running!")
    app.run_polling()

if __name__ == "__main__":
    main()
  
