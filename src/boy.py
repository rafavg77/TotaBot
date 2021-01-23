import logging
from requests.models import Response
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from Utils.getPublicInfo import GetPublicIP
from Utils.getSpeedTest import GetSpeed
from Utils.getPiHole import *
from configparser import ConfigParser
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)#logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'Utils/config/config.ini')
config = ConfigParser()
config.read(initfile)
token_bot = config.get('auth', 'token_bot')


def start(bot, update):
    logger.info('I have received a /start command')
    bot.message.reply_text("Hi Master, I'm here to server you!! ")
                            #reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def ping(bot, update):
    logger.info('I have received a /ping command')
    bot.message.reply_text("Pong !!")

def publicip(bot, update):
    logger.info('I have received a /publicip command')
    info = GetPublicIP()
    response = "Public IP: " + info.publicIP.ip + "\nCity: " + info.publicIP.city + "\nRegion: " + info.publicIP.region + "\nCountry: " + info.publicIP.country + "\nOrg: " + info.publicIP.org
    bot.message.reply_text(response)

def getspeed(bot, update):
    logger.info('I have received a /getspeed command')
    speed = GetSpeed()
    response = "Ping: " + speed.ping + "\nDonwload: " + speed.speedTestInfo.download + "\nUpload: " + speed.speedTestInfo.upload
    bot.message.reply_text(response)

def piholestatus(bot, update):
    logger.info('I have received a /piholestatus command')
    statusHole = getHoleStatus()
    bot.message.reply_text("PiHole Status: " + statusHole)

def pihodisable(bot, update):
    logger.info('I have received a /pihodisable command')
    setHoleDisable()
    bot.message.reply_text("Setting PiHole: Disable")

def piholeenable(bot, update):
    logger.info('I have received a /piholeenable command')
    setHoleEnable()
    bot.message.reply_text("Setting PiHole: Enable")

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
    
    updater.start_polling()
    updater.idle()