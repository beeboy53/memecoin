import re

def detect_chain(address: str):
    if address.startswith("0x") and len(address) == 42:
        return "evm"

    if re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", address):
        return "solana"

    return None
