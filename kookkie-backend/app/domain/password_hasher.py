from passlib.hash import pbkdf2_sha256


class PasswordHasher:
    def hash(self, password): 
        return pbkdf2_sha256.hash(password)
        
    def verify(self, hashed_password, unhashed_password):
        return pbkdf2_sha256.verify(unhashed_password, hashed_password)
