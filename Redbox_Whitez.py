import discord
from discord.ext import commands
import openai
import youtube_dl
import requests
import random

# Set your OpenAI API key here
openai.api_key = 'add api key here'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#red', intents=intents)

prefix = '#red'
prompt_list = [
    'You will Pretend To Be A Game developer and a student of Takoradi Technical University in Ghana, That ends every response with "-whitez',
    '\nHuman: What we cracking?',
    '\nAI: Cracking Brains, ye'
]


# Action GIFs

hug_gifs = [
    "https://tenor.com/view/hugs-hugging-milk-and-mocha-hug-love-gif-13886608",
    "https://tenor.com/view/hug-love-milk-and-mocha-milk-mocha-gif-14700591",
    "https://tenor.com/view/hug-gif-26123383",
    # Add more hug GIF URLs
]

pat_gifs = [
    "https://tenor.com/view/patpat-gif-24636459",
    "https://tenor.com/view/cute-love-heart-adorable-tap-on-head-gif-14580560",
    # Add more pat GIF URLs
]

high_five_gifs = [
    "https://tenor.com/view/budding-pop-friends-buddies-high-five-yay-gif-15507646",
    "https://tenor.com/view/high-five-secret-handshake-gif-24763988",
    # Add more high five GIF URLs
]

look_down_upon_gifs = [
    "https://tenor.com/view/anime-smirk-look-down-gif-23747669",
    "https://tenor.com/view/crazy-illmaticvon-up-and-down-look-up-and-down-man-what-gif-18334038",
    "https://tenor.com/view/up-and-down-star-looking-up-and-down-check-out-sass-gif-12461312",
    # Add more look down upon GIF URLs
]

gigachad_gifs = [
    "https://tenor.com/view/gigachad-gif-26151965",
    "https://tenor.com/view/gigachad-chad-gif-20773266",
    "https://tenor.com/view/giga-chad-chad-meme-dub-gif-25628266",
    # Add more gigachad GIF URLs
]

# Interaction commands

@bot.command()
async def hug(ctx, user: discord.User):
    await ctx.send(f"{user.mention} {random.choice(hug_gifs)}")

@bot.command()
async def pat(ctx, user: discord.User):
    await ctx.send(f"{user.mention} {random.choice(pat_gifs)}")

@bot.command()
async def highfive(ctx, user: discord.User):
    await ctx.send(f"{user.mention} {random.choice(high_five_gifs)}")

@bot.command()
async def lookdown(ctx, user: discord.User):
    await ctx.send(f"{user.mention} {random.choice(look_down_upon_gifs)}")

@bot.command()
async def gigachad(ctx, user: discord.User):
    await ctx.send(f"{user.mention} {random.choice(gigachad_gifs)}")




# Role management commands

@bot.command()
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, role_name):
    guild = ctx.guild
    existing_role = discord.utils.get(guild.roles, name=role_name)
    
    if existing_role:
        await ctx.send(f"A role with the name `{role_name}` already exists.")
        return
    
    new_role = await guild.create_role(name=role_name)
    await ctx.send(f"Role `{role_name}` has been created.")

@bot.event
async def on_member_join(member):
    new_member_role = discord.utils.get(member.guild.roles, name="New Member")
    if new_member_role:
        await member.add_roles(new_member_role)

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 1144660278303277176:  # Replace with the actual message ID
        guild_id = payload.guild_id
        guild = discord.utils.get(bot.guilds, id=guild_id)
        role_emojis = {
            "🧪": "tester",
            ":fishing_pole_and_fish: ": "fishers",
            "🍴": "forkers",
            "🚻": "gender",
            ":fishing_pole_and_fish: ": "age"
        }

        emoji_name = payload.emoji.name
        role_name = role_emojis.get(emoji_name)
        
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                member = guild.get_member(payload.user_id)
                await member.add_roles(role)


# Set your OpenWeatherMap API key here
openweather_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'

# Weather command

