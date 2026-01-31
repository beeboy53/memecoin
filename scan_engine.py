import requests

GOPLUS_API = "https://api.gopluslabs.io/api/v1/token_security"

CHAINS = [
    1,      # Ethereum
    56,     # BSC
    137,    # Polygon
    42161,  # Arbitrum
    8453    # Base
]


def fetch_security(address):
    for chain in CHAINS:
        try:
            res = requests.get(
                f"{GOPLUS_API}/{chain}",
                params={"contract_addresses": address},
                timeout=10
            )

            result = res.json().get("result")
            if result:
                return list(result.values())[0], chain
        except:
            pass

    return None, None


def scan_token(address: str):
    data, chain = fetch_security(address)

    if not data:
        return "❌ Could not detect token on supported chains."

    score = 100
    notes = []

    if data.get("is_honeypot") == "1":
        score -= 40
        notes.append("❌ Honeypot detected")

    sell_tax = float(data.get("sell_tax", 0))
    if sell_tax > 20:
        score -= 20
        notes.append(f"⚠️ High sell tax ({sell_tax}%)")

    if data.get("is_blacklisted") == "1":
        score -= 30
        notes.append("❌ Blacklist logic detected")

    lp_count = int(data.get("lp_holder_count", 0))
    if lp_count <= 1:
        score -= 25
        notes.append("❌ Liquidity concentration risk")

    if score >= 80:
        risk = "🟢 LOW RISK"
    elif score >= 50:
        risk = "🟡 MEDIUM RISK"
    else:
        risk = "🔴 HIGH RISK"

    findings = "\n".join(notes) if notes else "✅ No major red flags"

    return f"""
Token Risk Scan

Chain ID: {chain}
Score: {score}/100
Status: {risk}

Findings:
{findings}

Disclaimer: Risk analysis only. Not financial advice.
"""
