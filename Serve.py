from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps

e = create_engine('sqlite:///proxies.db')

app = Flask(__name__)
api = Api(app)

class proxies(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('type', type = str, required = True, choices=('http', 'socks4', 'socks5'), help = 'No valid proxy type provided')
        self.reqparse.add_argument('limit', type = int, required = False, default = 1000)
        self.reqparse.add_argument('all', type = bool, default = False)
        super(proxies, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        if args['type'] == 'http':
            if args['all']:
                return http_proxies_all.get(object)
            else:
                return http_proxies.get(object, args['limit'])
        elif args['type'] == 'socks4':
            if args['all']:
                return socks4_proxies_all.get(object)
            else:
                return socks4_proxies.get(object, args['limit'])
        if args['type'] == 'socks5':
            if args['all']:
                return socks4_proxies_all.get(object)
            else:
                return socks4_proxies.get(object, args['limit'])


class statistics(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('type', type = str, choices=('http', 'socks4', 'socks5'), help = 'Invalid type provided')
        super(statistics, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        if args['type']:
            if args['type'] == 'http':
                return {'count': self.getHTTPCount()}
            if args['type'] == 'socks4':
                return {'count': self.getSOCKS4Count()}
            if args['type'] == 'socks5':
                return {'count': self.getSOCKS5Count()}
        else:
            res = {'http': self.getHTTPCount(), 'socks4': self.getSOCKS4Count(), 'socks5': self.getSOCKS5Count()}
            return res
    def getHTTPCount(self):
        conn = e.connect()
        query = conn.execute("select COUNT() from http")
        return [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor][0]['COUNT()']
    def getSOCKS4Count(self):
        conn = e.connect()
        query = conn.execute("select COUNT() from socks4")
        return [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor][0]['COUNT()']
    def getSOCKS5Count(self):
        conn = e.connect()
        query = conn.execute("select COUNT() from socks5")
        return [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor][0]['COUNT()']


class http_proxies_all(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from http")
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result
 
class http_proxies(Resource):
    def get(self, proxy_count):
        conn = e.connect()
        query = conn.execute("select * from http ORDER BY RANDOM() LIMIT '%s'" % proxy_count)
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result


class socks4_proxies_all(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from socks4")
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result

class socks4_proxies(Resource):
    def get(self, proxy_count):
        conn = e.connect()
        query = conn.execute("select * from socks4 ORDER BY RANDOM() LIMIT '%s'" % proxy_count)
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result


class socks5_proxies_all(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from socks5")
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result

class socks5_proxies(Resource):
    def get(self, proxy_count):
        conn = e.connect()
        query = conn.execute("select * from socks5 ORDER BY RANDOM() LIMIT '%s'" % proxy_count)
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result

api.add_resource(proxies, '/api/proxies')
api.add_resource(statistics, '/api/stats')

api.add_resource(http_proxies_all, '/api/http/all')
api.add_resource(http_proxies, '/api/http/<int:proxy_count>')

api.add_resource(socks4_proxies_all, '/api/socks4/all')
api.add_resource(socks4_proxies, '/api/socks4/<int:proxy_count>')

api.add_resource(socks5_proxies_all, '/api/socks5/all')
api.add_resource(socks5_proxies, '/api/socks5/<int:proxy_count>')

if __name__ == '__main__':
    app.run()