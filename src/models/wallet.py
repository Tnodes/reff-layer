from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Wallet:
    wallet_address: str
    referral_code: Optional[str] = None
    total_points: int = 0
    node_points: int = 0
    last_claimed: Optional[datetime] = None
    referrals: List[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.referrals is None:
            self.referrals = []
            
    @classmethod
    def from_api_response(cls, data: dict) -> 'Wallet':
        """Create a Wallet instance from API response data"""
        try:
            created_at = datetime.strptime(data.get('createdAt', ''), '%Y-%m-%dT%H:%M:%S.%fZ') if data.get('createdAt') else None
            updated_at = datetime.strptime(data.get('updatedAt', ''), '%Y-%m-%dT%H:%M:%S.%fZ') if data.get('updatedAt') else None
        except ValueError:
            # Fallback if milliseconds are not present
            created_at = datetime.strptime(data.get('createdAt', ''), '%Y-%m-%dT%H:%M:%SZ') if data.get('createdAt') else None
            updated_at = datetime.strptime(data.get('updatedAt', ''), '%Y-%m-%dT%H:%M:%SZ') if data.get('updatedAt') else None
            
        return cls(
            wallet_address=data.get('walletAddress', ''),
            referral_code=data.get('referralCode', ''),
            total_points=data.get('totalPoints', 0),
            node_points=data.get('nodePoints', 0),
            referrals=data.get('referrals', []),
            created_at=created_at,
            updated_at=updated_at
        ) 