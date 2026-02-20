from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class User:
    id: int
    name: str
    job: str


class InMemoryStore:
    def __init__(self):
        self._lock = Lock()
        self._next_id = 1
        self._users: dict[int, User] = {}

        # seed data (jako "test data" v projektu)
        self.create_user("Jan Novak", "QA")
        self.create_user("Eva Holt", "DevOps")

    def create_user(self, name: str, job: str) -> User:
        with self._lock:
            user = User(id=self._next_id, name=name, job=job)
            self._users[user.id] = user
            self._next_id += 1
            return user

    def list_users(self) -> list[User]:
        with self._lock:
            return list(self._users.values())

    def get_user(self, user_id: int) -> User | None:
        with self._lock:
            return self._users.get(user_id)