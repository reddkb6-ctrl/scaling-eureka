import os
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
from dotenv import load_dotenv

load_dotenv()

TEST_GUILD_ID = 1517823070012706836
TEST_GUILD = discord.Object(id=TEST_GUILD_ID)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# 🃏 TRADING CARD SYSTEM
# ----------------------------

CARDS = {
    "rare": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321499508052049/F47E7E8D-159F-4AB2-B05A-224E406FF2F4.png",
    "godly": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500044791858/DEF80D5F-1E7B-489F-A30C-56822B1075CB.png",
    "overpowered": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500317290617/3CFA23A5-2C53-48B2-8C21-34CBB44242C1.png",
    "epic": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500602761357/5E247489-1BA6-4B81-9EF1-5E346D32E598.png",
    "legendary": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500912877649/2FAAA87C-B4D4-437C-B6A9-74ACCD7462B2.png",
    "uncommon": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321501399548034/0D1A5228-5018-4622-8290-3ACC46EE0930.png",
}

CARD_NAMES = {
    "rare": "-",
    "godly": "-",
    "overpowered": "-",
    "epic": "-",
    "legendary": "-",
    "uncommon": "-"
}

inventory = {}  # user_id -> list of cards

def add_card(user_id: int, card_id: str):
    inventory.setdefault(user_id, [])
    inventory[user_id].append(card_id)

# ----------------------------
# BOT READY
# ----------------------------

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=TEST_GUILD)
        print(f"⚡ Synced {len(synced)} command(s) to test guild.")

        global_synced = await bot.tree.sync()
        print(f"🌍 Synced {len(global_synced)} global command(s).")

    except Exception as e:
        print(f"❌ Sync Error: {e}")

    print(f"✅ Logged in as {bot.user}")

# ----------------------------
# STATUS INPUT
# ----------------------------

async def terminal_status_listener():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            new_status = await asyncio.to_thread(input, "Status: ")
            if new_status.strip():
                await bot.change_presence(activity=discord.Game(name=new_status))
        except:
            pass
        await asyncio.sleep(1)

# ----------------------------
# FUN COMMANDS
# ----------------------------

@bot.tree.command(name="owner")
async def owner(interaction: discord.Interaction):
    await interaction.response.send_message(
        "👑 Owner: Aarav <@1015328404494635038>"
    )

@bot.tree.command(name="finwood")
async def finwood(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🐐 Finwood is the GOAT."
    )

@bot.tree.command(name="hug")
@app_commands.describe(user="Who do you want to hug?")
async def hug(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(
        f"{interaction.user.mention} hugs {user.mention} 🤗💞"
    )

# ----------------------------
# CARD PACK SYSTEM
# ----------------------------

@bot.tree.command(name="pack", description="Open a card pack 🎁")
async def pack(interaction: discord.Interaction):
    card_id = random.choice(list(CARDS.keys()))
    add_card(interaction.user.id, card_id)

    embed = discord.Embed(
        title=f"You pulled {CARD_NAMES[card_id]} 🎉",
        color=discord.Color.purple()
    )
    embed.set_image(url=CARDS[card_id])

    await interaction.response.send_message(embed=embed)

# ----------------------------
# VIEW INVENTORY
# ----------------------------

@bot.tree.command(name="cards", description="View your card collection")
async def cards(interaction: discord.Interaction):
    user_cards = inventory.get(interaction.user.id, [])

    if not user_cards:
        return await interaction.response.send_message("You have no cards yet!")

    text = ""
    for c in user_cards:
        text += f"• {CARD_NAMES[c]}\n"

    await interaction.response.send_message(f"📦 Your Cards:\n{text}")

# ----------------------------
# TRADE SYSTEM
# ----------------------------

@bot.tree.command(name="trade", description="Trade a card with another user")
@app_commands.describe(
    user="User to trade with",
    card="Card you want to give"
)
async def trade(interaction: discord.Interaction, user: discord.User, card: str):
    card = card.lower()

    if card not in CARDS:
        return await interaction.response.send_message("Invalid card!")

    user_inv = inventory.get(interaction.user.id, [])

    if card not in user_inv:
        return await interaction.response.send_message("You don't own that card!")

    # remove from sender
    user_inv.remove(card)

    # give to receiver
    add_card(user.id, card)

    await interaction.response.send_message(
        f"🔁 {interaction.user.mention} traded **{CARD_NAMES[card]}** to {user.mention}"
    )

# ----------------------------
# RUN BOT
# ----------------------------

async def main():
    async with bot:
        asyncio.create_task(terminal_status_listener())
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

asyncio.run(main())