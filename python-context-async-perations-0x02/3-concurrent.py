import asyncio
import aiosqlite

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("airbnb.db") as db:   # our earlier schema database
        async with db.execute("SELECT id, name, email FROM Users") as cursor:
            results = await cursor.fetchall()
            print("[All Users]", results)
            return results

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("airbnb.db") as db:
        async with db.execute("SELECT id, name, age FROM Users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("[Users > 40]", results)
            return results

# Run both queries concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
