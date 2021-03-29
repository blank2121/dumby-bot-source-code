#importing nessesary modules

import discord
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
import time
from random import choice
import json, requests

#stet up timer for how long it takes for program to go online

s=time.time()

#the quote of the day setup

url = "https://quotes15.p.rapidapi.com/quotes/random/"

querystring = {"language_code":"en"}

headers = {
    'x-rapidapi-key': "8dbd9229a5msh60edcf9aad6fea5p18d3d6jsnb9a0c89bddb2",
    'x-rapidapi-host': "quotes15.p.rapidapi.com"
    }

#bot data like status and prefix setup
client = commands.Bot(command_prefix="~")
videos=cycle(["https://www.youtube.com/watch?v=dQw4w9WgXcQ","https://www.youtube.com/watch?v=LD8P8Mq3rVU","https://www.youtube.com/watch?v=qHEe653pxxY",
              "https://www.youtube.com/watch?v=Za8bfjHPMrk","https://www.youtube.com/watch?v=4kK0yAP4iec","https://www.youtube.com/watch?v=s6jqZoztMSM",
              "https://www.youtube.com/watch?v=nzYDMX93JNA"])
client.remove_command("help")


@client.event
async def on_ready():
    #change_state.start()
    e=time.time()
    print(e-s)
    print("we good to go.")

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.dark_orange()
    )

    embed.set_author(name="Help")
    embed.add_field(name='~add', value="type the two numbers that you want to add after ~add.", inline=True)
    embed.add_field(name='~minus', value="type the two numbers that you want to subtract after ~minus.", inline=True)
    embed.add_field(name='~times', value="type the two numbers that you want to multipy after ~times.", inline=True)
    embed.add_field(name='~divide', value="type the two numbers that you want to divide after ~divide.", inline=True)
    embed.add_field(name='~afk', value="~afk <state: on/off> <if on: reason message> so everytime you get pings it will say you are afk and for the reason you typed.", inline=True)
    embed.add_field(name="~ping", value="tells you your ping.", inline=True)
    embed.add_field(name="~poll", value="type the message you want to poll after ~poll.", inline=True)
    embed.add_field(name="~covid", value="type deaths, hospitalized, or positive after ~covid to get that info.", inline=True)
    embed.add_field(name="~profic_pic", value="type the name of the person that has the profic picture you want to see.", inline=True)
    embed.add_field(name="~quote",value="you just get a random quote.",inline=True)
    embed.add_field(name="_ _ _ _ _ _ _ _ _ _ _ _", value="Mod commands ↓", inline=False)
    embed.add_field(name='~kick',value="type @username#0000 after ~kick(you can only do this is you have the mods role.)",inline=True)
    embed.add_field(name='~ban',value="(it bans the person) type @username#0000 after ~hammer.",inline=True)
    embed.add_field(name='~unban',value="type the person's name and then their discriminator but with out the @ (username#0000).",inline=True)
    embed.add_field(name='~clear',value="after that enter how many previous messages you want to delete.",inline=True)
    await ctx.author.send(embed=embed, delete_after=300)
    

#the basic commands/opporations

@client.command(past_context=True)
async def add(ctx, int1, int2):
    out=int(int1)+int(int2)
    await ctx.send(out)

@client.command()
async def covid(ctx, info):
    request=requests.get("https://api.covidtracking.com/v1/us/current.json").json()
    positive = request[0]["positive"]
    hospitalized = request[0]["hospitalizedCurrently"]
    deaths = request[0]["death"]
    date = request[0]["dateChecked"][0:10]
    if info=="positive":
        embed=discord.Embed(title=(f"{positive} have COVID-19 in the USA."), colour=discord.Colour.dark_magenta())
        await ctx.send(embed=embed)
    elif info=="hospitalized":
        embed=discord.Embed(title=(f"{hospitalized} are currently hospitalized with COVID-19 in the USA."), colour=discord.Colour.dark_magenta())
        await ctx.send(embed=embed)
    elif info=="deaths":
        embed=discord.Embed(title=(f"{deaths} people have died of COVID-19 in the USA since {date}."), colour=discord.Colour.dark_magenta())
        await ctx.send(embed=embed)
    else:
        await ctx.send("that is not a valid input. refer to the help command to know the proper input for this command.")

@client.command()
async def minus(ctx, int1, int2):
    out=int(int1)-int(int2)
    await ctx.send(out)

@client.command()
async def times(ctx, int1, int2):
    out=int(int1)*int(int2)
    await ctx.send(out)

@client.command()
async def divide(ctx, int1, int2):
    out=int(int1)/int(int2)
    await ctx.send(out)

