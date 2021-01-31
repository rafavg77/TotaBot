from configparser import ConfigParser
import logging
import requests
import json
import os 
import time

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config/config.ini')
config = ConfigParser()
config.read(initfile)

USERNAME = config.get('firewall',"fw_user")
PASSWORD = config.get('firewall',"fw_passwd")
BASE_URL = config.get('firewall','fw_url')
FW_HEADERS = {"Origin":"{}".format(BASE_URL),"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Totaman Browser/5.0 (X11; Linux x86_64) Totaman WebKit/537.36 (KHTML, like Gecko) TotaChrome/88.0.4324.96 Safari/537.36","Referer": "{}".format(BASE_URL)+"/webpages/login.html","Connection":"close","DNT":"1","Accept-Encoding":"gzip, deflate","Accept-Language":"es-MX,es;q=0.9","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class FirewallApi:

    def __init__(self):
            logger.info("Let's do This :D")

    def disableWan(self,wan_interface):
        self.login()
        self.getStatus2()
        self.disableWanInterface(wan_interface)
        time.sleep(3)
        self.getStatus2()
        #self.viewRoutes()
        #self.getWanStatus()
        self.logout()
    
    def enableWan(self,wan_interface):
        self.login()
        self.getStatus2()
        self.enableWanInterface(wan_interface)
        time.sleep(3)
        self.getStatus2()
        #self.viewRoutes()
        #self.getWanStatus()
        self.logout()

    def login(self):

        SESSION = requests.Session()
        paramsGet = {"form":"login"}
        paramsPost = {"data":"{\"method\":\"login\",\"params\":{\"username\": %s,\"password\":%s}}" % (USERNAME, PASSWORD)}
        headers = FW_HEADERS
        response = SESSION.post(BASE_URL+"/cgi-bin/luci/;stok=/login", data=paramsPost, params=paramsGet, headers=headers)

        logger.info("Status code:   %i" % response.status_code)
        logger.info("Response body: %s" % response.content)

        stok=json.loads(response.content)
        responseSotk=stok["result"]["stok"]
        Setcookie=response.cookies.get_dict()
        logger.info(Setcookie)

        self.responseSotk = responseSotk
        self.Setcookie = Setcookie

    def getStatus2(self):
        session = requests.Session()

        paramsGet = {"form":"status2"}
        paramsPost = {"data":"{\"method\":\"get\"}"}
        headers = FW_HEADERS
        cookies = self.Setcookie
        response = session.post(BASE_URL+"/cgi-bin/luci/;stok={}/admin/interface".format(self.responseSotk), data=paramsPost, params=paramsGet, headers=headers, cookies=cookies)

        logger.info("Response  Status2 body: %s" % response.content)

    def viewRoutes(self):
        SESSION = requests.Session()
        paramsGet = {"form":"policy_route"}
        paramsPost = {"data":"{\"method\":\"get\",\"params\":{}}"}
        headers = FW_HEADERS
        cookies = self.Setcookie
        response = SESSION.post(BASE_URL+"/cgi-bin/luci/;stok={}/admin/policy_route".format(self.responseSotk), data=paramsPost, params=paramsGet, headers=headers, cookies=cookies)

        logger.info("Status code:   %i" % response.status_code)
        logger.info("Response body: %s" % response.content)
        resultado = json.loads(response.content)
        return(resultado)

    def logout(self):
        SESSION = requests.Session()
        paramsGet = {"form":"logout"}
        paramsPost = {"data":"{\"method\":\"set\"}"}
        headers = FW_HEADERS
        cookies = self.Setcookie
        response = SESSION.post(BASE_URL+"/cgi-bin/luci/;stok={}/admin/system".format(self.responseSotk), data=paramsPost, params=paramsGet, headers=headers, cookies=cookies)
        
        logger.info("Cerrando Sesion")
        logger.info("Status code:   %i" % response.status_code)
        logger.info("Response body: %s" % response.content)

    def getWanStatus(self):
        session = requests.Session()
        paramsGet = {"form":"status"}
        paramsPost = {"data":"{\"method\":\"get\",\"params\":{\"wan_id\":1,\"proto\":\"dhcp\"}}"}
        headers = FW_HEADERS
        cookies = self.Setcookie
        response = session.post(BASE_URL+"/cgi-bin/luci/;stok={}/admin/interface_wan".format(self.responseSotk), data=paramsPost, params=paramsGet, headers=headers, cookies=cookies)

        logger.info("Status code:   %i" % response.status_code)
        logger.info("Response body: %s" % response.content)

    def disableWanInterface(self,wan_interface):
        session = requests.Session()

        paramsGet = {"form":"disconnect"}
        paramsPost = {"data":"{\"method\":\"set\",\"params\":{\"wan_id\":%s}}" % (wan_interface)}
        headers = FW_HEADERS
        cookies = self.Setcookie
        response = session.post(BASE_URL+"/cgi-bin/luci/;stok={}/admin/interface_wan".format(self.responseSotk), data=paramsPost, params=paramsGet, headers=headers, cookies=cookies)

        logger.info("Status code:   %i" % response.status_code)
        logger.info("Response body: %s" % response.content)
    
    def enableWanInterface(self,wan_interface):
        session = requests.Session()

        paramsGet = {"form":"connect"}
        paramsPost = {"data":"{\"method\":\"set\",\"params\":{\"wan_id\":%s}}" % (wan_interface)}
        headers = FW_HEADERS
        cookies = self.Setcookie
        response = session.post(BASE_URL+"/cgi-bin/luci/;stok={}/admin/interface_wan".format(self.responseSotk), data=paramsPost, params=paramsGet, headers=headers, cookies=cookies)

        logger.info("Status code:   %i" % response.status_code)
        logger.info("Response body: %s" % response.content)

#fw = FirewallApi()
#fw.disableWan()