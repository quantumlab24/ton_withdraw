from logger import logger
import os
import sys
from datetime import datetime, timezone, timedelta
import asyncio
import requests
import random

from tonutils.client import ToncenterV3Client, TonapiClient
from tonutils.wallet import (
    WalletV3R1,
    WalletV3R2,
    WalletV4R1,
    WalletV4R2,
    WalletV5R1,
    HighloadWalletV2,
    HighloadWalletV3
)
from tonutils.wallet import PreprocessedWalletV2R1, PreprocessedWalletV2
from tonutils.wallet.messages import TransferMessage
from enum import Enum

# TONconsole API key : https://tonconsole.com/
TON_CONSOLE_API_KEY = ""

# Адрес TON кошелька, на который собираем все балансы
TON_ADDRESS_FOR_SEND = ""

# Комиссия TON за трансфер TON на другой адрес
TON_FEE = 0.0088

TYPE_WALLET = [
    # Типы кошельков TON, которые проверяет скрипт на наличие баланса и выводит на адрес указанный в TON_ADDRESS_FOR_SEND
    WalletV3R1,
    WalletV3R2,
    WalletV4R1,
    WalletV4R2,
    WalletV5R1,
    HighloadWalletV2,
    HighloadWalletV3
]

async def create_transfer_logs():
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    file_path = os.path.join(folder_path, "transfer_logs.txt")
    os.makedirs(folder_path, exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("")

async def write_transfer_logs(data: str):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    file_path = os.path.join(folder_path, "transfer_logs.txt")
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(data)

async def transfer_ton(i: int, mnemonic: str) -> None:
    for TypeWallet in TYPE_WALLET:
        try:
            client = TonapiClient(
                api_key=TON_CONSOLE_API_KEY,
                rps=2,
                max_retries=3
            )

            wallet, _, private_key, mnemonic = TypeWallet.from_mnemonic(
                client=client,
                mnemonic=mnemonic,
            )

            _ton_address_1 = wallet.address.to_str(is_bounceable=True)
            _ton_address_2 = wallet.address.to_str(is_bounceable=False)

            if TON_ADDRESS_FOR_SEND != _ton_address_1 and TON_ADDRESS_FOR_SEND != _ton_address_2:
                balance: float = await wallet.balance()
                logger.warning(f"[{i}] | {_ton_address_1} : {_ton_address_2} ({TypeWallet.__name__}) | "
                               f"Balance: {balance:.8f} TON")

                _transfer_amount = balance - TON_FEE
                if _transfer_amount > 0:

                    tx_hash = await wallet.transfer(
                        destination=TON_ADDRESS_FOR_SEND,
                        amount=_transfer_amount
                    )

                    logger.warning(f"[{i}] | {_ton_address_1} : {_ton_address_2} ({TypeWallet.__name__}) | "
                                   f"Успешный трансфер {_transfer_amount:.8f} TON на кошелек: {TON_ADDRESS_FOR_SEND} | hash: {tx_hash}")

                    _time_formatted = (datetime.now(timezone.utc) + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
                    _transfer_history = f"{_time_formatted} | [{i}] | {_ton_address_1} : {_ton_address_2} ({TypeWallet.__name__}) => {TON_ADDRESS_FOR_SEND} | {_transfer_amount:.8f} | {tx_hash}\n"
                    await write_transfer_logs(_transfer_history)

                    await asyncio.sleep(3)

                else:
                    logger.warning(f"[{i}] | {_ton_address_1} : {_ton_address_2} ({TypeWallet.__name__}) | "
                                   f"Нет доступного баланса для вывода!")

            else:
                logger.error(f"[{i}] | {_ton_address_1} : {_ton_address_2} ({TypeWallet.__name__}) | "
                             f"Данные кошелька совпадают с кошельком для вывода: {TON_ADDRESS_FOR_SEND}!")

        except Exception as e:
            logger.error(f"[{i}] | Error transfer_ton({TypeWallet.__name__}) : {e}")


async def main():
    with open("mnemonic.txt", "r", encoding="utf-8") as f:
        mnemonics = [line.strip() for line in f if line.strip()]

    for index, mnemonic in enumerate(mnemonics):
        i = index + 1
        logger.warning(f"[{i}] | Mnemonic фраза отправлена в работу...")
        await transfer_ton(i, mnemonic)
        await asyncio.sleep(1)

    logger.warning(f"Все трансферы выполнены! Завершение...")


if __name__ == "__main__":
    asyncio.run(main())