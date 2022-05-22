import httpx
import os
import time
from colorama import Fore, Style, init
import threading
import random
from threading import Lock

init()
s_print_lock = Lock()

tokens = []
proxies = []

spammed = 0

joined = 0
joined_captcha = 0
joined_locked = 0

checked_valid = 0
checked_invalid = 0
checked_locked = 0

sent_fr = 0
failed_fr = 0

class ChannelSpammer():
    def __init__(self, token, id, message):
        self.token = token
        self.id = id
        self.message = message

    def spam_channel(self):
        if ":" in self.token:
            self.token = self.token.split(":")[2]
        headers = { 
            "Host": "discord.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "X-Context-Properties": "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjczNTIzMDEyMjY5NjYzODU0NSIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5NzU3MDIyNjY1NTAwNTQ5NjIiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9",
            "Authorization": self.token,
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJkZSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAwLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTI5MjY4LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            "X-Discord-Locale": "en-US",
            "X-Debug-Options": "bugReporterEnabled",
            "Origin": "https://discord.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        global spammed
        with httpx.Client(headers=headers, proxies="http://" + random.choice(proxies)) as client:
            cookes_raw = str(client.get('https://discord.com/api/v9/users/@me').headers['set-cookie'])
            dcfduid = cookes_raw.split("__dcfduid=")[1].split("Expires=")[0]
            sdcfduid = cookes_raw.split("__sdcfduid=")[1].split("Expires=")[0]
            cookies = f"__dcfduid={dcfduid}__sdcfduid={sdcfduid} locale:en-US;"
            client.headers["Cookie"] = cookies
            response = client.post(f"https://discord.com/api/v9/channels/{self.id}/messages", json={"content": str(self.message)})
            if(response.status_code == 200):
                spammed += 1
                set_title(f"Spammed messages: {str(spammed)}")
                s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}Spammed: {self.message} with {self.token}{Style.RESET_ALL}")
            else:
                if(response.json()["code"] == 20028):
                    tosleep = response.json()["retry_after"]
                    s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.YELLOW}Sleep {tosleep} with {self.token}{Style.RESET_ALL}")
                    time.sleep(tosleep)
                else:
                    s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.LIGHTRED_EX}Failed spam with {self.token}: {response.text}{Style.RESET_ALL}")

    def spam_channel_loop(self):
        while True:
            self.spam_channel()
            #time.sleep(0.05)

