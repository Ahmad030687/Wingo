import requests
import time
import sys
import random
from datetime import datetime
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    # Fallback if colorama not installed
    class Fore: GREEN = ""; RED = ""; YELLOW = ""; CYAN = ""; WHITE = ""; RESET = ""
    class Style: BRIGHT = ""

# --- CONFIGURATION ---
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageSize=50&ts="
Bot_Name = "DARKNET SUPREME PY"
Version = "V.1.0"

# --- GLOBAL VARS ---
current_level = 1
last_issue = None
current_bet = None
wins = 0
losses = 0

def banner():
    print(f"{Fore.GREEN}{Style.BRIGHT}" + "="*40)
    print(f"{Fore.GREEN}   {Bot_Name}  {Fore.WHITE}|  {Version}")
    print(f"{Fore.GREEN}   LEVEL 2 FIXER ENGINE ACTIVATED")
    print(f"{Fore.GREEN}" + "="*40 + "\n")

def get_data():
    try:
        # Adding random timestamp to avoid cache
        ts = int(time.time() * 1000)
        url = f"{API_URL}{ts}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()['data']['list']
        else:
            return None
    except Exception as e:
        return None

def analyze_logic(history):
    global current_level
    
    # Extract Data
    last_res = "BIG" if int(history[0]['number']) >= 5 else "SMALL"
    
    # --- LOGIC ENGINE ---
    prediction = ""
    algo = ""
    
    # LEVEL 1: RIDE THE WAVE (Follow Trend)
    if current_level == 1:
        prediction = last_res
        algo = "DRAGON FOLLOW (L1)"
        
    # LEVEL 2: THE FIXER (Anti-Trend / Flip)
    # Agar L1 fail hua, iska matlab Trend toot gaya. 
    # Hum Trend wapas judne ka intezar nahi karenge, hum Opposite khelenge.
    else:
        prediction = "SMALL" if last_res == "BIG" else "BIG"
        algo = "SHADOW ASSASSIN (L2)"
        
    return prediction, algo

def print_bet(issue, pred, algo, level):
    # Quantum Seeds (Visual Only)
    s1 = random.randint(5, 9) if pred == "BIG" else random.randint(0, 4)
    s2 = random.randint(0, 9)
    
    color = Fore.GREEN if pred == "BIG" else Fore.RED
    
    print(f"{Fore.CYAN}[SCANNING] {Fore.WHITE}Analyzing Market Data...")
    time.sleep(1) # Fake calculation delay for feel
    
    print(f"\n{Fore.YELLOW}>>> NEW SIGNAL DETECTED <<<")
    print(f"PERIOD  : {Fore.WHITE}#{issue}")
    print(f"ALGO    : {Fore.CYAN}{algo}")
    print(f"LEVEL   : {Fore.YELLOW}{level}")
    print(f"SEEDS   : {Fore.WHITE}[ {s1} ] [ {s2} ]")
    print(f"BET     : {color}{Style.BRIGHT}███ {pred} ███{Style.RESET}\n")

def verify_win(history):
    global current_bet, current_level, wins, losses
    
    latest_issue = history[0]['issueNumber']
    latest_res = "BIG" if int(history[0]['number']) >= 5 else "SMALL"
    latest_num = history[0]['number']
    
    if current_bet and current_bet['issue'] == latest_issue:
        print(f"{Fore.WHITE}RESULT #{latest_issue}: {latest_res} [{latest_num}]")
        
        if current_bet['pred'] == latest_res:
            print(f"{Fore.GREEN}{Style.BRIGHT}✔ WINNER! - RECOVERY SUCCESS{Style.RESET}")
            wins += 1
            current_level = 1 # Reset to Level 1
        else:
            print(f"{Fore.RED}{Style.BRIGHT}✖ LOSS - ACTIVATING LEVEL 2{Style.RESET}")
            losses += 1
            current_level = 2 # Activate Fixer Mode
            if current_level > 2: current_level = 1 # Reset if L2 fails (Optional Safety)

        print(f"{Fore.WHITE}Session Stats: {Fore.GREEN}{wins} W {Fore.WHITE}| {Fore.RED}{losses} L")
        print("-" * 40)
        current_bet = None

def main():
    global last_issue, current_bet
    banner()
    
    while True:
        history = get_data()
        
        if history:
            latest = history[0]
            latest_issue = latest['issueNumber']
            
            # 1. Check Result of Previous Bet
            if current_bet and int(latest_issue) >= int(current_bet['issue']):
                verify_win(history)
            
            # 2. Make New Prediction
            next_issue = str(int(latest_issue) + 1)
            
            if last_issue != latest_issue:
                last_issue = latest_issue
                
                # Logic Call
                pred, algo = analyze_logic(history)
                
                # Save Bet
                current_bet = {
                    'issue': next_issue,
                    'pred': pred
                }
                
                # Print UI
                print_bet(next_issue, pred, algo, current_level)
                
            else:
                # Waiting animation
                sys.stdout.write(f"\r{Fore.WHITE}Waiting for Draw... {datetime.now().strftime('%H:%M:%S')}")
                sys.stdout.flush()
                
        else:
            print(f"{Fore.RED}Connection Error... Retrying")
            
        time.sleep(2) # Refresh rate

if __name__ == "__main__":
    main()
