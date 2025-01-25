import random

number = random.randint(100, 132)

class APIConfig:
    BASE_URL = "https://referral.layeredge.io/api"
    DEFAULT_REFERRAL_CODE = "YOURE_REFERRAL_CODE"
    TIMEOUT = 30
    
    @classmethod
    def get_headers(cls):
        return {
            "accept": "application/json",
            "accept-language": "en-US;q=0.8,en;q=0.7",
            "connection": "keep-alive",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://dashboard.layeredge.io",
            "referer": "https://dashboard.layeredge.io/",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{number}.0.0.0 Safari/537.36"
        } 