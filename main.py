import discord
from discord.ext import commands
import os

# ===== TOKEN =====
TOKEN = os.environ("TOKEN")

# ===== 頻道設定 =====
HONEYPOT_CHANNELS = {1492474797555187844, 1479671657714024620}

# ===== intents =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== 啟動 =====
@bot.event
async def on_ready():
    print(f"✅ Bot 已上線：{bot.user}")

# ===== 監聽訊息 =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 如果在誘餌頻道
    if message.channel.id in HONEYPOT_CHANNELS:
        try:
            await message.delete()

            # 嘗試封鎖（如果 bot 有權限）
            await message.author.ban(reason="在誘餌頻道發言")

            print(f"🚫 已封鎖：{message.author} ({message.author.id})")

        except discord.Forbidden:
            print("❌ 權限不足：無法封鎖用戶")
        except Exception as e:
            print(f"⚠️ 錯誤：{e}")

    # 讓指令正常運作
    await bot.process_commands(message)

# ===== 啟動 bot =====
bot.run(TOKEN)
