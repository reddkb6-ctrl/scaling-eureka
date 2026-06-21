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

# -----------------------------
# TRADING CARD SYSTEM
# -----------------------------

cards = [
    {"name": "Card 1", "url": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321499508052049/F47E7E8D-159F-4AB2-B05A-224E406FF2F4.png"},
    {"name": "Card 2", "url": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500044791858/DEF80D5F-1E7B-489F-A30C-56822B1075CB.png"},
    {"name": "Card 3", "url": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500317290617/3CFA23A5-2C53-48B2-8C21-34CBB44242C1.png"},
    {"name": "Card 4", "url": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500602761357/5E247489-1BA6-4B81-9EF1-5E346D32E598.png"},
    {"name": "Card 5", "url": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321500912877649/2FAAA87C-B4D4-437C-B6A9-74ACCD7462B2.png"},
    {"name": "Card 6", "url": "https://cdn.discordapp.com/attachments/1416122220459065607/1518321501399548034/0D1A5228-5018-4622-8290-3ACC46EE0930.png"},
]

user_cards = {}  # user_id -> list of card indexes

def add_card(user_id: int, card_index: int):
    user_cards.setdefault(user_id, []).append(card_index)

# -----------------------------
# BOT READY
# -----------------------------

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=TEST_GUILD)
        print(f"⚡ Synced {len(synced)} command(s) to test guild.")

        global_synced = await bot.tree.sync()
        print(f"🌍 Synced {len(global_synced)} global command(s).")

    except Exception as e:
        print(f"❌ Sync Error: {e}")

    print(f"✅ Logged in successfully as {bot.user}")

# -----------------------------
# STATUS INPUT
# -----------------------------

async def terminal_status_listener():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            new_status = await asyncio.to_thread(
                input,
                "Enter new bot status (or press Enter to skip): "
            )
            if new_status.strip():
                await bot.change_presence(activity=discord.Game(name=new_status))
                print(f"--> Bot status changed to: Playing {new_status}\n")
        except Exception as e:
            print(f"Status listener error: {e}")
        await asyncio.sleep(1)

# -----------------------------
# ORIGINAL FUN COMMANDS
# -----------------------------

@bot.tree.command(name="owner", description="Find out who owns this awesome bot!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def owner(interaction: discord.Interaction):
    await interaction.response.send_message(
        "👑 The owner of this bot is **Aarav!** <@1015328404494635038>!! he is soo tuff trust"
    )

@bot.tree.command(name="finwood", description="Who is he?")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def finwood(interaction: discord.Interaction):
    await interaction.response.send_message(
        "He is the GOAT. Thank you **finwood** for everything! 🐐"
    )

@bot.tree.command(name="rps", description="Play Rock, Paper, Scissors!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.choices(choice=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors")
])
async def rps(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    user_choice = choice.value
    bot_choice = random.choice(["rock", "paper", "scissors"])

    if user_choice == bot_choice:
        result = "It's a tie! 👔"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        result = "You win! 🎉"
    else:
        result = "I win! 🤖"

    await interaction.response.send_message(
        f"You chose **{user_choice}**, I chose **{bot_choice}**. {result}"
    )

@bot.tree.command(name="coinflip", description="Flip a coin in the chat!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await interaction.response.send_message(f"🪙 The coin landed on: **{result}**")

@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(question="The question you want to ask the 8-ball")
async def eightball(interaction: discord.Interaction, question: str):
    responses = [
        "It is certain.",
        "Without a doubt.",
        "Probably broskid.",
        "Outlook good.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Don't count on it.",
        "My reply is no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    reply = random.choice(responses)
    await interaction.response.send_message(
        f"❓ **Question:** {question}\n🎱 **8-Ball says:** {reply}"
    )

@bot.tree.command(name="roll", description="Roll a dice in the chat!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(sides="How many sides should the dice have? (Default is 6)")
async def roll(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        return await interaction.response.send_message(
            "❌ A die must have at least 2 sides!",
            ephemeral=True
        )

    result = random.randint(1, sides)
    await interaction.response.send_message(
        f"🎲 You rolled a **{result}** (out of {sides} sides!)"
    )

@bot.tree.command(name="guess", description="Guess a secret number between 1 and 50!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(number="Your guess")
async def guess(interaction: discord.Interaction, number: int):
    secret_number = random.randint(1, 50)

    if number == secret_number:
        await interaction.response.send_message(
            f"🎉 **Correct!** You guessed the secret number **{secret_number}**!"
        )
    elif number < secret_number:
        await interaction.response.send_message(
            f"📉 Too low! Your guess: `{number}`. (The answer was `{secret_number}`!)"
        )
    else:
        await interaction.response.send_message(
            f"📈 Too high! Your guess: `{number}`. (The answer was `{secret_number}`!)"
        )

@bot.tree.command(name="serverinfo", description="Displays information about the current server.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        return await interaction.response.send_message(
            "❌ This command can only be used inside a server.",
            ephemeral=True
        )

    embed = discord.Embed(
        title=f"{guild.name} Info",
        color=discord.Color.blue()
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="Owner", value=str(guild.owner), inline=True)
    embed.add_field(name="Total Members", value=str(guild.member_count), inline=True)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%B %d, %Y"), inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="purge", description="Deletes a specified number of messages from the channel.")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
@app_commands.describe(amount="The number of messages to delete")
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(
        f"🗑️ Successfully deleted {len(deleted)} messages.",
        ephemeral=True
    )

@purge.error
async def purge_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        if interaction.response.is_done():
            await interaction.followup.send(
                "❌ You don't have permission to use this command!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command!",
                ephemeral=True
            )


# -----------------------------
# RUN BOT
# -----------------------------

async def main():
    async with bot:
        asyncio.create_task(terminal_status_listener())
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

asyncio.run(main())