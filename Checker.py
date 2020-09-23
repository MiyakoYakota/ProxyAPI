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

# --------------------------------------------------------------------------------------------
def checkAndWriteHTTP(proxy):
    proxyID = proxy['id']
    combo = proxy['proxy']
    print(f"Checking Proxy #{proxyID} - {combo}")
    try:
        start = time.process_time()
        response = requests.get('http://azenv.net/', proxies={"http": "http://"+combo}, timeout=15) # Send the data and assign the response to the variable response
        end = time.process_time()
        if "REMOTE_ADDR = " + combo.split(':')[0] in response.text:
            print(f"[Good Proxy] ID: {proxyID} - Combo: {combo} - Ping: {str(end - start)}")
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
def main():
    all_http_proxies = getAllHTTP()
    freeze_support()
    numThreads = 400
    
    pool = Pool(int(numThreads))  # Start 4 threads
    pool.map(checkAndWriteHTTP, all_http_proxies) # Checky Checky

if __name__ == "__main__":
    main()
