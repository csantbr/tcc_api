from judge.app import Application
from judge.routers import routers
import hypercorn.asyncio
import asyncio

app = Application(routers=routers)

async def main():
    config = hypercorn.Config()
    config.bind = ["0.0.0.0:8000"]
    await hypercorn.asyncio.serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())
