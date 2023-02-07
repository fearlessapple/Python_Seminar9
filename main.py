import random
import telebot
from telebot import types

bot = telebot.TeleBot("6108610097:AAHh3KIBA7sfK48AudD9hPpd5ABXUSKc-XY")


@bot.message_handler(commands=["button", "start"])
def button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Старт игры.")
    but2 = types.KeyboardButton("Завершить игру.")
    markup.add(but1)
    markup.add(but2)
    bot.send_message(message.chat.id, "Запуск игры 'КОНФЕТЫ'",
                     reply_markup=markup)


def start_bot(message):
    print("Старт игры!")
    global player, conf, conf_player
    print("Запуск сервера игры 'КОНФЕТЫ'.")
    bot.send_message(message.chat.id, "Условие задачи: На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга. Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет. Все конфеты оппонента достаются сделавшему последний ход.")
    conf = 2021
    player = random.randint(1, 2)
    text = "Первым играет игрок №" + str(player)
    bot.send_message(message.chat.id, text)
    conf_player = [0, 0]
    text = "Игрок №" + str(player) + \
        " - введи количество конфет которые ты возьмешь: "
    bot.send_message(message.chat.id, text)
    print("Первый ход игрока №", player)
    if player == 2:
        num = random.randint(1, 28)
        text = "Бот взял " + str(num) + " конфет"
        bot.send_message(message.chat.id, text)
        conf -= num
        conf_player[player-1] += num
        player = 1
        text = "На столе осталось " + str(conf) + " конфет"
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Ход переходит игроку № 1")
        bot.send_message(
            message.chat.id, "Игрок № 1 - введи количество конфет которые ты возьмешь: ")

def win_check(message):
    global player, conf, conf_player
    if conf <= 0:
        bot.send_message(message.chat.id, "Победа!")
        text = "Победил игрок №" + str(player)
        bot.send_message(message.chat.id, text)
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        print("Победа! Победил игрок №", player)
        end_game(message)

def bot_move(message):
    global player, conf, conf_player
    num = (conf - (conf//28)*28)-1
    if num == 0:
        num = random.randint(1, 28)
    if conf < 29:
        num = conf
    text = "Бот взял " + str(num) + " конфет"
    bot.send_message(message.chat.id, text)
    conf -= num
    win_check(message)
    conf_player[player-1] += num
    player = 1
    if conf > 0:
        text = "На столе осталось " + str(conf) + " конфет"
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Ход переходит игроку № 1")
        bot.send_message(
            message.chat.id, "Игрок № 1 - введи количество конфет которые ты возьмешь: ")
        print("Ход переходит игроку № 1")

def end_game(message):
    bot.send_message(
        message.chat.id, "Игра завершена. Перезапустите игру /start")
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    print("Игра завершена")

@bot.message_handler(content_types=["text"])
def controller(message):
    global player, conf, conf_player
    if message.text == "Старт игры.":
        start_bot(message)
    elif message.text == "Завершить игру.":
        end_game(message)
    elif conf > 0:
        if message.text.isdigit():
            num = int(message.text)
            if int(message.text) > 0 and int(message.text) < 29:
                conf -= num
                win_check(message)
                conf_player[player-1] += num
                if conf > 0:
                    if player == 2:
                        player = 1
                    else:
                        player = 2
                    text = "На столе осталось " + str(conf) + " конфет"
                    bot.send_message(message.chat.id, text)
                    text = "Ход переходит игроку № " + str(player)
                    bot.send_message(message.chat.id, text)
                    text = "Игрок №" + \
                        str(player) + \
                        " - введи количество конфет которые ты возьмешь: "
                    bot.send_message(message.chat.id, text)
                    print("Переход хода к игроку №", player)
                    if player == 2:
                        bot_move(message)
            else:
                bot.send_message(
                    message.chat.id, "* неверно! нужно ввести число от 1 до 28")
        else:
            bot.send_message(
                message.chat.id, "Вы ввели текст... Нужно ввести число! от 1 до 28")
    elif conf < 1:
        end_game(message)

print("ЗАПУСК")
bot.infinity_polling()