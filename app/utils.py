from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hashes the password
def hasher(password: str):
    return pass_context.hash(password)

#compares the entered password and the hash
def verify(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)