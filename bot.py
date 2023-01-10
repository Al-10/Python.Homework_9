import telebot 
import random

bot = telebot.TeleBot('Вставьте ваш ТОКЕН')

candies: int
choise = []
chat_id: int


@bot.message_handler(commands=['start'])
def hello_commands(message):
    global chat_id
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Выбери команду '/start_game' или '/help'")


@bot.message_handler(commands=['start_game'])
def start_game_commands(message):
    global choice, candies
    candies = 117
    # chat_id = message.chat.id
    bot.send_message(chat_id, 'Условие игры: На столе лежит 117 конфета. Играют два игрока делая ход друг после друга.Первый ход определяется жеребьёвкой.За один ход можно забрать не более чем 28 конфет.Конфеты оппонента достаются сделавшему последний ход.')
    bot.send_message(chat_id, 'Начнем игру с конфетами! \n Давай определим кто первый делает ход?!' )
    players = ['Пользователь', 'Bot']
    choice = random.choice(players)
    msg = "Игру начнет {}".format(choice)
    bot.send_message(chat_id, msg)
    game()

@bot.message_handler(commands=['step'])
def step_commands(message):
    global candies, choice
    move = int(message.text.split()[1])
    if move > 0 and move < 29 and move <= candies:
        candies -= move
        if winner():
            bot.send_message(chat_id, "Выбери команду '/start_game' чтобы начать игру")
        else:
            msg = f'Осталось {candies}'
            bot.send_message(chat_id, msg)
            choice = "Bot"
            game()
    else:
        msg = 'Столько взять нельзя! \n Введите количество конфет после команды /step'
        bot.send_message(chat_id, msg)

def game():
    global choice
    global candies
    if choice == 'Пользователь':
        msg = 'Введите количество конфет после команды /step'
        bot.send_message(chat_id, msg)
    else:
        max = min([28, candies])
        move = random.randint(1, max)
        msg = f'Бот взял {move}'
        bot.send_message(chat_id, msg)
        candies -= move
        if winner():
            bot.send_message(chat_id, "Выбери команду '/start_game' чтобы начать игру")
        else:
            msg = f'Осталось {candies}'
            bot.send_message(chat_id, msg)
            choice = 'Пользователь'
            game()

def winner():
        if candies <= 0:
            msg = f'Поздравляю, выиграл {choice}!'
            bot.send_message(chat_id, msg)
            return True
        else:
            return False
        

def input_candies():
    global candies
    while True:
        msg = 'Введите количество конфет после команды /step'
        bot.send_message(chat_id, msg)

        move = int(input('Введите конфеты '))
        if move > 0 and move < 29 and move <= candies:
            candies -= move
            break
        else:
            print('Столько взять нельзя')


@bot.message_handler(commands=['help'])
def help_commands(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Чтобы выиграть игру необходимо перехватить инициативу у бота с нужным колличеством вытягиваемых конфет и дальше уравнивать до 29 в каждом ходе. А именно: конфеты_взял_бот + конфеты_взял_игрок = 29')



print('server start')
bot.infinity_polling()