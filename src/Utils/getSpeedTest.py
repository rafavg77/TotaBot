import re
import sys
import subprocess
import speedtest

class GetSpeed:
    def __init__(self):
        self.speedTestInfo = self.getSpeedTest()

    def getSpeedTest(self):
        response = subprocess.Popen('/home/tota77/Developer/Bots/TotaBot/venv/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
        download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
        upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

        ping2 = ping[0].replace(',', '.')
        download2 = download[0].replace(',', '.')
        upload2 = upload[0].replace(',', '.')

        """
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        #return res["download"], res["upload"], res["ping"]
        """
        
        self.ping = ping2
        self.download = download2
        self.upload = upload2

        return self