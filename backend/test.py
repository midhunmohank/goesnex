from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


print(get_password_hash("secret"))

print(verify_password("secret", "$2b$12$N3qi2UVX8RG6TPJh2xAfg.fVAfgqMfTX4ULKRiHDbaJ5O5TpeCO7W"))