@client.command()
async def profile_pic(ctx, member: discord.User):
    embed=discord.Embed(title=(f"{member.display_name}'s profile picture."))
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def poll(ctx, *, mess):
    global t
    embed=discord.Embed(colour=discord.Colour.from_rgb(181, 81, 198))
    embed.set_author(name="Poll")
    embed.add_field(name=f"{mess}",value="_ _",inline=False)
    embed.add_field(name="_ _", value="✅: option A", inline=False)
    embed.add_field(name="_ _", value="❌: option B", inline=False)
    embed.set_thumbnail(url="https://images.g2crowd.com/uploads/product/image/large_detail/large_detail_48d356bf2b41aa5c0c23a99ece81bccc/poll-everywhere.png")
    embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Made by {ctx.author}")
    t=await ctx.send(embed=embed)
    await ctx.send("@everyone")
    await t.add_reaction("✅")
    await t.add_reaction("❌")

@client.command()
async def quote(ctx):
    embed=discord.Embed(colour=discord.Colour.dark_magenta())
    response = requests.request("GET", url, headers=headers, params=querystring)

    api = json.loads(response.content)

    quote = api["content"]
    source = api['originator']
    source_name = source["name"]
    embed.add_field(name="_ _",value=quote,inline=False)
    embed.add_field(name="_ _",value=f"-{source_name}",inline=False)


    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("!rank")
    ping = (time.monotonic() - before) * 1000
    await message.delete()
    embed=discord.Embed(title=(f"{int(ping)}ms"), colour=discord.Colour.gold())
    await ctx.send(embed=embed)

@client.command()
async def afk(ctx, state,*,prompt="This person is currently afk."):
    if state=="on":
        with open("afk_mess.json", "r") as x:
            pre = json.load(x)
            with open("afk_mess.json", "w") as x:
                t={f"{ctx.author.id}": prompt}
                pre.update(t)
                json.dump(pre,x)
    elif state=="off":
       with open("afk_mess.json", "r") as x:
            pre = json.load(x)
            with open("afk_mess.json", "w") as x:
                pre.pop(str(ctx.author.id))
                json.dump(pre,x)


#mod only commands

@client.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member : discord.Member, *, reason="The hammer has done it's work."):
    embed = discord.Embed(
        colour=discord.Colour.dark_red()
    )
    embed.set_author(name=f"{member} was banned.")
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/770420594789187585/786593590440099870/Untitled151.jpg')
    embed.set_image(url="https://storage.googleapis.com/discordstreet/emojis/6b6d7cf7-5661-4add-bdc1-8b41fd2be7ef.gif")
    embed.add_field(name="_ _ _ _ _ _ _ _ _ _ _ _", value=f"{ctx.author} has banned {member}")
    await ctx.send(embed=embed)
    await member.ban(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def unban(ctx,*, member):
    embed = discord.Embed(
        colour=discord.Colour.teal()
    )
    banned_users= await ctx.guild.bans()
    member_name,member_disc=member.split('#')

    for ban_entry in banned_users:
        user=ban_entry.user

        if(user.name,user.discriminator)==(member_name,member_disc):
            await ctx.guild.unban(user)
            embed.set_author(name=f"{user} was unbanned.")
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/770420594789187585/786593590440099870/Untitled151.jpg')
            embed.set_image(url="https://i1.wp.com/sites.duke.edu/lawfire/files/2019/05/shutterstock_656449450.jpg")
            embed.add_field(name="_ _ _ _ _ _ _ _ _ _ _ _",value=f"{ctx.author} has unbanned {user}")
            await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True, administrator=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=(amount+1))


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify how many messages to delete.")

#events

@client.event
async def on_message(message):
    if message.author==client.user:
        return
    with open("afk_mess.json","r") as x:
        pre = json.load(x)
        word = message.content
        if "<@!" in message.content:
            t=word.split(">")
            for i in range(len(t)):
                if "<@!" in t[i]:
                    out=t[i].split("<@!")
                    out=out[1]
                    if str(out) in pre:
                        await message.channel.send(pre[str(out)])
                    break
        if message.content.startswith("~"):
            per = message.author
            ch = message.channel
            server = message.guild
            print(f"{per} used {message.content} on {server} in {ch}")

        await client.process_commands(message)

async def b_t():
    await client.wait_until_ready()

    while not client.is_closed():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"in {len(client.guilds)} different servers."))
        await asyncio.sleep(25)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="memes... come join.", url=next(videos)))
        await asyncio.sleep(25)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="videos that give me nastalgia."))
        await asyncio.sleep(25)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to your command. || ~help"))
        await asyncio.sleep(25)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="something."))
        await asyncio.sleep(25)
        #add yt channel
        #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="My makers youtube channe;.", url=(""))
        #await asyncio.sleep(25)
client.loop.create_task(b_t())


client.run()
