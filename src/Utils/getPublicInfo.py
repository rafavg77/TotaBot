from configparser import ConfigParser
import ipinfo
import os
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config/config.ini')
config = ConfigParser()
config.read(initfile)
token = config.get('auth', 'token_ipinfo')

class GetPublicIP:
    def __init__(self):
        self.publicIP = self.getIpInfo()

    def getIpInfo(self):
        handler = ipinfo.getHandler(token)
        details = handler.getDetails()
        ipInfo = ""
        ipinfo.ip = details.ip
        ipinfo.city = details.city
        ipinfo.region = details.region
        ipinfo.country = details.country
        ipinfo.org = details.org
        return ipinfo

#GetPublicIP()