import uvicorn
from reqs import app
from conf import settings
import time


def main():
    while True:
        try:
            uvicorn_process = uvicorn.run(
                "main:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
                workers=2,
                ssl_keyfile=settings.SSL_KEYFILE,
                ssl_certfile=settings.SSL_CERTFILE,
            )
            uvicorn_process.wait()
        except ConnectionError:
            time.sleep(5)
            continue
        else:
            break


if __name__ == "__main__":
    main()
