from pyfiglet import Figlet
from colorama import Fore
import os

def print_banner():
    # Check the operating system
    if os.name == 'posix':  # Linux and MacOS
        figlet = Figlet(font='Larry 3D')
        print(figlet.renderText('Tdrop'))
            
        print(Fore.WHITE + 'Program Name: Layeredge Auto Referral Tool')
        print(Fore.WHITE + 'Telegram    : ' + Fore.MAGENTA + 'https://t.me/tdropid\n')
    elif os.name == 'nt':  # Windows
        figlet = Figlet(font='Larry3D')
        print(figlet.renderText('Tdrop'))
        print(Fore.WHITE + 'Program Name: Layeredge Auto Referral Tool')
        print(Fore.WHITE + 'Telegram    : ' + Fore.MAGENTA + 'https://t.me/tdropid\n')