import requests
import logging

class ProxyManager:
    def __init__(self):
        self.proxies = [
            "http://104.207.43.119:3128", "http://104.167.26.235:3128", "http://104.167.31.222:3128",
            "http://104.167.26.72:3128", "http://104.207.34.211:3128", "http://104.207.34.92:3128",
            "http://104.207.52.205:3128", "http://104.207.41.203:3128", "http://104.207.36.133:3128",
            "http://104.207.49.194:3128", "http://104.207.47.78:3128", "http://104.207.54.82:3128",
            "http://104.207.51.11:3128", "http://104.207.55.92:3128", "http://104.207.62.121:3128",
            "http://104.207.51.130:3128", "http://104.207.38.20:3128", "http://104.207.60.157:3128",
            "http://104.207.61.76:3128", "http://104.207.63.110:3128", "http://104.207.49.86:3128",
            "http://104.167.26.35:3128", "http://104.207.57.75:3128", "http://104.207.49.227:3128",
            "http://104.207.48.48:3128", "http://104.207.40.80:3128", "http://104.207.52.94:3128",
            "http://104.167.30.133:3128", "http://104.207.42.35:3128", "http://104.207.56.210:3128",
            "http://104.207.49.249:3128", "http://104.207.32.52:3128", "http://104.207.49.47:3128",
            "http://104.207.54.42:3128", "http://104.207.54.94:3128", "http://104.167.31.102:3128",
            "http://104.207.55.199:3128", "http://104.207.58.61:3128", "http://104.207.45.213:3128",
            "http://104.207.46.92:3128", "http://104.167.24.41:3128", "http://104.207.53.102:3128",
            "http://104.207.49.102:3128", "http://104.167.29.153:3128", "http://104.207.38.134:3128",
            "http://104.207.54.69:3128", "http://104.167.26.221:3128", "http://104.207.34.40:3128",
            "http://104.207.33.241:3128", "http://104.207.44.150:3128", "http://104.167.29.94:3128",
            "http://104.207.56.4:3128", "http://104.207.36.167:3128", "http://104.207.37.79:3128",
            "http://104.207.37.101:3128", "http://104.207.56.29:3128", "http://104.207.35.23:3128",
            "http://104.207.63.145:3128", "http://104.207.61.206:3128", "http://104.207.40.153:3128",
            "http://104.167.24.164:3128", "http://104.207.51.218:3128", "http://104.207.37.22:3128",
            "http://104.167.26.183:3128", "http://104.207.52.178:3128", "http://104.207.63.181:3128",
            "http://104.167.25.173:3128", "http://104.207.37.87:3128", "http://104.207.36.135:3128",
            "http://104.207.36.112:3128", "http://104.207.45.127:3128", "http://104.167.27.202:3128",
            "http://104.207.57.184:3128", "http://104.207.51.184:3128", "http://104.167.27.138:3128",
            "http://104.207.37.159:3128", "http://104.207.63.41:3128", "http://104.207.58.20:3128",
            "http://104.167.27.77:3128", "http://104.207.42.61:3128", "http://104.207.50.220:3128",
            "http://104.167.28.99:3128", "http://104.207.40.169:3128", "http://104.207.43.151:3128",
            "http://104.167.30.68:3128", "http://104.167.27.72:3128", "http://104.207.60.50:3128",
            "http://104.207.44.241:3128", "http://104.207.36.154:3128", "http://104.167.28.246:3128",
            "http://104.207.59.93:3128", "http://104.207.32.145:3128", "http://104.207.50.134:3128",
            "http://104.207.54.99:3128", "http://104.207.46.213:3128", "http://104.207.47.218:3128",
            "http://104.207.37.127:3128", "http://104.207.43.237:3128", "http://104.207.53.222:3128",
            "http://104.207.58.133:3128"
        ]
        self.proxy_usage = {proxy: 0 for proxy in self.proxies}

    def validate_proxy(self, proxy):
        try:
            response = requests.get('https://www.google.com', proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                logging.info(f'Proxy {proxy} is valid.')
                return True
        except Exception as e:
            logging.error(f'Proxy {proxy} is invalid: {e}')
        return False

    def get_next_proxy(self):
        for proxy, usage_count in sorted(self.proxy_usage.items(), key=lambda item: item[1]):
            if self.validate_proxy(proxy):
                self.proxy_usage[proxy] += 1
                return proxy
        
        logging.error("No valid proxies found after validation.")
        return None

    def invalidate_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logging.info(f'Removed proxy: {proxy}')