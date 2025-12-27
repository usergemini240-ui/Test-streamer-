import os
from pyrogram import Client
from quart import Quart, request, Response

# --- TERI DETAILS ---
API_ID = 31334323
API_HASH = "d55ae0078019695fce2e7056d87832cb"
BOT_TOKEN = "8362775728:AAGFSIGZC2DYRJSPSL67UCJFlU5ffPDXYj8"
CHANNEL_ID = "voxohost" 

# --- SERVER SETUP (No-Crash Logic) ---
app = Quart(__name__)
client = Client("voxohost_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.before_serving
async def start_bot():
    print("Bot Start ho raha hai...")
    await client.start()
    print("Bot Mast Chal Gaya! 🚀")

@app.after_serving
async def stop_bot():
    await client.stop()
    print("Bot Band ho gaya.")

@app.route('/')
async def home():
    return "Tera 4K Video Server Ready Hai! 🔥"

@app.route('/stream/<int:msg_id>')
async def stream_video(msg_id):
    try:
        # Message dhoondho
        msg = await client.get_messages(CHANNEL_ID, msg_id)
        
        if not msg or not msg.video:
            return "Video nahi mili bhai! ID check kar.", 404

        # --- 4K STREAMING LOGIC ---
        # Ye chunk-by-chunk data bhejega taaki phone hang na ho
        async def generate():
            async for chunk in client.stream_media(msg):
                yield chunk

        # Browser ko headers bhejo
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Disposition': f'inline; filename="video.mp4"'
        }
        
        return Response(generate(), headers=headers)

    except Exception as e:
        return f"Error: {e}", 500

# Note: Render isko Procfile ke through chalayega (Uvicorn)
