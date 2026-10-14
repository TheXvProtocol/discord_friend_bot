import os
import asyncio
import sys

print("🚀 程式開始執行...", flush=True)

try:
    import discord
    from discord.ext import commands
    print("✅ discord.py 匯入成功", flush=True)
except Exception as e:
    print(f"❌ discord.py 匯入失敗: {e}", flush=True)
    sys.exit(1)

try:
    from google import genai
    from google.genai import types
    print("✅ google-genai 匯入成功", flush=True)
except Exception as e:
    print(f"❌ google-genai 匯入失敗: {e}", flush=True)
    sys.exit(1)

# 讀取環境變數
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print(f"🔍 檢查 Token 狀態: {'已載入 (' + TOKEN[:5] + '...)' if TOKEN else '未找到！'}", flush=True)
print(f"🔍 檢查 Gemini Key 狀態: {'已載入' if GEMINI_API_KEY else '未找到！'}", flush=True)

if not TOKEN:
    print("❌ 錯誤：找不到 DISCORD_BOT_TOKEN，請檢查 Render 環境變數！", flush=True)
    sys.exit(1)

# 初始化 Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✨ 機器人已成功登入！帳號名稱：{bot.user}", flush=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content and GEMINI_API_KEY:
        async with message.channel.typing():
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=message.content,
                    config=types.GenerateContentConfig(
                        system_instruction="你是一個名叫「小麥」的好朋友，說話自然隨性，帶點關心。",
                        temperature=0.8,
                    ),
                )
                reply_text = response.text.strip()
                messages_to_send = [m.strip() for m in reply_text.split("\n") if m.strip()]
                
                for msg in messages_to_send:
                    await asyncio.sleep(1.0)
                    await message.channel.send(msg)
            except Exception as e:
                await message.channel.send("哎呀，剛剛恍神了一下，你剛剛說什麼？😅")
                print(f"Gemini API 錯誤: {e}", flush=True)

    await bot.process_commands(message)

if __name__ == "__main__":
    try:
        print("🔄 正在啟動 Discord Bot 主迴圈...", flush=True)
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ 執行 bot.run 時發生嚴重錯誤: {e}", flush=True)