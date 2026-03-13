from app.database import db
from app.schemas import GradeRecord


async def insert_grades(records: list[GradeRecord]) -> tuple[int, int]:
    async with db as pool:
        async with pool.acquire() as conn:
            await conn.execute("TRUNCATE TABLE grades RESTART IDENTITY")

            batch_size = 1000
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                query = """
                    INSERT INTO grades (date, group_name, student_name, grade)
                    VALUES ($1, $2, $3, $4)
                """
                await conn.executemany(
                    query,
                    [(r.date, r.group_name, r.student_name, r.grade) for r in batch],
                )

            stats = await conn.fetchrow("""
                SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT student_name) as total_students
                FROM grades
            """)
            return stats["total_records"], stats["total_students"]


async def get_students_more_than_3_twos() -> list[dict]:
    async with db as pool:
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT 
                student_name as full_name,
                COUNT(*) as count_twos
                FROM grades
                WHERE grade = 2
                GROUP BY student_name
                HAVING COUNT(*) > 3
                ORDER BY count_twos DESC
            """)
        return [dict(row) for row in rows]


async def get_students_less_than_5_twos() -> list[dict]:
    async with db as pool:
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT 
                student_name as full_name,
                COUNT(*) as count_twos
                FROM grades
                WHERE grade = 2
                GROUP BY student_name
                HAVING COUNT(*) < 5
                ORDER BY count_twos ASC
            """)
        return [dict(row) for row in rows]
