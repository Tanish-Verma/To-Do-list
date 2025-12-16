import aiosqlite

class DataBase:

    def __init__(self):
        self.conn: aiosqlite.Connection = None

    async def connect(self):
        self.conn = await aiosqlite.connect("tasks.db")
        return

    async def init_table(self):
        async with self.conn.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await self.conn.commit()
            await cursor.close()
        return
    
    async def init_db(self):
        await self.connect()
        await self.init_table()
        return
    
    async def add_task(self, user_id: int, text: str):
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO tasks (user_id, text) VALUES (?, ?)",
                (user_id, text)
            )

            await self.conn.commit()
            return cursor.lastrowid

    async def list_task(self, user_id: int) -> str:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, text FROM tasks WHERE user_id = ? AND done = 0 ORDER BY created_at",
                (user_id,)
            )
            rows = await cursor.fetchall()

        if not rows:
            return "🎉 Your to-do list is empty!\nUse /add to create a new task."

        message = "📋 *Your To-Do List*\n\n"
        for i, (_, text) in enumerate(rows, start=1):
            message += f"{i}. {text}\n"

        return message

    async def get_uncompleted_tasks(self,user_id: int)->list:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT id, text FROM tasks WHERE user_id = ? AND done = 0 ORDER BY created_at", (user_id,))
            rows = await cursor.fetchall()
            return rows 

    async def mark_task_completed(self, user_id: int, task_id: int) -> bool:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE tasks SET done = 1 WHERE id = ? AND user_id = ? AND done = 0",
                (task_id, user_id)
            )
            updated_rows = cursor.rowcount

        await self.conn.commit()
        return updated_rows > 0
    
    async def clear_tasks(self, user_id: int) -> int:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "DELETE FROM tasks WHERE user_id = ?",
                (user_id,)
            )
            deleted_rows = cursor.rowcount

        await self.conn.commit()
        return deleted_rows
db = DataBase()