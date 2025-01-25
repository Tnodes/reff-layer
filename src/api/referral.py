import tls_requests as requests
from typing import Dict, Optional, Tuple
import time
import json
import random

from ..config.settings import APIConfig
from ..models.wallet import Wallet
from ..utils.exceptions import APIError, WalletAlreadyRegisteredError, InvalidWalletError
from ..utils.proxy_handler import ProxyHandler
from ..utils.logger import Logger

class ReferralClient:
    def __init__(self, referral_code: Optional[str] = None, proxy_file: str = "proxy.txt"):
        self.base_url = APIConfig.BASE_URL
        self.referral_code = referral_code or APIConfig.DEFAULT_REFERRAL_CODE
        self.headers = APIConfig.get_headers()
        self.proxy_handler = ProxyHandler(proxy_file)
        self.logger = Logger()
        
        if self.proxy_handler.is_enabled():
            self.logger.info(f"Loaded {self.proxy_handler.get_proxy_count()} proxies")
        else:
            self.logger.warning("Running without proxy support")
    
    def _make_request(self, endpoint: str, json_data: Dict, max_retries: int = 3) -> Tuple[Dict, int]:
        """
        Make an HTTP request to the API with exponential backoff
        """
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    delay = min((2 ** attempt) + random.uniform(1, 3), 15)
                    self.logger.info(f"Attempt {attempt + 1}/{max_retries} - Waiting {delay:.2f} seconds...")
                    time.sleep(delay)
                
                proxies = None
                if self.proxy_handler.is_enabled():
                    proxies = self.proxy_handler.get_next_proxy()
                    if proxies:
                        self.logger.proxy(f"Using proxy: {proxies['https']}")
                    else:
                        self.logger.warning("Failed to get proxy, making direct request")
                
                self.logger.request(f"POST {url}")
                self.logger.info(f"Attempt {attempt + 1}/{max_retries}")
                
                response = requests.post(
                    url,
                    json=json_data,
                    headers=self.headers,
                    timeout=APIConfig.TIMEOUT,
                    verify=False,
                    proxies=proxies if proxies else None
                )
                
                if not response:
                    raise APIError("No response received")
                
                self.logger.response(response.status_code, response.text)
                
                if response.status_code == 409:
                    raise WalletAlreadyRegisteredError("Wallet address is already registered")
                elif response.status_code == 400:
                    raise InvalidWalletError("Invalid wallet address")
                elif response.status_code == 429: 
                    self.logger.warning("Rate limit hit, waiting longer...")
                    time.sleep(15)
                    continue
                elif response.status_code >= 500:
                    self.logger.warning(f"Server error {response.status_code}, retrying...")
                    time.sleep(5)
                    continue
                elif response.status_code == 407:
                    if proxies:
                        self.logger.warning("Proxy authentication failed, trying next proxy...")
                        continue
                    else:
                        raise APIError("Proxy authentication required but no proxy available")
                
                try:
                    data = json.loads(response.text) if response.text.strip() else {}
                    return data, response.status_code
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {str(e)}")
                    if attempt < max_retries - 1:
                        continue
                    return {"error": "Invalid JSON response", "text": response.text}, response.status_code
                    
            except (WalletAlreadyRegisteredError, InvalidWalletError) as e:
                raise e
            except requests.exceptions.ProxyError as e:
                if proxies:
                    self.logger.error(f"Proxy error: {str(e)}, trying next proxy...")
                    if attempt < max_retries - 1:
                        continue
                    raise APIError(f"All proxy attempts failed: {str(e)}")
                else:
                    raise APIError(f"Connection error: {str(e)}")
            except Exception as e:
                self.logger.error(f"Request failed: {str(e)}")
                if attempt < max_retries - 1:
                    continue
                raise APIError(f"Request failed: {str(e)}")
                
        raise APIError(f"Request failed after {max_retries} attempts")
        
    def register_wallet(self, wallet_address: str, max_retries: int = 3) -> Wallet:
        """
        Register a wallet address for referral
        """
        try:
            data, status_code = self._make_request(
                f'referral/register-wallet/{self.referral_code}',
                {'walletAddress': wallet_address},
                max_retries=max_retries
            )
            
            if status_code == 200 and isinstance(data, dict) and 'data' in data:
                wallet = Wallet.from_api_response(data["data"])
                self.logger.success(f"Successfully registered wallet {wallet_address}")
                return wallet
            else:
                raise APIError(f"Unexpected response format or status code: {status_code}")
                
        except (WalletAlreadyRegisteredError, InvalidWalletError) as e:
            raise e
        except Exception as e:
            raise APIError(f"Failed to register wallet: {str(e)}")
            
    def process_wallet_with_delay(self, wallet_address: str) -> Dict:
        """
        Process a wallet with proper delay and error handling
        """
        try:
            delay = random.uniform(2, 5)
            self.logger.info(f"Waiting {delay:.2f} seconds before processing next wallet...")
            time.sleep(delay)
            
            return self.register_wallet(wallet_address)
        except Exception as e:
            self.logger.error(f"Error processing wallet {wallet_address}: {str(e)}")
            raise 