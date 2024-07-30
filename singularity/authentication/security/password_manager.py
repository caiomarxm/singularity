import bcrypt


class PasswordManager:
    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt(rounds=rounds)
        )
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
