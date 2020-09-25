# Hack to allow importing packages from parrent directories
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# Database imports
from Schema import Base, http, socks4, socks5
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///proxies.db')
Base.metadata.bind = engine # Bind the engine to the metadata of the Base class
DBSession = sessionmaker(bind=engine)
session = DBSession()
currentTime = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Proxy importing
http_dir = './input/http'
http_proxies = []

socks4_dir = './input/socks4'
socks4_proxies = []

socks5_dir = './input/socks5'
socks5_proxies = []

e = create_engine('sqlite:///proxies.db')
conn = e.connect()

## Import HTTP proxies from ./input/http
for root, dirs, files in os.walk(http_dir):
    for file in files:
        # read all lines from file
        file_line_list = [line.rstrip('\n') for line in open(os.path.join(root, file), 'r')]
        # append to proxy_list
        http_proxies.extend(file_line_list)

## Import SOCKS4 proxies from ./input/socks4
for root, dirs, files in os.walk(socks4_dir):
    for file in files:
        # read all lines from file
        file_line_list = [line.rstrip('\n') for line in open(os.path.join(root, file), 'r')]
        # append to proxy_list
        socks4_proxies.extend(file_line_list)

## Import SOCKS5 proxies from ./input/socks5
for root, dirs, files in os.walk(socks5_dir):
    for file in files:
        # read all lines from file
        file_line_list = [line.rstrip('\n') for line in open(os.path.join(root, file), 'r')]
        # append to proxy_list
        socks5_proxies.extend(file_line_list)
        


# Proxy loading
print("I am about to import proxies from their respective directories, this is what you want to do, right?")
input("Press enter to continue. ")
## Load HTTP proxies
for proxy in http_proxies:
    if proxy:
        try:
            http_proxy = http(proxy=proxy, ping=0, added=currentTime, lastChecked=currentTime)
            session.add(http_proxy)
        except:
            print("Failed to import proxy (duplicate?) " + proxy)
session.commit()
## Load SOCKS4 proxies
for proxy in socks4_proxies:
    if proxy:
        try:
            socks4_proxy = socks4(proxy=proxy, ping=0, added=currentTime, lastChecked=currentTime)
            session.add(socks4_proxy)
        except:
            print("Failed to import proxy (duplicate?) " + proxy)
session.commit()
## Load SOCKS5 proxies
for proxy in socks5_proxies:
    if proxy:
        try:
            socks5_proxy = socks5(proxy=proxy, ping=0, added=currentTime, lastChecked=currentTime)
            session.add(socks5_proxy)
        except:
            print("Failed to import proxy (duplicate?) " + proxy)
session.commit()