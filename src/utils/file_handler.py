from typing import List
import os
from ..utils.logger import Logger

class FileHandler:
    def __init__(self):
        self.logger = Logger()
    
    def read_wallet_addresses(self, file_path: str) -> List[str]:
        """
        Read wallet addresses from a file
        
        Args:
            file_path: Path to the file containing wallet addresses
            
        Returns:
            List[str]: List of wallet addresses
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty
        """
        if not os.path.exists(file_path):
            self.logger.error(f"Wallet file '{file_path}' not found")
            raise FileNotFoundError(f"Wallet file '{file_path}' not found")
            
        with open(file_path, 'r') as f:
            addresses = [line.strip() for line in f.readlines() if line.strip()]
            
        if not addresses:
            self.logger.error(f"No wallet addresses found in {file_path}")
            raise ValueError(f"No wallet addresses found in {file_path}")
            
        # Validate wallet addresses
        for addr in addresses:
            if not addr.startswith('0x') or len(addr) != 42:
                self.logger.error(f"Invalid wallet address format: {addr}")
                raise ValueError(f"Invalid wallet address format: {addr}")
        
        return addresses 