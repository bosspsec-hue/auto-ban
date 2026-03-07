import discord
import os
from discord.ext import commands

# --- 設定區 ---
TOKEN = os.environ.get('DISCORD_TOKEN')HONEYPOT_CHANNEL_ID = 1479671657714024620  # 替換成你的誘餌頻道 ID
# --------------

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # 必須開啟才能讀取訊息內容
intents.members = True          # 必須開啟才有權限封鎖成員

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'機器人已上線：{bot.user}')

@bot.event
async def on_message(message):
    # 排除機器人自己的訊息，避免無限迴圈
    if message.author == bot.user:
        return

    # 檢查是否在特定的「誘餌頻道」
    if message.channel.id == HONEYPOT_CHANNEL_ID:
        try:
            # 執行封鎖 (Ban)
            await message.author.ban(reason="在誘餌頻道發言（疑似廣告機器人）")
            print(f'已封鎖用戶: {message.author} (ID: {message.author.id})')
            
            # (選填) 刪除該訊息
            await message.delete()
        except discord.Forbidden:
            print(f'權限不足：無法封鎖 {message.author}，請檢查機器人位階。')
        except Exception as e:
            print(f'發生錯誤: {e}')

    await bot.process_commands(message)

bot.run(TOKEN)
