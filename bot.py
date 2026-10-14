import os
import asyncio
import discord
from discord.ext import commands
from google import genai
from google.genai import types

# 1. 初始化 Gemini Client
# 請確保在 Render 的 Environment 變數中加入 GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# 2. 設定 Discord Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 定義小麥的人設與 burst messaging (多訊息連發) 指令
SYSTEM_INSTRUCTION = """
你是一個名叫「小麥」的好朋友。說話風格自然、隨性、帶點關心，就像真的朋友在用通訊軟體聊天一樣。
回覆時請遵循以下原則：
1. 不要用太正式或機器人的語氣。
2. 每次回覆時，請把你的話拆成 2 到 3 個短句（分段傳送），模擬真人傳訊息時「傳多個泡泡」的習慣。
3. 如果使用者傳送訊息，請用 JSON 格式回傳一個包含多個字串的陣列，例如：["第一句", "第二句"]，這樣程式才能幫你分開傳送。
"""

@bot.event
async def on_ready():
    print(f"✨ 機器人已成功登入！帳號名稱：{bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 當收到訊息時，呼叫 Gemini API 生成小麥的回覆
    if message.content:
        async with message.channel.typing():
            try:
                # 呼叫 Gemini 2.5 模型
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=message.content,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.8,
                    ),
                )
                
                reply_text = response.text.strip()
                
                # 模擬朋友的「多訊息連發」：如果 AI 回覆包含換行，我們就拆成多則訊息依序發送
                messages_to_send = [m.strip() for m in reply_text.split("\n") if m.strip()]
                
                for msg in messages_to_send:
                    await asyncio.sleep(1.0) # 模擬打字與思考的間隔時間
                    await message.channel.send(msg)
                    
            except Exception as e:
                await message.channel.send("哎呀，剛剛恍神了一下，你剛剛說什麼？😅")
                print(f"Gemini API 錯誤: {e}")

    await bot.process_commands(message)

# 3. 啟動 Bot
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    print("❌ 錯誤：找不到 DISCORD_BOT_TOKEN 環境變數！")
else:
    try:
        bot.run(TOKEN)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            print("🚨 觸發 Discord 429 頻率限制，請等待冷卻後再試。")
        else:
            print(f"❌ 發生 HTTP 錯誤: {e}")