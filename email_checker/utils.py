import time
import random

def random_delay(a, b):
    time.sleep(random.randint(a, b))


def get_random_proxies_for_session(proxy_count):
    all_proxies = []
    
    with open('data/proxies.txt') as fp:
        all_proxies = fp.read().splitlines()
    
    random.shuffle(all_proxies)
    proxies = all_proxies[:proxy_count]
    proxies = [proxy.strip() for proxy in proxies]  
    return proxies