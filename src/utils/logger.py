from colorama import init, Fore, Back, Style
from datetime import datetime

# Initialize colorama
init(autoreset=True)

class Logger:
    @staticmethod
    def info(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.CYAN}[{timestamp}] ℹ INFO: {Fore.WHITE}{message}")
    
    @staticmethod
    def success(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.GREEN}[{timestamp}] ✓ SUCCESS: {Fore.WHITE}{message}")
    
    @staticmethod
    def error(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.RED}[{timestamp}] ✗ ERROR: {Fore.WHITE}{message}")
    
    @staticmethod
    def warning(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.YELLOW}[{timestamp}] ⚠ WARNING: {Fore.WHITE}{message}")
    
    @staticmethod
    def proxy(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.MAGENTA}[{timestamp}] 🌐 PROXY: {Fore.WHITE}{message}")
    
    @staticmethod
    def request(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.BLUE}[{timestamp}] ⟶ REQUEST: {Fore.WHITE}{message}")
    
    @staticmethod
    def response(status_code: int, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = Fore.GREEN if status_code == 200 else Fore.RED if status_code >= 400 else Fore.YELLOW
        print(f"{color}[{timestamp}] ⟵ RESPONSE ({status_code}): {Fore.WHITE}{message}")
    
    @staticmethod
    def progress(current: int, total: int, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        percentage = (current / total) * 100
        print(f"{Fore.CYAN}[{timestamp}] ⏳ PROGRESS: {Fore.WHITE}[{current}/{total}] {percentage:.1f}% - {message}")
    
    @staticmethod
    def summary(total: int, success: int, registered: int, errors: int):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{Fore.CYAN}[{timestamp}] 📊 SUMMARY:")
        print(f"{Fore.WHITE}Total wallets processed: {Fore.CYAN}{total}")
        print(f"{Fore.WHITE}Successfully registered: {Fore.GREEN}{success}")
        print(f"{Fore.WHITE}Already registered: {Fore.YELLOW}{registered}")
        print(f"{Fore.WHITE}Errors: {Fore.RED}{errors}\n")