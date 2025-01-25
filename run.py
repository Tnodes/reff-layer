import sys
import os

# Disable pycache
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Run the main program
from main import main

if __name__ == "__main__":
    main() 