class Joiner():
    def __init__(self, token, invite, verify):
        self.token = token
        self.invite = invite
        self.verify = verify

    def join_token(self):
        if ":" in self.token:
            self.token = self.token.split(":")[2]
        headers = { 
            "Host": "discord.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "X-Context-Properties": "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjczNTIzMDEyMjY5NjYzODU0NSIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5NzU3MDIyNjY1NTAwNTQ5NjIiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9",
            "Authorization": self.token,
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJkZSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAwLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTI5MjY4LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            "X-Discord-Locale": "en-US",
            "X-Debug-Options": "bugReporterEnabled",
            "Origin": "https://discord.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        global joined
        global joined_captcha
        global joined_locked
        with httpx.Client(headers=headers, proxies="http://" + random.choice(proxies)) as client:
            cookes_raw = str(client.get('https://discord.com/api/v9/users/@me').headers['set-cookie'])
            dcfduid = cookes_raw.split("__dcfduid=")[1].split("Expires=")[0]
            sdcfduid = cookes_raw.split("__sdcfduid=")[1].split("Expires=")[0]
            cookies = f"__dcfduid={dcfduid}__sdcfduid={sdcfduid} locale:en-US;"
            client.headers["Cookie"] = cookies
            response = client.post(f"https://discord.com/api/v9/invites/{self.invite}", json={})
            if(response.status_code == 200):
                name = response.json()["guild"]["name"]
                if(self.verify):
                    guild_id = response.json()["guild"]["id"]
                    verify_json = client.get(f"https://discord.com/api/v9/guilds/{guild_id}/member-verification?with_guild=false&invite_code={self.invite}")
                    verify_resp = client.put(f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me", json=verify_json.json())
                    if verify_resp.status_code == 201:
                        s_print(f"{Fore.GREEN}Joined & Bypassed: {self.token} to {name}{Style.RESET_ALL}")
                else:
                    joined += 1
                    s_print(f"{Fore.GREEN}Joined: {self.token} to {name}{Style.RESET_ALL}")
            elif response.status_code == 401:
                s_print(f"{Fore.RED}Invalid token: {self.token}{Style.RESET_ALL}")
            elif response.status_code == 403:
                if("banned" in response.text):
                    s_print(f"{Fore.RED}Banned token: {self.token}{Style.RESET_ALL}")
                else:
                    joined_locked += 1
                    s_print(f"{Fore.RED}Locked token: {self.token}{Style.RESET_ALL}")
            elif response.status_code == 429:
                s_print(f"{Fore.YELLOW}Rate limited: {self.token}{Style.RESET_ALL}")
            elif response.status_code == 404:
                s_print(f"{Fore.RED}Invalid invite: {self.token}{Style.RESET_ALL}")
            elif response.status_code == 400:
                joined_captcha += 1
                s_print(f"{Fore.YELLOW}Captcha detected: {self.token}{Style.RESET_ALL}")
            set_title(f"Joined: {str(joined)} Captcha: {str(joined_captcha)} Locked: {str(joined_locked)}")

class Checker():
    def __init__(self, token):
        self.token = token

    def check(self):
        unformated = self.token
        if ":" in self.token:
            self.token = self.token.split(":")[2]
        headers = { 
            "Host": "discord.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "X-Context-Properties": "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjczNTIzMDEyMjY5NjYzODU0NSIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5NzU3MDIyNjY1NTAwNTQ5NjIiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9",
            "Authorization": self.token,
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJkZSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAwLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTI5MjY4LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            "X-Discord-Locale": "en-US",
            "X-Debug-Options": "bugReporterEnabled",
            "Origin": "https://discord.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        global checked_valid
        global checked_invalid
        global checked_locked
        global tokens
        with httpx.Client(headers=headers, proxies="http://" + random.choice(proxies)) as client:
            cookes_raw = str(client.get('https://discord.com/api/v9/users/@me').headers['set-cookie'])
            dcfduid = cookes_raw.split("__dcfduid=")[1].split("Expires=")[0]
            sdcfduid = cookes_raw.split("__sdcfduid=")[1].split("Expires=")[0]
            cookies = f"__dcfduid={dcfduid}__sdcfduid={sdcfduid} locale:en-US;"
            client.headers["Cookie"] = cookies
            response = client.get(f"https://discord.com/api/v9/users/@me/library")
            if(response.status_code == 401):
                checked_invalid += 1
                tokens.remove(unformated)
                s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.RED}Invalid: {self.token}{Style.RESET_ALL}")
            elif('You need to verify' in response.text):
                checked_locked += 1
                tokens.remove(unformated)
                s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.LIGHTRED_EX}Locked: {self.token}{Style.RESET_ALL}")
            elif(response.status_code == 200):
                checked_valid += 1
                s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.GREEN}Valid: {self.token}{Style.RESET_ALL}")
            else:
                s_print(response.status_code)
            set_title(f"Valid: {str(checked_valid)} Locked: {str(checked_locked)} Invalid: {str(checked_invalid)}")

class FriendBomber():
    def __init__(self, token, tag):
        self.token = token
        self.tag = tag

    def send_request(self):
        if ":" in self.token:
            self.token = self.token.split(":")[2]
        global sent_fr
        global failed_fr
        headers = { 
            "Host": "discord.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "X-Context-Properties": "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjczNTIzMDEyMjY5NjYzODU0NSIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5NzU3MDIyNjY1NTAwNTQ5NjIiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9",
            "Authorization": self.token,
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJkZSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAwLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTI5MjY4LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            "X-Discord-Locale": "en-US",
            "X-Debug-Options": "bugReporterEnabled",
            "Origin": "https://discord.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        with httpx.Client(headers=headers, proxies="http://" + random.choice(proxies)) as client:
            cookes_raw = str(client.get('https://discord.com/api/v9/users/@me').headers['set-cookie'])
            dcfduid = cookes_raw.split("__dcfduid=")[1].split("Expires=")[0]
            sdcfduid = cookes_raw.split("__sdcfduid=")[1].split("Expires=")[0]
            cookies = f"__dcfduid={dcfduid}__sdcfduid={sdcfduid} locale:en-US;"
            client.headers["Cookie"] = cookies
            response = client.post(f"https://discord.com/api/v9/users/@me/relationships", json={"username":self.tag.split("#")[0],"discriminator":int(self.tag.split("#")[1])})
            if(response.status_code == 204):
                sent_fr += 1
                s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.GREEN}Sent to: {self.tag} with {self.token}{Style.RESET_ALL}")
            else:
                failed_fr += 1
                s_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} {Fore.RED}Failed to: {self.tag} with {self.token}{Style.RESET_ALL}")
            print(response.text)
            set_title(f"Sent Friend requests: {str(sent_fr)}")


# MODULES

