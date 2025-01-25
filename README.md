# Layeredge Auto Referral Tool

A powerful automation tool for managing Layeredge referrals with proxy support and beautiful console output.

## Features

- 🚀 Fast and efficient wallet registration
- 🌐 Optional proxy support with automatic rotation
- 🎨 Beautiful colored console output
- 📊 Real-time progress tracking
- 💾 Automatic result saving
- 🔄 Retry mechanism with exponential backoff
- 📝 Detailed logging
- 🛡️ Error handling and recovery

## Requirements

- Python 3.8 or higher
- Required Python packages (installed automatically)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Tnodes/reff-layer.git
cd reff-layer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Edit the `src/config/settings.py` file to set your `referral code` and other settings.

2. Create `wallet.txt` and add your wallet addresses (one per line):
```
0x0000000000000000000000000000000000000000
0x0000000000000000000000000000000000000000
0x0000000000000000000000000000000000000000
```
Note: Each wallet address must be in the correct format (0x... and 42 characters long)

3. (Optional) Create `proxy.txt` and add your proxies (one per line):
```
http://username:password@host:port
https://username:password@host:port
```
Note: The tool will run without proxies if this file doesn't exist or is empty.

## Usage

Run the tool using:
```bash
python run.py
```

The tool will:
1. Validate wallet addresses in `wallet.txt`
2. Use proxies if available (optional)
3. Save results to the `logs` directory
4. Show real-time progress and statistics

## Output

The tool provides:
- Real-time progress updates
- Color-coded status messages
- Success/error statistics
- Detailed logs in JSON format

Example log file (`logs/registration_results_TIMESTAMP.json`):
```json
[
  {
    "wallet_address": "0x...",
    "status": "success",
    "referral_code": "...",
    "timestamp": "..."
  }
]
```

## Error Handling

The tool handles various scenarios:
- Missing or empty wallet file
- Invalid wallet addresses
- Already registered wallets
- Network errors
- Proxy failures (with fallback to direct connection)
- Rate limiting

## Support

For support, join our Telegram channel: [https://t.me/tdropid](https://t.me/tdropid)