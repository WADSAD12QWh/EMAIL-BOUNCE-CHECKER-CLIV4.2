# ===========> DON'T CHANGE THIS
# SCRIPT : VALIDATOR BOUNCE
# VERSION : 4.2
# TELEGRAM AUTHOR : https://t.me/zlaxtert
# SITE : https://darkxcode.site/
# TEAM : DARKXCODE
# ================> END

import requests
import threading
import time
import os
import json
import configparser
from colorama import Fore, Back, Style, init
from queue import Queue
from urllib.parse import quote

# Initialize colorama
init(autoreset=True)

# Colors
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
kuning = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX
cyan = Fore.CYAN
reset = Fore.RESET
bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
res = Style.RESET_ALL
yl = Fore.YELLOW
cy = Fore.CYAN
mg = Fore.MAGENTA
bc = Back.GREEN
fr = Fore.RED
sr = Style.RESET_ALL
fb = Fore.BLUE
fc = Fore.LIGHTCYAN_EX
fg = Fore.GREEN
br = Back.RED

# Banner
banner = f"""{hijau}
                                 /           /                          
                                /' .,,,,  ./ \\                           
                               /';'     ,/  \\                                
                              / /   ,,//,'''                         
                             ( ,, '_,  ,,,' ''                 
                             |    /{merah}@{hijau}  ,,, ;' '               
                            /    .   ,''/' ',''       
                           /   .     ./, ',, ' ;                      
                        ,./  .   ,-,',' ,,/''\\,'                 
                       |   /; ./,,'',,'' |   |                                               
                       |     /   ','    /    |                                               
                        \\___/'   '     |     |                                               
                         ',,'  |      /     '\\                                              
                              /  (   |   )    ~\\            
                             '   \\   (    \\     \\~            
                             :    \\                \\                                                 
                              ; .         \\--                                                  
                               :   \\         ; {magenta}                                                 
,------.    ,---.  ,------. ,--. ,--.,--.   ,--. ,-----.  ,-----. ,------.  ,------. 
|  .-.  \\  /  O  \\ |  .--. '|  .'   / \\  `.'  / '  .--./ '  .-.  '|  .-.  \\ |  .---' 
|  |  \\  :|  .-.  ||  '--'.'|  .   '   .'    \\  |  |     |  | |  ||  |  \\  :|  `--,  
|  '--'  /|  | |  ||  |\\  \\ |  |\\   \\ /  .'.  \\ '  '--'\\ '  '-'  '|  '--'  /|  `---. 
`-------' `--' `--'`--' '--'`--' '--''--'   '--' `-----'  `-----' `-------' `------' {reset}
{fr}       ===================================================================={reset}
                  |{fb} SCRIPT{reset}  :{fg} VALIDATOR BOUNCE               {reset} |
                  |{fb} VERSION{reset} :{fg} 4.2{reset}                             |
                  |{fb} AUTHOR {reset} :{fg} https://t.me/zlaxtert{reset}           |
{fr}       ===================================================================={reset}
"""


