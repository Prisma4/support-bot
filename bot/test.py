import httpx


url = "http://194.87.220.226:8000/tickets/tickets/"


headers = {
    "X-Telegram-Bot-Api-Token": "c8e26823-4c10-4541-8335-7124b97b37ac",
    "X-Telegram-User-Id": "1234"
}


async def test_authentication():
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

import asyncio
asyncio.run(test_authentication())
