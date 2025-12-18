import re

def check_length(password):
    return len(password) >= 12

def check_uppercase(password):
    return any(c.isupper() for c in password)

def check_lowercase(password):
    return any(c.islower() for c in password)

def check_digit(password):
    return any(c.isdigit() for c in password)

def check_special(password):
    return re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None
