import time
import telebot
import threading
import get_book_list
import uuid

bot = telebot.TeleBot('YOUR_API')

data = {}

def update_data():
    global data
    while True:
        data = t.parse_info('https://ctice.gov.md/manuale-scolare/')
        time.sleep(300)

threading.Thread(target=update_data).start()
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello! To get instructions, please use the command /instruction.")

@bot.message_handler(commands=['instruction'])
def start(message):
    gif_url = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWQzbW9oaDRmaXA2bGJlemZqa2xrOHZ0dDRncnV2dXF3bDV3bmRicCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ITow4I6fOLsMykudYh/giphy.gif'
    bot.send_animation(message.chat.id, gif_url, caption="How to use")

@bot.inline_handler(lambda query: True)

def query_text(query):
    global data

    text = query.query
    parts = text.split()

    # get class nfo
    class_info = ""
    if len(parts) > 1:
        class_number = parts[0]
        if class_number.isdigit() and int(class_number) in range(1, 16):
            if int(class_number) == 13:
                class_info = "Group: Limba Engleza"
            elif int(class_number) == 14:
                class_info = "Group: Limba Franceza"
            elif int(class_number) == 15:
                class_info = "Group: Manuale vechi"
            else:
                class_info = f"*Clasa:* {class_number}"
        else:
            class_info = "неверный номер класса"

        if len(parts) == 2:
            class_number = parts[0]
            keyword = parts[1]

        if data:
            results = []
            for class_name, books_info in data.items():
                if str(class_name) == class_number:
                    for book_info in books_info:
                        file_name = book_info['NAME']
                        download_link = book_info['LINK']

                        if keyword.lower() in file_name.lower():
                            results.append(book_info)

            articles = []
            for result in results:
                file_name = result['NAME']
                download_link = result['LINK']

                message_text = f'*Book:* `{file_name}`\n{class_info}'

                result_id = uuid.uuid4().hex
                keyboard = telebot.types.InlineKeyboardMarkup()
                download_button = telebot.types.InlineKeyboardButton(
                    text="Download 📥",
                    url=download_link
                )
                keyboard.add(download_button)

                article = telebot.types.InlineQueryResultArticle(
                    id=result_id,
                    title=file_name,
                    input_message_content=telebot.types.InputTextMessageContent(
                        message_text=message_text,
                        parse_mode='Markdown'
                    ),
                    reply_markup=keyboard,
                    url=download_link,
                    hide_url=True
                )
                articles.append(article)

            bot.answer_inline_query(query.id, articles)
        else:
            print('Ошибка при парсинге')

    # history
    # user_id = query.from_user.id  # get user ID
    # user_name = query.from_user.username  # get nikname if exist
    # user_info = user_name if user_name else f"User ID: {user_id}"
    # print(f"{user_info} отправил запрос: {text}")
    # import datetime
    # # Save the output to a text file with the current date and time
    # with open('output.txt', 'a') as f:
    #    f.write(f"{datetime.datetime.now()} - {user_info} отправил запрос: {text}\n")

bot.infinity_polling()
