import requests
import json
import os
from colorama import *
from datetime import datetime
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class CatsDogs:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.catsdogs.live',
            'Origin': 'https://catsdogs.live',
            'Pragma': 'no-cache',
            'Referer': 'https://catsdogs.live/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Cats & Dogs - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_task_list(self):
        url = "https://raw.githubusercontent.com/vonssy/Response.JSON/refs/heads/main/catsdogs_tasks.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('code', [])
        except requests.exceptions.RequestException as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Error: Failed to fetch data from URL. {e}{Style.RESET_ALL}")
            return []
        except json.JSONDecodeError:
            self.log(f"{Fore.RED + Style.BRIGHT}Error: Failed to parse JSON data.{Style.RESET_ALL}")
            return []
    
    def user_info(self, query: str):
        url = 'https://api.catsdogs.live/user/info'
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Telegram-Web-App-Data': query
        })

        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def balance(self, query: str):
        url = 'https://api.catsdogs.live/user/balance'
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Telegram-Web-App-Data': query
        })

        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def claim_game(self, query: str):
        url = 'https://api.catsdogs.live/game/claim'
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Telegram-Web-App-Data': query
        })

        response = self.session.post(url, headers=self.headers)
        result = response.json()
        if response.status_code == 200:
            return result
        else:
            return None
        
    def tasks(self, query: str):
        url = 'https://api.catsdogs.live/tasks/list'
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Telegram-Web-App-Data': query
        })

        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def complete_basic_tasks(self, query: str, task_id: int):
        url = 'https://api.catsdogs.live/tasks/claim'
        data = json.dumps({'task_id': task_id})
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Telegram-Web-App-Data': query
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = response.json()
            if result:
                return result
            else:
                return None
        else:
            return None
        
    def complete_video_tasks(self, query: str, video_id: int, code: str):
        url = 'https://api.catsdogs.live/tasks/claim'
        data = json.dumps({'task_id': video_id, 'verification_code':code})
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Telegram-Web-App-Data': query
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                return result
            else:
                return None
        else:
            return None
    
    def process_query(self, query: str):

        user = self.user_info(query)
        if user:
            balance = self.balance(query)
            if balance:
                total_balance = sum(balance.values())
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['username']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {total_balance} $FOOD {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Error Fetching User Info ]{Style.RESET_ALL}")
        else:
            self.log(f"{Fore.RED+Style.BRIGHT}[ Error Fetching User Info ]{Style.RESET_ALL}")
        time.sleep(1)

        claim = self.claim_game(query)
        if claim:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Game{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {claim['claimed_amount']} $FOOD {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Game{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
        time.sleep(1)

        tasks = self.tasks(query)
        if tasks:
            processed_videos = set()

            for task in tasks:
                task_id = task['id']
                title = task['title']
                reward = task['amount']
                task_type = task['type']

                if not task['hidden'] and task['transaction_id'] is None:

                    if task_type == 'video_code':
                        tasks_video = self.load_task_list()

                        for video in tasks_video:
                            video_id = video['id']
                            code = video['code']

                            if video_id in processed_videos:
                                continue

                            complete_video = self.complete_video_tasks(query, video_id, code)
                            if complete_video:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {video['title']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {reward} $FOOD {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                                processed_videos.add(video_id)
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {video['title']} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            time.sleep(1)

                    else:
                        complete_basic = self.complete_basic_tasks(query, task_id)
                        if complete_basic:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {reward} $FOOD {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Isn't Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)
        else:
            self.log(f"{Fore.RED + Style.BRIGHT}[ Error Fetching Tasks Info ]{Style.RESET_ALL}")
        
    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        time.sleep(3)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Cats & Dogs - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    catsdogs = CatsDogs()
    catsdogs.main()