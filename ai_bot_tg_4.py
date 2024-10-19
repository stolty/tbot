import os
from together import Together
import asyncio
from telebot.async_telebot import AsyncTeleBot

'''
1. базовая функциональность отвечает на /ai текст
2. добавил полную работоспособность при работе 1х1
3. добавлена асинхронность и nonstop=true
4. убран   апи ключ \ токен тг   для деплоя на облако
'''

TG_TOKEN = os.getenv('TG_TOKEN')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

bot = AsyncTeleBot(TG_TOKEN)
client = Together(TOGETHER_API_KEY)


def get_answer(_model, user_text):
    stream = client.chat.completions.create(
        model=_model,
        messages=[{"role": "user", "content": user_text}],
        stream=True)

    output = ""

    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        output += content
    return output


@bot.message_handler(commands=['start'])
async def start_message(message):
    output = ("Пример запроса:\n"
              "/ai сколько будет 2+2? \n \n"
              "На данный момент доступно 4 различных модели ИИ-ботов: \n"
              "/ai Llama-3.1-405B (топ9)\n"
              "/ai2 Qwen2.5-72B (топ15)\n"
              "/ai3 Llama-3.1-70B (топ25)\n"
              "/ai4 Gemma-2-27b (топ35)\n")
    try:
        await bot.send_message(message.chat.id, output)
    except:
        pass


@bot.message_handler(commands=['help'])
async def help_message(message):
    output = ("Пример запроса:\n"
              "/ai сколько будет 2+2? \n \n"
              "На данный момент доступно 4 различных модели ИИ-ботов: \n"
              "/ai Llama-3.1-405B (топ9)\n"
              "/ai2 Qwen2.5-72B (топ15)\n"
              "/ai3 Llama-3.1-70B (топ25)\n"
              "/ai4 Gemma-2-27b (топ35)\n")
    try:
        await bot.send_message(message.chat.id, output)
    except:
        pass


@bot.message_handler(commands=['ai'])
async def answer_message(message):
    user_text = message.text.split('/ai', 1)[-1].strip()
    if not user_text:
        await bot.reply_to(message, "Пожалуйста, введите текст после команды /ai")
        return

    output_await = get_answer("meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", user_text)
    output = "Llama-3.1-405B:" + '\n' + '\n' + str(output_await)
    try:
        await bot.send_message(message.chat.id, output)
    except:
        pass


@bot.message_handler(commands=['ai2'])
async def answer_message(message):
    user_text = message.text.split('/ai2', 1)[-1].strip()
    if not user_text:
        await bot.reply_to(message, "Пожалуйста, введите текст после команды /ai2")
        return

    output = "Qwen2.5-72B:" + '\n' + '\n' + get_answer("Qwen/Qwen2.5-72B-Instruct-Turbo", user_text)
    try:
        await bot.send_message(message.chat.id, output)
    except:
        pass


@bot.message_handler(commands=['ai3'])
async def answer_message(message):
    user_text = message.text.split('/ai3', 1)[-1].strip()
    if not user_text:
        await bot.reply_to(message, "Пожалуйста, введите текст после команды /ai3")
        return

    output = "Llama-3.1-70B:" + '\n' + '\n' + get_answer("meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", user_text)
    try:
        await bot.send_message(message.chat.id, output)
    except:
        pass


@bot.message_handler(commands=['ai4'])
async def answer_message(message):
    user_text = message.text.split('/ai4', 1)[-1].strip()
    if not user_text:
        await bot.reply_to(message, "Пожалуйста, введите текст после команды /ai4")
        return

    output = "Gemma-2-27B:" + '\n' + '\n' + get_answer("google/gemma-2-27b-it", user_text)
    try:
        await bot.send_message(message.chat.id, output)
    except:
        pass


if __name__ == "__main__":
    asyncio.run(bot.polling(none_stop=True))