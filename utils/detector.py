def detect(count):
    if count <= 3:
        return "SAFE"
    elif count <= 7:
        return "ALERT"
    else:
        return "BLOCK"