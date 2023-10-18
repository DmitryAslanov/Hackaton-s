import time
import telebot
import csv, io
import import_ipynb
import spacy_ml
import my_downloads

bot = telebot.TeleBot('6386042545:AAG3xFFJm0RqPk4k5GzoOGyyOtjm6HkMui4')


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Здравствуйте! \n'
                                      'Чтобы получить рейтинг одного пресс-релиза, отправьте его файлом в формате .txt\n'
                                      'Чтобы получить рейтинг нескольких пресс-релизов, отправьте их файлом в формате .csv\n'
                                      'Также вы можете отправить текст одним сообщением, однако длина сообщений в телеграм ограничена')


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id, 'Анализируем...')
    data = message.text
    answer = spacy_ml.predict_text(data)
    bot.send_message(message.chat.id, f'Рейтинг: {answer}')
    do_again(message)


def do_again(message):
    bot.send_message(message.chat.id, 'Вы можете отправить ещё один файл')

@bot.message_handler(content_types=['document'])
def answer(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_message(message.chat.id, 'Анализируем...\n'
                                      'Пожалуйста, не отправляйте новые файлы, пока анализ не будет завершён')

    if 'txt' == file_name.split('.')[1]:
        answer = spacy_ml.predict_text(downloaded_file.decode())
        bot.send_message(message.chat.id,  f'Рейтинг: {answer}')
        do_again(message)
    elif 'csv' == file_name.split('.')[1]:        
        answer_data = spacy_ml.predict_csv(downloaded_file.decode())
        # csv module can write data in io.StringIO buffer only
        s = io.StringIO()
        writer = csv.writer(s, delimiter=";")
        writer.writerow(('Id','Категория','Уровень рейтинга'))
        writer.writerows(answer_data)
        s.seek(0)
        # python-telegram-bot library can send files only from io.BytesIO buffer
        # we need to convert StringIO to BytesIO
        buf = io.BytesIO()

        # extract csv-string, convert it to bytes and write to buffer
        buf.write(s.getvalue().encode())
        buf.seek(0)

        # set a filename with file's extension
        buf.name = f'answer{message.id}.csv'
        bot.send_document(message.chat.id, document=buf)
        do_again(message)
    elif 'xlsx' == file_name.split('.')[1]:        
        src = file_name
        with open("files/" + src, 'wb') as new_file:
            new_file.write(downloaded_file)
        answer_data = spacy_ml.predict_xlsx(f'files/{file_name}')
        # csv module can write data in io.StringIO buffer only
        s = io.StringIO()
        writer = csv.writer(s, delimiter=";")
        writer.writerow(('Id','Категория','Уровень рейтинга'))
        writer.writerows(answer_data)
        s.seek(0)
        # python-telegram-bot library can send files only from io.BytesIO buffer
        # we need to convert StringIO to BytesIO
        buf = io.BytesIO()

        # extract csv-string, convert it to bytes and write to buffer
        buf.write(s.getvalue().encode())
        buf.seek(0)

        # set a filename with file's extension
        buf.name = f'answer{message.id}.csv'
        bot.send_document(message.chat.id, document=buf)
        do_again(message)
    else:
        bot.send_message(message.chat.id, 'Неизвестный формат файла. Пожалуйста, отправьте .txt или .csv')



if __name__ == '__main__':
    my_downloads.load()
    while True:
        try:
            bot.polling(none_stop=True)
        except ():
            time.sleep(5)