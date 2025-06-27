# 💸 TON Auto Withdrawer

This script automatically checks the balance of TON wallets (based on mnemonic phrases) and, if funds are available, **sends them to the specified main wallet**.

## ⚙️ Features

- Supports popular TON wallet types (`WalletV3R1`, `WalletV3R2`, `WalletV4R1`, `WalletV4R2`, `WalletV5R1`, `HighloadWalletV2/V3`, etc.)
- Connects via the [`tonconsole.com`](https://tonconsole.com/) API
- Accounts for TON network fees
- Logs all successful transactions
- Processes multiple mnemonics sequentially
- Asynchronous (uses `asyncio`)
- Convenient log output

## 📁 Project Structure

```
├── main.py                  # Main script
├── mnemonic.txt             # List of mnemonics (one per line)
├── logger.py                # Logger module (assumed to be present)
└── logs/
    └── transfer_logs.txt    # Log of all successful transfers
```

## 📦 Installation

1. Make sure you have Python 3.11+ installed
2. Install dependencies:

```bash
python -m venv .venv
```
```bash
.venv\Scripts\Activate
```
```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
loguru~=0.7.3
requests~=2.32.4
tonutils~=0.4.8
```

## 🛠 Configuration

Open `main.py` and set:

```python
TON_CONSOLE_API_KEY = "YOUR_API_KEY_FROM_tonconsole.com"
TON_ADDRESS_FOR_SEND = "YOUR_TON_ADDRESS_FOR_FUNDS_COLLECTION"
```

Also, make sure there is a `mnemonic.txt` file in the root directory with mnemonics:

```
word word word ... (12/24 words)
word word word ... (12/24 words)
...
```

## 🚀 Run

```bash
python main.py
```

The script will sequentially process each wallet, check its balance, and if sufficient funds are available — transfer them to the specified address.

## 📄 Logs

- All successful transfers are saved to `logs/transfer_logs.txt`.
- Logger also prints information to the console.

## ❗ Important

- Transfer fee is set manually (default `0.0088 TON`). Make sure it's up to date.
- The script **will not transfer funds** if the balance is ≤ the fee.

## ✅ Example log line

```
2025-06-27 14:53:10 | [1] | EQD... : UQD... (WalletV4R1) => EQC... | 1.23456789 | tx:ABCDEF123...
```
