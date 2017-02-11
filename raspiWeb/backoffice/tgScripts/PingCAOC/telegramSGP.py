
import telebot
import requests

def sendTelegramBot(msg):
    try:
        TOKEN = '320854606:AAGb95Vb9rax_pF8WZbXDIMXnzJSD1RbBP4'
        tb = telebot.TeleBot(TOKEN)
        chatid = 89102745
        tb.send_message(chatid, msg)
        return True
    except Exception as e:
        # globalVars.toLogFile('Error sendTelegramBot: ' + str(e))
        print('Error sendTelegramBot: ' + str(e))
    return False


# print('antes URL')
# r = requests.get('curl -s -X POST https://api.telegram.org/bot320854606:AAGb95Vb9rax_pF8WZbXDIMXnzJSD1RbBP4/getMe  | jq .')
# print(r.json())

