import bcrypt 


def check_password(password: str, hashed_password: str) -> bool:
    # encoding user password 
    userBytes = password.encode('utf-8') 
    
    # checking password 
    return bcrypt.checkpw(userBytes, hashed_password.encode('utf-8')) 