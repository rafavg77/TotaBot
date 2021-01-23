import asyncio
import json
import re
import aiohttp
import sys
import os
from hole import Hole
from configparser import ConfigParser

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config/config.ini')
config = ConfigParser()
config.read(initfile)
token_dns = config.get('dns', 'token_dns')
url_dns = config.get('dns', 'url')

async def main():
    """Get the data from a *hole instance."""
    async with aiohttp.ClientSession() as session:
        data = Hole(url_dns, loop, session)
        await data.get_data()
        print("Status:", data.status)
        return data.status

async def disable():
    """Get the data from a *hole instance."""
    async with aiohttp.ClientSession() as session:
        data = Hole(url_dns, loop, session, api_token=token_dns)
        await data.disable()

async def enable():
    """Get the data from a *hole instance."""
    async with aiohttp.ClientSession() as session:
        data = Hole(url_dns, loop, session, api_token=token_dns)
        await data.enable()

loop = asyncio.get_event_loop()

def getHoleStatus():
    status = loop.run_until_complete(main())
    return status

def setHoleDisable():
    status = loop.run_until_complete(disable())
    return status

def setHoleEnable():
    status = loop.run_until_complete(enable())
    return status