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
        return cls(
            wallet_address=data["walletAddress"],
            referral_code=data.get("referralCode"),
            total_points=data.get("totalPoints", 0),
            node_points=data.get("nodePoints", 0),
            last_claimed=datetime.fromisoformat(data["lastClaimed"]) if data.get("lastClaimed") else None,
            referrals=data.get("referrals", []),
            created_at=datetime.fromisoformat(data["createdAt"]) if data.get("createdAt") else None,
            updated_at=datetime.fromisoformat(data["updatedAt"]) if data.get("updatedAt") else None
        ) 