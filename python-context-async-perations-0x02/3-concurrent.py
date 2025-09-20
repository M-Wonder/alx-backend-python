import asyncio
import aiosqlite

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("[All Users]", results)
            return results

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("[Users > 40]", results)
            return results

# Function to run both concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
