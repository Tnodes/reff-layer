from pyfiglet import Figlet
from colorama import Fore

def print_banner():
    figlet = Figlet(font='Larry3D')
    print(figlet.renderText('Tdrop'))
    print(Fore.WHITE + 'Program Name: Layeredge Auto Referral Tool')
    print(Fore.WHITE + 'Telegram    : ' + Fore.MAGENTA + 'https://t.me/tdropid\n')