import asyncio
import websockets
import json
import subprocess
import yt_dlp
import os  # Thêm thư viện os để lấy PORT

ESP_SAMPLE_RATE = 24000 

class YouTubeService:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
        }

    def get_audio_stream_url(self, query):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if 'entries' in info: video = info['entries'][0]
                else: video = info
                return {"title": video['title'], "url": video['url']}
        except Exception as e:
            print(f"Lỗi YouTube: {e}")
            return None

async def stream_audio_to_esp32(websocket, audio_url):
    await websocket.send(json.dumps({"type": "tts", "state": "start"}))
    
    # FFmpeg command
    command = [
        'ffmpeg', '-re', '-i', audio_url, '-f', 's16le', '-ac', '1',
        '-ar', str(ESP_SAMPLE_RATE), '-vn', '-logloglevel', 'quiet', 'pipe:1'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    chunk_size = 4096
    
    try:
        while True:
            data = process.stdout.read(chunk_size)
            if not data: break
            await websocket.send(data)
            await asyncio.sleep(0.005)
    except Exception:
        pass
    finally:
        process.kill()
        await websocket.send(json.dumps({"type": "tts", "state": "stop"}))

async def handle_xiaozhi_connection(websocket):
    print("ESP32 Connected!")
    try:
        async for message in websocket:
            # Logic xử lý lệnh ở đây (như bài trước)
            if isinstance(message, str):
                 # Demo: Nếu nhận text bất kỳ, thử mở nhạc test
                 # Thực tế bạn ghép logic STT vào đây
                 pass
    except:
        pass

async def main():
    # QUAN TRỌNG: Lấy PORT từ Render, nếu không có thì dùng 8080
    port = int(os.environ.get("PORT", 8080))
    print(f"Server listening on port {port}")
    
    # Listen trên 0.0.0.0 để Cloud route được traffic
    async with websockets.serve(handle_xiaozhi_connection, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())