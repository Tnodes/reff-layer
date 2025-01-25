from typing import List, Optional
import random
import os

class ProxyHandler:
    def __init__(self, proxy_file: str = "proxy.txt"):
        self.proxy_file = proxy_file
        self.proxies = self._load_proxies()
        self.current_index = 0
        self.proxy_enabled = bool(self.proxies)  # Track if proxies are available
    
    def _load_proxies(self) -> List[str]:
        """Load proxies from file"""
        try:
            if not os.path.exists(self.proxy_file):
                print(f"Note: Proxy file '{self.proxy_file}' not found. Running without proxies.")
                return []
                
            with open(self.proxy_file, 'r') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
                
            if not proxies:
                print("Note: No proxies found in proxy file. Running without proxies.")
                
            return proxies
        except Exception as e:
            print(f"Warning: Error loading proxies: {str(e)}. Running without proxies.")
            return []
    
    def get_next_proxy(self) -> Optional[dict]:
        """Get next proxy in rotation"""
        if not self.proxy_enabled:
            return None
            
        if not self.proxies:
            return None
            
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        
        # Format: protocol://user:pass@host:port or protocol://host:port
        try:
            if '@' in proxy:
                protocol, auth_host = proxy.split('://')
                auth, host = auth_host.split('@')
                return {
                    'http': proxy,
                    'https': proxy
                }
            else:
                protocol, host = proxy.split('://')
                return {
                    'http': proxy,
                    'https': proxy
                }
        except Exception as e:
            print(f"Warning: Error parsing proxy {proxy}: {str(e)}")
            return None
    
    def get_random_proxy(self) -> Optional[dict]:
        """Get random proxy from list"""
        if not self.proxy_enabled:
            return None
            
        if not self.proxies:
            return None
            
        proxy = random.choice(self.proxies)
        
        try:
            if '@' in proxy:
                protocol, auth_host = proxy.split('://')
                auth, host = auth_host.split('@')
                return {
                    'http': proxy,
                    'https': proxy
                }
            else:
                protocol, host = proxy.split('://')
                return {
                    'http': proxy,
                    'https': proxy
                }
        except Exception as e:
            print(f"Warning: Error parsing proxy {proxy}: {str(e)}")
            return None
            
    def get_proxy_count(self) -> int:
        """Get total number of loaded proxies"""
        return len(self.proxies)
        
    def is_enabled(self) -> bool:
        """Check if proxy support is enabled"""
        return self.proxy_enabled 