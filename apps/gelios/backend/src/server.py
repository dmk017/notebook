import uvicorn
from src.config import get_settings


def start():
    settings = get_settings()
    uvicorn.run("src.main:app", host=settings.host, port=settings.port, reload=True)


if __name__ == "__main__":
    start()
