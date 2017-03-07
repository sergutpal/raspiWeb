import globalVars
import telebot
import requests

telegramBot = None


def getTelegramToken():
    TOKEN = '320854606:AAGb95Vb9rax_pF8WZbXDIMXnzJSD1RbBP4'
    return TOKEN


def readTelegramBot(messages): 
    globalVars.toLogFile('msg bot Recibido')

    for message in messages: 
        cid = message.chat.id
    globalVars.toLogFile('[' + str(cid) + ']: ' + message.text)
    return True


def sendTelegramBot(chatid, msg):
    global telegramBot

    try:
        telegramBot.send_message(chatid, msg)
        globalVars.toLogFile('sendTelegramBot: ' + msg)
        return True
    except Exception as e:
        globalVars.toLogFile('Error sendTelegramBot: ' + str(e))
    return False


def initBot():
    global telegramBot

    try:
        telegramBot = telebot.TeleBot(getTelegramToken())
        telegramBot.set_update_listener(readTelegramBot)
        chatid = 89102745
        sendTelegramBot(chatid, 'Raspibot inicializado correctamente')    
        telegramBot.polling(none_stop=False, interval=1)
        globalVars.toLogFile('Todo ok')
        return True
    except Exception as e:
        globalVars.toLogFile('Error initBot: ' + str(e))
        return False


initBot()
 

