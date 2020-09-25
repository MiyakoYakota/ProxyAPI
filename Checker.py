from sqlalchemy import create_engine
import requests
import time
from datetime import datetime
from multiprocessing import Pool
from multiprocessing import freeze_support # Windows Support

e = create_engine('sqlite:///proxies.db')
# --------------------------------------------------------------------------------------------
def getAllHTTP():
    conn = e.connect()
    query = conn.execute("select * from http")
    result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
    return result

def getAllSOCKS4():
    conn = e.connect()
    query = conn.execute("select * from socks4")
    result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
    return result

def getAllSOCKS5():
    conn = e.connect()
    query = conn.execute("select * from socks5")
    result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
    return result
# --------------------------------------------------------------------------------------------
def checkAndWriteHTTP(proxy):
    proxyID = proxy['id']
    combo = proxy['proxy']
    print(f"Checking Proxy #{proxyID} - {combo}")
    try:
        response = requests.get('http://azenv.net/', proxies={"http": "http://"+combo}, timeout=15) # Send the data and assign the response to the variable response
        if "REMOTE_ADDR = " + combo.split(':')[0] in response.text:
            print(f"[Good Proxy] ID: {proxyID} - Combo: {combo}")
            conn = e.connect()
            conn.execute("UPDATE http SET lastChecked = '{checkedAt}' WHERE id = {id}".format(checkedAt=datetime.now().strftime(("%Y-%m-%d %H:%M:%S")), id=str(proxyID)))
            return True
        else:
            conn = e.connect()
            conn.execute("DELETE FROM http WHERE id = %s" % str(proxyID))
            print("Deleted Proxy " + str(proxyID))
            return False
    except:
        conn = e.connect()
        conn.execute("DELETE FROM http WHERE id = %s" % str(proxyID))
        print("Deleted Proxy " + str(proxyID))
        return False
# --------------------------------------------------------------------------------------------
def checkAndWriteSOCKS4(proxy):
    proxyID = proxy['id']
    combo = proxy['proxy']
    print(f"Checking Proxy #{proxyID} - {combo}")
    try:
        response = requests.get('http://azenv.net/', proxies={"http": "socks4://"+combo}, timeout=15) # Send the data and assign the response to the variable response
        if "REMOTE_ADDR = " + combo.split(':')[0] in response.text:
            print(f"[Good Proxy] ID: {proxyID} - Combo: {combo}")
            conn = e.connect()
            conn.execute("UPDATE socks4 SET lastChecked = '{checkedAt}' WHERE id = {id}".format(checkedAt=datetime.now().strftime(("%Y-%m-%d %H:%M:%S")), id=str(proxyID)))
            return True
        else:
            conn = e.connect()
            conn.execute("DELETE FROM socks4 WHERE id = %s" % str(proxyID))
            print("Deleted Proxy " + str(proxyID))
            return False
    except:
        conn = e.connect()
        conn.execute("DELETE FROM socks4 WHERE id = %s" % str(proxyID))
        print("Deleted Proxy " + str(proxyID))
        return False
# --------------------------------------------------------------------------------------------
def checkAndWriteSOCKS5(proxy):
    proxyID = proxy['id']
    combo = proxy['proxy']
    print(f"Checking Proxy #{proxyID} - {combo}")
    try:
        response = requests.get('http://azenv.net/', proxies={"http": "socks5://"+combo}, timeout=15) # Send the data and assign the response to the variable response
        if "REMOTE_ADDR = " + combo.split(':')[0] in response.text:
            print(f"[Good Proxy] ID: {proxyID} - Combo: {combo}")
            conn = e.connect()
            conn.execute("UPDATE socks5 SET lastChecked = '{checkedAt}' WHERE id = {id}".format(checkedAt=datetime.now().strftime(("%Y-%m-%d %H:%M:%S")), id=str(proxyID)))
            return True
        else:
            conn = e.connect()
            conn.execute("DELETE FROM socks5 WHERE id = %s" % str(proxyID))
            print("Deleted Proxy " + str(proxyID))
            return False
    except:
        conn = e.connect()
        conn.execute("DELETE FROM socks5 WHERE id = %s" % str(proxyID))
        print("Deleted Proxy " + str(proxyID))
        return False
# --------------------------------------------------------------------------------------------
def main():
    all_http_proxies = getAllHTTP()
    all_socks4_proxies = getAllSOCKS4()
    all_socks5_proxies = getAllSOCKS5()
    freeze_support()
    numThreads = 400
    
    pool = Pool(int(numThreads))
    pool.map(checkAndWriteHTTP, all_http_proxies)
    print("Checked " + str(len(all_http_proxies)) + " HTTP Proxies")
    time.sleep(5)
    pool.map(checkAndWriteSOCKS4, all_socks4_proxies)
    print("Checked " + str(len(all_socks4_proxies)) + " SOCKS4 Proxies")
    #time.sleep(5)
    pool.map(checkAndWriteSOCKS5, all_socks5_proxies)
    print("Checked " + str(len(all_socks5_proxies)) + " SOCKS5 Proxies")

if __name__ == "__main__":
    main()