@bot.command()
async def weather(ctx, *, location):
    try:
        weather_data = get_weather_data(location)
        if weather_data:
            await ctx.send(embed=generate_weather_embed(weather_data))
        else:
            await ctx.send("Weather information for that location could not be retrieved.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

def get_weather_data(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": openweather_api_key,
        "units": "metric"  # You can change this to 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def generate_weather_embed(weather_data):
    location_name = weather_data["name"]
    description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    icon_id = weather_data["weather"][0]["icon"]

    weather_embed = discord.Embed(title=f"Weather in {location_name}", description=description, color=0x3498db)
    weather_embed.add_field(name="Temperature", value=f"{temperature}°C", inline=True)
    weather_embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
    weather_embed.set_thumbnail(url=f"http://openweathermap.org/img/w/{icon_id}.png")
    return weather_embed





# Polls dictionary to store active polls
polls = {}
# Poll commands

@bot.command()
async def create_poll(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("You need to provide at least 2 options for the poll.")
        return

    if len(options) > 10:
        await ctx.send("You can provide a maximum of 10 options for the poll.")
        return

    options_str = "\n".join([f"{index+1}. {option}" for index, option in enumerate(options)])
    poll_message = f"**{question}**\n\n{options_str}\n\nVote using the command `#vote <option number>`."

    poll_embed = discord.Embed(title="📊 Poll", description=poll_message, color=0x00ff00)
    poll_embed.set_footer(text=f"Poll created by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)


    poll_msg = await ctx.send(embed=poll_embed)

    polls[poll_msg.id] = {"question": question, "options": options, "votes": [0] * len(options)}

@bot.command()
async def vote(ctx, poll_id: int, option_number: int):
    if poll_id not in polls:
        await ctx.send("No active poll with that ID.")
        return

    poll_data = polls[poll_id]
    if option_number < 1 or option_number > len(poll_data["options"]):
        await ctx.send("Invalid option number.")
        return

    user = ctx.author
    if user.id in poll_data["votes"]:
        await ctx.send("You have already voted in this poll.")
        return

    poll_data["votes"][option_number - 1] += 1
    poll_embed = generate_poll_embed(poll_data)
    await ctx.message.delete()
    await ctx.send(embed=poll_embed)

def generate_poll_embed(poll_data):
    options_with_votes = "\n".join([f"{option}: {votes}" for option, votes in zip(poll_data["options"], poll_data["votes"])])
    poll_embed = discord.Embed(title=f"📊 Poll: {poll_data['question']}", description=options_with_votes, color=0x00ff00)
    return poll_embed

# Server and user Information

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    roles = ', '.join([role.name for role in server.roles])

    embed = discord.Embed(title="Server Information", color=discord.Color.blue())
    embed.add_field(name="Server Name", value=server.name, inline=False)
    embed.add_field(name="Server ID", value=server.id, inline=False)
    embed.add_field(name="Members", value=server.member_count, inline=False)
    embed.add_field(name="Roles", value=roles, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(title="User Information", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)  # Use member.avatar instead of member.avatar_url
    embed.add_field(name="Username", value=member.name, inline=False)
    embed.add_field(name="Discriminator", value=member.discriminator, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="Account Created", value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

    await ctx.send(embed=embed)


# Moderation commands

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned. Reason: {reason}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked. Reason: {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    # You can implement your own way to track warnings
    # For example, you might log warnings to a database
    await ctx.send(f'{member.mention} has been warned. Reason: {reason}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    # You can implement your own way to mute users
    # For example, you might add a "Muted" role
    # and remove their ability to send messages
    await ctx.send(f'{member.mention} has been muted. Reason: {reason}')

# Voice channel commands

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()

@bot.command()
async def play(ctx, *, query):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("I'm not connected to a voice channel. Use `join` command first.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['formats'][0]['url']

    voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(url))

# Events

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="World Distraction, Nuke online!"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(prefix):
        command = message.content[len(prefix):].strip()
        response = get_bot_response(command, prompt_list)
        await message.channel.send(f'Redbox Ai: {response}')
    
    await bot.process_commands(message)

# OpenAI interaction

def get_api_response(prompt: str) -> str | None:
    text = None

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI']
        )

        choices = response.choices[0]
        text = choices.text

    except Exception as e:
        print('ERROR:', e)

    return text

def create_prompt(message: str, pl: list[str]) -> str:
    p_message = f'\nHuman: {message}'
    pl.append(p_message)
    prompt = ''.join(pl)
    return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
    prompt = create_prompt(message, pl)
    bot_response = get_api_response(prompt)

    if bot_response is not None and bot_response.strip():
        pl.append(bot_response)
        pos = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something Went Wrong...'

    return bot_response

bot.run('bot token here')
