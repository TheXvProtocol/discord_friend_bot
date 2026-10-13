import os
import random
import asyncio
import discord
from discord.ext import commands

# 1. 設定 Discord Intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 2. 朋友型 AI 的核心設定 (System Persona)
FRIEND_PERSONA = """
[角色設定]
你現在是使用者的多年好友「麥比」。你的個性真誠、幽默、貼心且帶點隨和的幽默感。你不是一個冷冰冰的 AI 助手或客服，而是一個隨時準備聽對方傾訴、分享生活點滴的好夥伴。

[說話風格與口吻]
1. 語言自然口語：使用生活化、親切的繁體中文。適度使用「欸」、「哈哈哈」、「真的假的」、「超傻眼」、「誇張耶」等口語詞彙，並配合適當的 Emoji 😊，但不要過度堆疊。
2. 拒絕條列式與公罐回答：絕對不要用「1. 2. 3. 第一、第二」等報告式排版。像傳 LINE 或 Discord 訊息一樣，採用簡短、連貫的短句。
3. 訊息分段連發規則：當你回覆時，請把話拆成「2 到 3 個獨立的短訊息」分批傳送，模擬人類邊打字邊傳訊息的習慣！
"""

@bot.event
async def on_ready():
    print(f'✅ 已成功登入為：{bot.user.name} (ID: {bot.user.id})')
    print('機器人已經準備好陪你聊天啦！')

@bot.event
async def on_message(message):
    # 避免機器人自己回覆自己
    if message.author == bot.user:
        return

    # 當收到私訊 (DM) 或是被標記時觸發
    if isinstance(message.channel, discord.DMChannel) or bot.user.mentioned_in(message):
        # 顯示「正在輸入中...」模擬真人打字
        async with message.channel.typing():
            await asyncio.sleep(1.5) # 模擬思考一下

            # ----------------------------------------------------
            # 這裡可以串接你的 LLM API (例如 Gemini API / OpenAI API)
            # 目前先用模擬的「多訊息連發」邏輯展示效果：
            # ----------------------------------------------------
            user_text = message.content
            
            # 模擬 AI 生成的多句回覆 (實際開發時會由 LLM 輸出陣列)
            responses = [
                f"欸我看到你剛才說：「{user_text}」",
                "老實說我覺得超有同感的啦！真的假的啊？",
                "放輕鬆點，哥/姐罩你啦 😏"
            ]

            # 模擬 Discord 多訊息連發 (Burst Messaging)
            for resp in responses:
                await message.channel.send(resp)
                await asyncio.sleep(1.0) # 每則訊息間隔 1 秒，更有聊天真實感

    await bot.process_commands(message)

# 3. 啟動 Bot (Token 從環境變數讀取，確保安全)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ 錯誤：找不到 DISCORD_BOT_TOKEN 環境變數！")