def joiner_module():
    os.system("cls")
    s_print(Fore.LIGHTMAGENTA_EX + intro + Style.RESET_ALL)
    s_print(" ")
    invite = input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Enter invite: ")
    if(".gg/" in invite):
        invite = invite.split(".gg/")[1]
    delay = int(input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Enter delay in s (0 for no delay): "))
    verify = input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Bypass community verify? (y/n): ")
    if(verify == "y"):
        verify = True
    else:
        verify = False
    threads = []
    for token in tokens:        
        instant = Joiner(token, invite, verify)
        t = threading.Thread(target=instant.join_token)
        threads.append(t)
        if(delay != 0):
            time.sleep(delay)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    global joined
    global joined_locked
    global joined_captcha
    input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Results: Joined: {str(joined)} Locked: {str(joined_locked)} Captcha: {str(joined_captcha)}, Press ENTER to goto Main menu")
    joined = 0
    joined_locked = 0
    joined_captcha = 0
    main()


def channelspammer_module():
    os.system("cls")
    s_print(Fore.LIGHTMAGENTA_EX + intro + Style.RESET_ALL)
    s_print(" ")
    id = int(input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Enter channel id: "))
    message = input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Enter message to spam: ")
    for token in tokens:
        instant = ChannelSpammer(token, id, message)
        threading.Thread(target=instant.spam_channel_loop).start()
        #time.sleep(0.01)

def checker_module():
    os.system("cls")
    s_print(Fore.LIGHTMAGENTA_EX + intro + Style.RESET_ALL)
    s_print(" ")
    threads = []
    for token in tokens:
        instant = Checker(token)
        t = threading.Thread(target=instant.check)
        threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    global checked_valid
    global checked_invalid
    global checked_locked
    with open("tokens.txt", "r+") as token_file:
        token_file.truncate(0)
        token_file.close()
    with open("tokens.txt", "r+") as token_file:
        for token in tokens:
            token_file.write(token + "\n")
    input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Results: Valid: {str(checked_valid)} Locked: {str(checked_locked)} Invalid: {str(checked_invalid)}, Press ENTER to goto Main menu")
    checked_valid = 0
    checked_invalid = 0
    checked_locked = 0
    main()

def friendbomber_module():
    global sent_fr
    global failed_fr
    os.system("cls")
    s_print(Fore.LIGHTMAGENTA_EX + intro + Style.RESET_ALL)
    s_print(" ")
    tag = input("Enter tag#0000: ")
    threads = []
    for token in tokens:
        instant = FriendBomber(token, tag)
        t = threading.Thread(target=instant.send_request)
        threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Results: Sent: {str(sent_fr)} Failed: {str(failed_fr)}, Press ENTER to goto Main menu")
    sent_fr = 0
    failed_fr = 0
    main()

# UTILS

def load_tokens():
    global tokens
    tokens = []
    with open("tokens.txt") as token_file:
        for line in token_file:
            tokens.append(line.replace("\n", ""))
        return len(tokens)

def load_proxies():
    global proxies
    with open("proxies.txt") as proxy_file:
        for line in proxy_file:
            proxies.append(line.replace("\n", ""))
        return len(proxies)

def set_title(text):
    os.system(f"title Drip Spammer - {text}")

# MAIN

def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)

intro = '''
$$$$$$$\  $$$$$$$\  $$$$$$\ $$$$$$$\  
$$  __$$\ $$  __$$\ \_$$  _|$$  __$$\ 
$$ |  $$ |$$ |  $$ |  $$ |  $$ |  $$ |
$$ |  $$ |$$$$$$$  |  $$ |  $$$$$$$  |
$$ |  $$ |$$  __$$<   $$ |  $$  ____/ 
$$ |  $$ |$$ |  $$ |  $$ |  $$ |      
$$$$$$$  |$$ |  $$ |$$$$$$\ $$ |      
\_______/ \__|  \__|\______|\__|      
'''

def main():
    os.system('cls')
    set_title(f"Loaded tokens: {load_tokens()} Loaded proxies: {load_proxies()}")
    s_print(Fore.LIGHTMAGENTA_EX + intro + Style.RESET_ALL)
    s_print(" ")
    s_print(f"{Fore.LIGHTMAGENTA_EX}[1]{Style.RESET_ALL} Joiner")
    s_print(f"{Fore.LIGHTMAGENTA_EX}[2]{Style.RESET_ALL} Channel spammer")
    s_print(f"{Fore.LIGHTMAGENTA_EX}[3]{Style.RESET_ALL} Checker")
    s_print(f"{Fore.LIGHTMAGENTA_EX}[4]{Style.RESET_ALL} Friend bomber")
    s_print(" ")
    option = input(f"{Fore.LIGHTMAGENTA_EX}[>]{Style.RESET_ALL} Enter choice: ")
    try:
        option = int(option)
    except:
        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Choice must be integer bewteen 1-4")
        time.sleep(2)
        main()
    if(option == 1):
        joiner_module()
    elif(option == 2):
        channelspammer_module()
    elif(option == 3):
        checker_module()
    elif(option == 4):
        friendbomber_module()
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Choice must be integer bewteen 1-4")
        time.sleep(2)
        main()

if(__name__ == "__main__"):
    main()
