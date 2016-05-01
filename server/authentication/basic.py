import bcrypt


def generate_password_hash(password: str) -> str:
    """
    Generates a hash of the specified password

    :param password: Password

    :return: Password hash
    """
    return bcrypt.hashpw(password, bcrypt.gensalt())


def authenticate(password: str, password_hash:str) -> bool:
    """
    Tries to authenticate the specified password with the specified password hash

    :param password: Password
    :param password_hash: Password hash

    :return: Authentication result
    """
    return bcrypt.checkpw(password, password_hash)
