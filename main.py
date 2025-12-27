import os
from pyrogram import Client
from aiohttp import web

# --- TERI DETAILS ---
API_ID = 31334323
API_HASH = "d55ae0078019695fce2e7056d87832cb"
BOT_TOKEN = "8362775728:AAGFSIGZC2DYRJSPSL67UCJFlU5ffPDXYj8"
CHANNEL_ID = "voxohost"

# --- BOT CONFIG ---
app = Client("my_test_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Bhai Tera Server Mast Chal Raha Hai! 🔥")

@routes.get("/stream/{msg_id}")
async def stream_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        
        # Channel se message dhundna
        msg = await app.get_messages(CHANNEL_ID, msg_id)
        
        if not msg or not msg.video:
            return web.Response(text="❌ Video nahi mili! Channel me check kar ID sahi hai kya.", status=404)
        
        # Streaming Logic
        async def file_generator():
            async for chunk in app.stream_media(msg):
                yield chunk

        # Browser ko batana ki ye video hai
        return web.Response(
            body=file_generator(),
            headers={
                "Content-Type": "video/mp4",
                "Content-Disposition": f'inline; filename="video.mp4"'
            }
        )
    except Exception as e:
        return web.Response(text=f"Error aaya bhai: {e}", status=500)

# --- FIX: STARTUP LOGIC ---
# Ye function Bot ko Server ke sath hi start karega
async def on_startup(web_app):
    print("Bot Start ho raha hai...")
    await app.start()
    print("Bot Connected!")

# Ye function Bot ko safely band karega
async def on_cleanup(web_app):
    await app.stop()
    print("Bot Stopped.")

def create_app():
    web_app = web.Application()
    web_app.add_routes(routes)
    # Bot ko server loop ke sath jod diya
    web_app.on_startup.append(on_startup)
    web_app.on_cleanup.append(on_cleanup)
    return web_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # run_app automatically loop handle karega
    web.run_app(create_app(), port=port)
    
