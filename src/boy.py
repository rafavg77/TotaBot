import logging
from requests.models import Response
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from Utils.getPublicInfo import GetPublicIP
from Utils.getSpeedTest import GetSpeed
from Utils.getPiHole import *
from Utils.firewallUtil import *
from configparser import ConfigParser
import time
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)#logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'Utils/config/config.ini')
config = ConfigParser()
config.read(initfile)
token_bot = config.get('auth', 'token_bot')
bad_permission = config.get('users', 'reply')


def isPermited(bot, update):
    id = bot.message.chat.id
    PERMITED_USERS = config.get('users',"permited")
    if str(id) in PERMITED_USERS:
        permission = True
    else:
        permission = False
        bot.message.reply_text(bad_permission)

    return permission 

def start(bot, update):
    if isPermited(bot, update):
        logger.info('I have received a /start command')
        bot.message.reply_text("Hi Master, I'm here to server you!! ")
                            #reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def ping(bot, update):
    logger.info('I have received a /ping command')
    if isPermited(bot, update):
        bot.message.reply_text("Pong !!")

def publicip(bot, update):
    logger.info('I have received a /publicip command')
    if isPermited(bot, update):
        info = GetPublicIP()
        response = "Public IP: " + info.publicIP.ip + "\nCity: " + info.publicIP.city + "\nRegion: " + info.publicIP.region + "\nCountry: " + info.publicIP.country + "\nOrg: " + info.publicIP.org
        bot.message.reply_text(response)

def getspeed(bot, update):
    logger.info('I have received a /getspeed command')
    if isPermited(bot, update):
        speed = GetSpeed()
        response = "Ping: " + speed.ping + "\nDonwload: " + speed.speedTestInfo.download + "\nUpload: " + speed.speedTestInfo.upload
        bot.message.reply_text(response)

def piholestatus(bot, update):
    logger.info('I have received a /piholestatus command')
    if isPermited(bot, update):
        statusHole = getHoleStatus()
        bot.message.reply_text("PiHole Status: " + statusHole)

def pihodisable(bot, update):
    logger.info('I have received a /pihodisable command')
    if isPermited(bot, update):
        setHoleDisable()
        bot.message.reply_text("Setting PiHole: Disable")

def piholeenable(bot, update):
    logger.info('I have received a /piholeenable command')
    if isPermited(bot, update):
        setHoleEnable()
        bot.message.reply_text("Setting PiHole: Enable")

def fwGetInterfaces(bot, update):
    logger.info('I have received a /fwGetInterfaces command')
    if isPermited(bot, update):
        fw = FirewallApi()
        status = fw.getAllWANStatus()
        print(status)
        bot.message.reply_text("Firwall Interfaces: " + status)

def fwEnableWAN(bot, update):
    logger.info('I have received a /fwEnableWAN command')
    if isPermited(bot, update):
        wanInterface = bot.message.text.replace("/fwEnableWAN", "").strip()
        print(wanInterface)
        if int(wanInterface) < 3:    
            fw = FirewallApi()
            status = fw.enableWan(int(wanInterface))
            time.sleep(10)
            bot.message.reply_text("Firwall Enabling WAN: " + wanInterface)
        else:
            bot.message.reply_text("Wrong Interface Number")

def fwDisableWAN(bot, update):
    logger.info('I have received a /fwDisableWAN command')
    if isPermited(bot, update):
        wanInterface = bot.message.text.replace("/fwDisableWAN", "").strip()
        if int(wanInterface) < 3:    
            fw = FirewallApi()
            status = fw.disableWan(int(wanInterface))
            time.sleep(10)
            bot.message.reply_text("Firwall Disabling WAN: " + wanInterface)
        else:
            bot.message.reply_text("Wrong Interface Number")

if __name__ == '__main__':

    updater = Updater(token=token_bot,use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('publicip', publicip))
    dispatcher.add_handler(CommandHandler('getspeed', getspeed))
    dispatcher.add_handler(CommandHandler('piholestatus', piholestatus))
    dispatcher.add_handler(CommandHandler('pihodisable', pihodisable))
    dispatcher.add_handler(CommandHandler('pihoenable', piholeenable))
    dispatcher.add_handler(CommandHandler('fwGetInterfaces', fwGetInterfaces))
    dispatcher.add_handler(CommandHandler('fwEnableWAN', fwEnableWAN))
    dispatcher.add_handler(CommandHandler('fwDisableWAN', fwDisableWAN))

    updater.start_polling()
    updater.idle()