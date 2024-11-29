# plugins/web_server.py
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

def web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    return app
