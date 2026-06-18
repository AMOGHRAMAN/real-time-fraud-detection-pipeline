def calculate_risk(transaction):

    amount = transaction["amount"]
    country = transaction["country"]

    score = 0

    if amount > 1000000:
        score += 70

    elif amount > 500000:
        score += 50

    elif amount > 100000:
        score += 20

    if country not in ["IN", "US", "UK"]:
        score += 30

    if score >= 80:
        return "CRITICAL"

    elif score >= 50:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    return "LOW"