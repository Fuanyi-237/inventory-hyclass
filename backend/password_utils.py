from passlib.context import CryptContext

# Support multiple schemes to avoid local environment issues with bcrypt backends.
# pbkdf2_sha256 is pure-Python and very reliable; bcrypt is kept for verifying existing hashes.
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
