import re
import bcrypt

def validate_register(email, password, username):

    emailRe = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    passwordRe = r'([A-Za-z0-9!@#$&~()\\-`.+,/\"}{]){12,64}'
    usernameRe = r'([A-Za-z0-9]){4,12}'

    if (re.fullmatch(emailRe, email)):
        emailValid = True
    else:
        emailValid = False
    
    if (re.fullmatch(passwordRe, password)):
        passwordValid = True
    else:
        passwordValid = False
    
    if (re.fullmatch(usernameRe, username)):
        usernameValid = True
    else:
        usernameValid = False
    
    return emailValid, passwordValid, usernameValid

def validate_password(password):
    passwordRe = r'([A-Za-z0-9!@#$&~()\\-`.+,/\"}{]){12,64}'

    if(re.fullmatch(passwordRe, password)):
        return True
    else:
        return False

def encrypt_password(password):
    """Encrypts the password and decodes it from utf-8 so the hash does not suffer from double encoding when being stored in the database."""

    encoded_password = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=15)

    hashed_password = bcrypt.hashpw(encoded_password, salt)

    stringPassword = hashed_password.decode("utf-8") 

    return stringPassword

def compare_password(input, stored):
    """Compares the user-provided password with the stored hash inside the database."""

    encoded_input = input.encode("utf-8")
    encoded_stored = stored.encode("utf-8")

    return bcrypt.checkpw(encoded_input, encoded_stored)