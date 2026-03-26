def predict_next(count):
    if count >= 10:
        return "CRITICAL"
    elif count >= 7:
        return "HIGH"
    elif count >= 4:
        return "MEDIUM"
    else:
        return "LOW"