from django.contrib.auth.hashers import Argon2PasswordHasher

class CustomArgon2PasswordHasher(Argon2PasswordHasher):

    algorithm = "custom_argon2"

    def encode(self, password, salt):
        print(f"Encoding password with {self.algorithm}")
        return super().encode(password, salt)

    def verify(self, password, encoded):
        print(f"Verifying password with {self.algorithm}")
        return super().verify(password, encoded)