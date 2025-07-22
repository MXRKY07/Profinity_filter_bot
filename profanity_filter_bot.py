import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

bot = commands.Bot(command_prefix='!', intents=intents)

# Profanity list (customize this)
BAD_WORDS = ['badword1', 'badword2', 'curseword']

# Control flag
profanity_filter_enabled = True

# Admin check
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.event
async def on_message(message):
    global profanity_filter_enabled

    if message.author.bot:
        return

    if profanity_filter_enabled:
        if any(bad_word in message.content.lower() for bad_word in BAD_WORDS):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, please avoid using offensive language.", delete_after=5)

    await bot.process_commands(message)

@bot.command()
@is_admin()
async def togglefilter(ctx):
    global profanity_filter_enabled
    profanity_filter_enabled = not profanity_filter_enabled
    status = "enabled" if profanity_filter_enabled else "disabled"
    await ctx.send(f"Profanity filter has been **{status}**.")

@bot.command()
@is_admin()
async def addword(ctx, *, word):
    word = word.lower()
    if word not in BAD_WORDS:
        BAD_WORDS.append(word)
        await ctx.send(f"Added `{word}` to the filter list.")
    else:
        await ctx.send(f"`{word}` is already in the filter list.")

@bot.command()
@is_admin()
async def removeword(ctx, *, word):
    word = word.lower()
    if word in BAD_WORDS:
        BAD_WORDS.remove(word)
        await ctx.send(f"Removed `{word}` from the filter list.")
    else:
        await ctx.send(f"`{word}` is not in the filter list.")

# Run the bot
bot.run('MTM5NzI1MzIwNzMzMTMxMTg1OA.Gt_-Vs.aech1x23AucJcYaBe3V-GdNwFCJj1ZUdnJsnwU')
