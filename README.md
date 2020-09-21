# ProxyAPI
#### Welcome to ProxyAPI (WORK IN PROGRESS)
##### A lightweight cron-based proxy-dispensing REST API created fully in Python.

## What does this do?
As of now, the program will load proxies into ``proxies.db``, and then serve them using the REST API (Serve.py)

## Usage:
First time use and future use
### Setup:
  - Run ``pip install -r requirements.txt`` to install required libraries
  - Run ``python Schema.py`` to create the database where proxies will be stored
### Adding Proxies:
  - Put HTTP proxies in `input/http/`
  - Put SOCKS4 proxies in `input/socks4/`
  - Put SOCKS5 proxies in `input/socks5/`
  - Run `python LoadProxies.py`
### Serving Proxies:
  - Run the server ``python Serve.py``

## Questions:
Have any questions on how to use this program? Feel free to do any of the following:
  - [Open an issue](https://github.com/MiyakoYakota/ProxyAPI/issues/new).
  - Message me on Discord: Request#0002
  - Email me: <miyako@miyako.rocks>
