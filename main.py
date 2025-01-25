import json
import os
from datetime import datetime
from src.api.referral import ReferralClient
from src.utils.exceptions import WalletAlreadyRegisteredError, InvalidWalletError, APIError
from src.utils.file_handler import FileHandler
from src.utils.logger import Logger
from src.utils.banner import print_banner

def process_wallet(client: ReferralClient, wallet_address: str) -> dict:
    """Process a single wallet address"""
    try:
        wallet = client.process_wallet_with_delay(wallet_address)
        
        return {
            "wallet_address": wallet.wallet_address,
            "status": "success",
            "referral_code": wallet.referral_code,
            "total_points": wallet.total_points,
            "node_points": wallet.node_points,
            "referrals": wallet.referrals,
            "created_at": wallet.created_at.isoformat() if wallet.created_at else None,
            "updated_at": wallet.updated_at.isoformat() if wallet.updated_at else None,
            "timestamp": datetime.now().isoformat()
        }
        
    except WalletAlreadyRegisteredError:
        return {
            "wallet_address": wallet_address,
            "status": "error",
            "error": "already_registered",
            "timestamp": datetime.now().isoformat()
        }
    except InvalidWalletError:
        return {
            "wallet_address": wallet_address,
            "status": "error",
            "error": "invalid_wallet",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "wallet_address": wallet_address,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def save_results(results: list, timestamp: str):
    """Save results to a log file"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"registration_results_{timestamp}.json")
    with open(log_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return log_file

def main():
    print_banner()
    logger = Logger()
    file_handler = FileHandler()
    
    client = ReferralClient()
    
    wallet_file = "wallet.txt"
    
    try:
        wallet_addresses = file_handler.read_wallet_addresses(wallet_file)
        total_wallets = len(wallet_addresses)
        
        logger.info(f"Found {total_wallets} valid wallet addresses to process")
        
        results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for idx, wallet_address in enumerate(wallet_addresses, 1):
            logger.progress(idx, total_wallets, f"Processing {wallet_address}")
            
            result = process_wallet(client, wallet_address)
            results.append(result)
            
            if idx % 10 == 0:
                log_file = save_results(results, timestamp)
                logger.info(f"Intermediate results saved to: {log_file}")
                
                successful = sum(1 for r in results if r["status"] == "success")
                already_registered = sum(1 for r in results if r.get("error") == "already_registered")
                errors = sum(1 for r in results if r["status"] == "error" and r.get("error") != "already_registered")
                
                logger.summary(idx, successful, already_registered, errors)
            
        log_file = save_results(results, timestamp)
        logger.info(f"Final results saved to: {log_file}")
        
        successful = sum(1 for r in results if r["status"] == "success")
        already_registered = sum(1 for r in results if r.get("error") == "already_registered")
        errors = sum(1 for r in results if r["status"] == "error" and r.get("error") != "already_registered")
        
        logger.summary(total_wallets, successful, already_registered, errors)
        
    except FileNotFoundError:
        logger.error(f"Please create a wallet.txt file with your wallet addresses")
    except ValueError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main() 