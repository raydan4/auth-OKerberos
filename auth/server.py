import aiohttp
from fastapi import FastAPI
from base64 import b64encode
import ujson
from Crypto.Hash import SHA256
import crypto
from config import key

app = FastAPI()


async def make_request(url: str, username: str, password: str) -> dict:
    timeout = aiohttp.ClientTimeout(total=35)
    params = {"username": username, "password": password}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, params=params) as resp:
            text = await resp.text("UTF-8")
            resp = ujson.loads(text)
            return resp


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/token")
async def login(username: str, password: str):
    try:
        url = "http://validate.php"
        resp = await make_request(url, username, password)
        valid, token = resp["valid"], resp["token"]
        h = SHA256.new()
        h.update(password.encode("UTF-8"))
        hash = h.hexdigest()
        resp = str(crypto.aes256_encrypt(key, bytes(token)))
        return b64encode(
            crypto.aes256_encrypt(hash, f'{{"auth": "fail", "token": {resp if valid else ""}}}'.encode("UTF-8")))
    except Exception as e:
        print(f'An exception has occurred: {e}')
        return [{"error": e}]


def test():
    # token =
    # resp = str(crypto.aes256_encrypt(key, bytes(token)))
    h = SHA256.new()
    h.update("password".encode("UTF-8"))
    hash = h.digest()
    # resp = str(crypto.aes256_encrypt(key, bytes(token)))
    temp = b64encode(crypto.aes256_encrypt('{"auth": "fail", "token": ""}'.encode('UTF-8'), hash))
    print(f'encoded: {temp}')


if __name__ == '__main__':
    test()
