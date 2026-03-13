import asyncpg
import os


class Database:
    def __init__(self):
        self.pool = None

    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "grades"),
            host=os.getenv("DB_HOST", "db"),
            port=int(os.getenv("DB_PORT", "5432")),
            min_size=1,
            max_size=20,
        )
        return self.pool

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.pool:
            await self.pool.close()


db = Database()