class BounceValidator:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load_config()
        self.lists_queue = Queue()
        self.proxies = []
        self.live_count = 0
        self.die_count = 0
        self.total_count = 0
        self.checked_count = 0
        self.lock = threading.Lock()
        self.threads_count = 0
        
    def load_config(self):
        """Reading configuration from settings.ini"""
        if not os.path.exists('settings.ini'):
            self.create_default_config()
        self.config.read('settings.ini')
        
        # Validate required settings
        if self.config['SETTINGS']['APIKEY'] == 'PASTE_YOUR_API_KEY_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API key in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        elif self.config['SETTINGS']['API'] == 'PASTE_YOUR_API_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        elif self.config['SETTINGS']['PROXY_AUTH'] == 'PASTE_YOUR_PROXY_AUTH_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your PROXY AUTH in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}")
            print(f"{res}[{yl}!{res}]{fb} If your proxy does not use Authentication, then leave the PROXY AUTH section in the {yl}settings.ini{fb} file blank {res}[{yl}!{res}]{fb}\n\n")
            exit()
        
    def create_default_config(self):
        """Creating a default configuration file"""
        self.config['SETTINGS'] = {
            'APIKEY': 'PASTE_YOUR_API_KEY_HERE',
            'API': 'PASTE_YOUR_API_HERE',
            'PATCH': '/validator/bounceV4/',
            'PROXY_AUTH': 'PASTE_YOUR_PROXY_AUTH_HERE',
            'TYPE_PROXY': 'http'
        }
        
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
            
        # Create a results folder
        os.makedirs('result', exist_ok=True)
    
    def load_lists(self, filename):
        """Loading email list from file"""
        if not os.path.exists(filename):
            print(f"{res}[{yl}!{res}]{fb} File {fg}{filename}{res}{fb} not found {res}[{yl}!{res}]{fb}")
            return False
            
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                item = line.strip()
                if item:
                    self.lists_queue.put(item)
                    
        self.total_count = self.lists_queue.qsize()
        print(f"{res}[{yl}!{res}]{fb} Successfully loaded {fg}{self.total_count}{res}{fb} lists from {fc}{filename} {res}[{yl}!{res}]{fb}")
        return True
        
    def load_proxies(self, filename):
        """Loading proxy list from file"""
        if not os.path.exists(filename):
            print(f"{res}[{yl}!{res}]{fb} File {fg}{filename}{res}{fb} not found {res}[{yl}!{res}]{fb}")
            return False
            
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    self.proxies.append(proxy)
                    
        print(f"{res}[{yl}!{res}]{fb} Successfully loaded {fg}{len(self.proxies)}{res}{fb} proxies {res}[{yl}!{res}]{fb}")
        return True
        
    def validate_item(self, item, proxy_index=0):

        
        """Validate a single item using the API"""
        apikey = self.config['SETTINGS']['APIKEY']
        api_url = self.config['SETTINGS']['API']
        patch_url = self.config['SETTINGS']['PATCH']
        proxy_auth = self.config['SETTINGS']['PROXY_AUTH']
        type_proxy = self.config['SETTINGS']['TYPE_PROXY']
        
        endpoint = api_url + patch_url
        
        # Set up parameters
        params = {
            'list': item,
            'apikey': apikey,
        }
        # Headers 
        headers = {
            'Accept': 'text/plain',
            "Content-Type": "application/x-www-form-urlencoded",  # untuk parameter query
            'Cookie': '_ga=GA1.1.377070463.1743832930; _tt_enable_cookie=1; _ttp=01JR29DZA0CSTVK88N5ZK5SM53_.tt.1; _gcl_au=1.1.943685857.1752070151; _ga_EL2XR9DXKK=GS2.1.s1755331914$o6$g1$t1755333799$j60$l0$h0; first_visit_date=2025-08-29+00%3A00%3A00+%2B0000; client_first_visit_date=true; _sp_id.70b7=aac48f9b-0bed-4bb2-b3aa-fc9ac357ad11.1756439806.4.1756495083.1756467836.15e4ea5c-4020-4928-8bc2-ea52f934c761',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        }
        
        # Add proxy if available
        if self.proxies:
            proxy = self.proxies[proxy_index % len(self.proxies)]
            params['proxy'] = proxy
            params['type_proxy'] = type_proxy
            
            # Add auth proxy if available
            if proxy_auth and proxy_auth != 'PASTE_YOUR_PROXY_AUTH_HERE':
                params['proxyAuth'] = proxy_auth
                
                proxies = f"{type_proxy}://{proxy_auth}@{proxy}"
        else : 
            params['proxy'] = ""
            params['type_proxy'] = "http"
        try:        
            time.sleep(2)
            response = requests.get(endpoint, params=params, timeout=30)
            data = json.loads(response.text)
            
            
            if 'data' in data and 'info' in data['data']:
                info = data['data']['info']
                details = info.get('details', {})
                
                # Handle different response structures
                if 'valid' in details :
                    valid = details['valid']
                    mx_record = details.get('mx_record', 'N/A')
                    provider = details.get('provider', 'N/A')
                    score = details.get('score', 0)
                    result = details.get('result', 'N/A')
                    reason = details.get('reason', 'N/A')
                    statistic = details.get('statistic', 'UNKNOWN')
                    msg = info.get('msg', 'UNKNOWN')
                    
                    result_line = f"{reason.upper()} | {item} | VALID : {valid} | MX RECORD : {mx_record} | PROVIDER : {provider} | SCROEE : {score}"
                    
                    if valid == True :
                        val = f"{hijau}{valid}{reset}"
                    else :
                        val = f"{merah}{valid}{reset}"
                    # Save results based on status
                    if reason.upper() == "LIVE":
                        with self.lock:
                            self.live_count += 1
                        self.save_result(f'result/LIVE.txt', result_line)
                        status = "LIVE"
                        stats = f"{hijau}{status.upper()}{reset}"
                    elif reason.upper() == "LIVE RISKY":
                        with self.lock:
                            self.live_count += 1
                        self.save_result(f'result/LIVE.txt', result_line)
                        status = "LIVE"
                        stats = f"{hijau}{status.upper()}{reset}"
                    elif reason.upper() == "LIVE DELIVERABLE":
                        with self.lock:
                            self.live_count += 1
                        self.save_result(f'result/LIVE.txt', result_line)
                        status = "LIVE"
                        stats = f"{hijau}{status.upper()}{reset}"
                    
                    else:
                        with self.lock:
                            self.die_count += 1
                        self.save_result(f'result/DIE.txt', item)
                        status = "DIE"
                        stats = f"{merah}{status.upper()}{reset}"
                        
                    # Show results
                    with self.lock:
                        self.checked_count += 1
                        
                    # Display progress
                    progress = f" {yl}Checked{res} | {hijau}LIVE: {self.live_count}{res} | {merah}DIE: {self.die_count}{res} | {res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]"
                    print(f"{progress}{res} -{yl} {item}{res} -> {stats} | {magenta}VALID{reset} : {val} |{cyan} BY DARKXCODE V4.2{reset}")
                          
                else:
                    # Handle case where details structure is different
                    with self.lock:
                        self.die_count += 1
                        self.checked_count += 1
                    
                    progress = f" {yl}Checked{res} | {hijau}LIVE: {self.live_count}{res} | {merah}DIE: {self.die_count}{res} |  {res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]"
                    self.save_result(f'result/DIE.txt', item)
                    print(f"{progress}{res} -{yl} {item}{res} -> {merah}DIE{reset} | {white}{info.get('msg', 'INVALID RESPONSE STRUCTURE!')}{res} |{cyan} BY DARKXCODE V4.2{reset}")
                    
            else:
                # Handle case where details structure is different
                with self.lock:
                    self.die_count += 1
                    self.checked_count += 1
                    
                self.save_result(f'result/ERROR.txt', item + " | INVALID RESPONSE")
                print(f"{res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]{res} -{yl} {item}{res} -> {white}ERROR{reset} | {merah}INVALID RESPONSE{res} |{cyan} BY DARKXCODE V4.2{reset}")

                
        except Exception as e:
            # Handle case where details structure is different
            with self.lock:
                self.die_count += 1
                self.checked_count += 1
                    
            self.save_result(f'result/ERROR.txt', item + " | VALIDATION ERROR")
            #self.save_result(f'result/ress.txt', response.text)
            print(f"{res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]{res} -{yl} {item}{res} -> {white}ERROR{reset} | {merah}VALIDATION ERROR{res} |{cyan} BY DARKXCODE V4.2{reset}")
            
    def save_result(self, filename, data):
        """Save results to file"""
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(data + '\n')
        except Exception as e:
            print(f"{res}[{yl}!{res}]{fb} Error saving to {filename}: {str(e)} {res}[{yl}!{res}]{fb}")
            
    def worker(self):
        """Worker thread to process validation"""
        proxy_index = 0
        while True:
            try:
                item = self.lists_queue.get_nowait()
            except:
                break
                
            self.validate_item(item, proxy_index)
            proxy_index += 1
            self.lists_queue.task_done()
            
    def print_stats(self):
        """Print statistics during execution"""
        while not self.lists_queue.empty() or threading.active_count() > 1:
            with self.lock:
                checked = self.checked_count
                live = self.live_count
                die = self.die_count
                total = self.total_count
            
            
            #time.sleep(1)
            
    def run(self):
        """Running validation process"""
        # Input file lists
        lists_file = input(f"{res}[{yl}+{res}]{fb} Enter Email lists file{fg} >> {fb}").strip()
        if not self.load_lists(lists_file):
            return
            
        # Input proxy file
        proxy_file = input(f"{res}[{yl}+{res}]{fb} Enter Proxy lists file (press Enter to skip){fg} >> {fb}").strip()
        if proxy_file and not self.load_proxies(proxy_file):
            return
            
        # Input number of threads
        try:
            self.threads_count = int(input(f"{res}[{yl}+{res}]{fb} Enter number of Threads (5-25) (Recommended 5-10){fg} >> {fb}").strip() or "5")
            self.threads_count = max(5, min(25, self.threads_count))  # Limit between 5-25
        except ValueError:
            print(f"{res}[{yl}!{res}]{fb} Invalid number of threads, using default 5 threads {res}[{yl}!{res}]{fb}")
            self.threads_count = 5
            
        # Make sure the result folder exists
        os.makedirs('result', exist_ok=True)
        print(f"\n{yl}RUNING API FROM {fg}{self.config['SETTINGS']['API']}{res}")
        print(f"{yl}USE PATCH API {fg}{self.config['SETTINGS']['PATCH']}{res}")
        print(f"{fr}={res}" * 60)
        print(f"{yl}Starting validation with {fg}{self.threads_count}{yl} threads{res}")
        print(f"{fr}={res}" * 60)
        
        start_time = time.time()
        
        # Create and run threads
        threads = []
        for i in range(self.threads_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Start stats thread
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()
            
        # Wait for all threads to finish
        self.lists_queue.join()
        
        # Small delay to ensure all threads complete
        time.sleep(2)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n{fr}={res}" * 60)
        print(f"Checking completed! Live: {fg}{self.live_count}{res} | Die: {fr}{self.die_count}{res}")
        print(f"Time taken: {elapsed_time:.2f} seconds")
        print(f"{res}[{yl}!{res}]{fb} Results saved in 'result' folder {res}[{yl}!{res}]{fb}")
        print(f"{fr}={res}" * 60)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    validator = BounceValidator()
    validator.run()