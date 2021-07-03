import discord
import asyncio
import json
import time
import random
import requests
import os
import datetime
import psutil

from discord.utils import get



with open("config.json") as f:
    config = json.load(f)

COLOR = int(config["COLOR"], 16)

VIDEO = "https://youtu.be/l86x1_GiMLA"

VERSION = "V 2.2.1"

INVITE = "https://discord.gg/8cRfBTd"

start_time = time.time()



async def database(guild):

    await client.wait_until_ready()

    with open("data.json") as f:
        data = json.load(f)

    if data.get(guild) is not None:
        del data[guild]

    data[guild] = {}
    data[guild]["prefix"] = config["PREFIX"]
    data[guild]["cooldowns"] = {}
    data[guild]["cooldowns"]["ticket"] = {}
    data[guild]["support"] = {}
    with open('data.json', 'w') as f:
        json.dump(data, f)


async def status():
    while True:
            await client.wait_until_ready()
            with open("config.json") as f:
                config = json.load(f)
            try:
                gui = await client.fetch_guild(767665471948062730)
            except:
                pass
            try:
                await client.change_presence(activity=discord.Game(config["STATUS"]), status=discord.Status.online)
            except:
                pass
            await asyncio.sleep(30)
            try:
                await client.change_presence(activity=discord.Game(PREFIX + f"help | Made by {gui.name}"), status=discord.Status.online)
            except:
                pass
            await asyncio.sleep(30)


class MyClient(discord.Client):


    async def on_raw_message_delete(self, payload):

        with open("data.json") as f:
            data = json.load(f)
         
        if payload.guild_id is not None:
         if data.get(str(payload.guild_id)) is not None:


                if data[str(payload.guild_id)]["support"].get(str(payload.channel_id)) is not None:
                    if data[str(payload.guild_id)]["support"][str(payload.channel_id)].get(str(payload.message_id)) is not None:

                            del data[str(payload.guild_id)]['support'][str(payload.channel_id)][str(payload.message_id)]
                            with open('data.json', 'w') as f:
                                json.dump(data, f)


                list = []
                for key in data[str(payload.guild_id)]["support"].keys():
                                list.append(key)

                for id1 in list:
                    list = []
                    for key in data[str(payload.guild_id)]["support"][id1].keys():
                                    list.append(key)

                    for id3 in list:
                        list = []
                        for key in data[str(payload.guild_id)]["support"][str(id1)][id3]["opened"].keys():
                                        list.append(key)

                        for id2 in list:
                            if data[str(payload.guild_id)]["support"][str(id1)][id3]["opened"][str(id2)] == payload.message_id and int(payload.channel_id) in data[str(payload.guild_id)]["support"][str(id1)][id3]["tickets"]:
                                del data[str(payload.guild_id)]["support"][str(id1)][id3]["opened"][str(id2)]
                                data[str(payload.guild_id)]["support"][str(id1)][id3]["tickets"].remove(int(id2))
                                del data[str(payload.guild_id)]["support"][str(id1)][id3]["owners"][str(id2)]
                                with open('data.json', 'w') as f:
                                                    json.dump(data, f)

                                if data[str(payload.guild_id)]["support"][str(id1)][id3]["closed"][str(id2)] == None:
                                    del data[str(payload.guild_id)]["support"][str(id1)][id3]["closed"][str(id2)]

                                    with open('data.json', 'w') as f:
                                                    json.dump(data, f)


                            if data[str(payload.guild_id)]["support"][str(id1)][id3]["closed"][str(id2)] == payload.message_id and int(payload.channel_id) in data[str(payload.guild_id)]["support"][str(id1)][id3]["tickets"]:
                                del data[str(payload.guild_id)]["support"][str(id1)][id3]["closed"][str(id2)]

                                with open('data.json', 'w') as f:
                                                    json.dump(data, f)

    async def on_guild_remove(self, guild):
        with open("data.json") as f:
            data = json.load(f)

        with open("config.json") as f:
            config = json.load(f)

        if data.get(str(guild.id)) is not None:
            del data[str(guild.id)]
            with open('data.json', 'w') as f:
                json.dump(data, f)


    async def on_guild_join(self, guild):
        with open("data.json") as f:
            data = json.load(f)

        with open("config.json") as f:
            config = json.load(f)

        await database(guild=str(guild.id))

        try:
            embed = discord.Embed(title=f"Thanks for adding `{client.user.name}` to your Server!", description="Please get sure, that I always have Administrator Permissions on your Server!\nAlso get sure, that you Setup the Bot before use the moderation commands!", color=COLOR)
            embed.add_field(name='Support', value=f"If you need help, visit our Support Server: {INVITE}")
            await guild.owner.send(embed=embed)
        except:
            pass

                



    async def on_private_channel_delete(self, channel):
        with open("data.json") as f:
            data = json.load(f)

        if data.get(str(channel.guild.id)) is not None:


            if data[str(channel.guild.id)]["support"].get(str(channel.id)) is not None:

                del data[str(channel.guild.id)]["support"][str(channel.id)]
                with open('data.json', 'w') as f:
                    json.dump(data, f)



            list = []
            for key in data[str(channel.guild.id)]["support"].keys():
                list.append(key)

            for id1 in list:
                list = []
                for key in data[str(channel.guild.id)]["support"][id1].keys():
                    list.append(key)
                for id in list:
                    if channel.id in data[str(channel.guild.id)]["support"][str(id1)][id]["tickets"]:
                        del data[str(channel.guild.id)]["support"][str(id1)][id]["opened"][str(channel.id)]
                        data[str(channel.guild.id)]["support"][str(id1)][id]["tickets"].remove(int(channel.id))
                        del data[str(channel.guild.id)]["support"][str(id1)][id]["owners"][str(channel.id)]
                        del data[str(channel.guild.id)]["support"][str(id1)][id]["closed"][str(channel.id)]

                        with open('data.json', 'w') as f:
                            json.dump(data, f)


    async def on_guild_channel_delete(self, channel):
        with open("data.json") as f:
            data = json.load(f)

        if data.get(str(channel.guild.id)) is not None:


            if data[str(channel.guild.id)]["support"].get(str(channel.id)) is not None:

                del data[str(channel.guild.id)]["support"][str(channel.id)]
                with open('data.json', 'w') as f:
                    json.dump(data, f)



            list = []
            for key in data[str(channel.guild.id)]["support"].keys():
                list.append(key)

            for id1 in list:
                list = []
                for key in data[str(channel.guild.id)]["support"][id1].keys():
                    list.append(key)
                for id in list:
                    if channel.id in data[str(channel.guild.id)]["support"][str(id1)][id]["tickets"]:
                        del data[str(channel.guild.id)]["support"][str(id1)][id]["opened"][str(channel.id)]
                        data[str(channel.guild.id)]["support"][str(id1)][id]["tickets"].remove(int(channel.id))
                        del data[str(channel.guild.id)]["support"][str(id1)][id]["owners"][str(channel.id)]
                        del data[str(channel.guild.id)]["support"][str(id1)][id]["closed"][str(channel.id)]

                        with open('data.json', 'w') as f:
                            json.dump(data, f)



    async def on_guild_role_delete(self, role):
        with open("data.json") as f:
            data = json.load(f)

        if data.get(str(role.guild.id)) is not None:


            list = []
            for key in data[str(role.guild.id)]["support"].keys():
                list.append(key)

            for id1 in list:
                list = []
                for key in data[str(role.guild.id)]["support"][id1].keys():
                                list.append(key)

                for id in list:
                    if role.id in data[str(role.guild.id)]["support"][id1][str(id)]["supportrole"]:
                        index = data[str(role.guild.id)]["support"][id1][str(id)]["supportrole"].index(role.id)
                        del data[str(role.guild.id)]["support"][id1][str(id)]["supportrole"][index]
                        with open('data.json', 'w') as f:
                            json.dump(data, f)


    async def on_ready(self):
        print(f"Logged in as {client.user}")
        with open("config.json") as f:
            config = json.load(f)

        config["ID"] = client.user.id

        with open('config.json', 'w') as f:
            json.dump(config, f)



    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.author.bot:
            return


        with open("data.json") as f:
            data = json.load(f)

        with open("config.json") as f:
            config = json.load(f)





        if not str(message.channel.type) == "private":
         if data.get(str(message.guild.id)) is not None:



            PREFIX = data[str(message.guild.id)]["prefix"]




            if message.content == PREFIX + "help":

                embed = discord.Embed(title="Categorys", color=COLOR)
                embed.add_field(name=":one:", value=PREFIX + "setup-ticket", inline=False)
                embed.add_field(name=":two:", value=PREFIX + "setprefix `NewPrefix`", inline=False)
                embed.add_field(name=":three:", value=PREFIX + "clsoe", inline=False)
                await message.channel.send(embed=embed)


            if message.content.startswith(PREFIX + "close"):
                    list = []
                    for key in data[str(message.guild.id)]["support"].keys():
                                    list.append(key)

                    for id1 in list:
                        list = []
                        for key in data[str(message.guild.id)]["support"][id1].keys():
                                        list.append(key)

                        for id in list:
                            if channel.id in data[str(message.guild.id)]["support"][id1][str(id)]["tickets"]:

                                        try:
                                            await message.add_reaction("✅")
                                            await message.add_reaction("❎")
                                        except:
                                            return

                                        def check(payload):
                                                                    return (payload.message_id == message.id and payload.user_id == message.author.id)
                                        try:
                                                        payload = await client.wait_for("raw_reaction_add", check=check, timeout=30)
                                                        if str(payload.emoji) == "❎":
                                                            await message.remove_reaction("❎", message.author)
                                                            await message.remove_reaction("❎", client.user)
                                                            await message.remove_reaction("✅", client.user)




                                                        if str(payload.emoji) == "✅":
                                                            await message.remove_reaction("✅", message.author)
                                                            await message.remove_reaction("❎", client.user)
                                                            await message.remove_reaction("✅", client.user)
                                                            overwrites = {
                                                                    message.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=False, external_emojis=False),
                                                                }
                                                            if data[str(message.guild.id)]["support"][id1][str(id)]["supportrole"] != []:
                                                                    pinged_msg_content = ""
                                                                    for role_id in data[str(message.guild.id)]["support"][id1][str(id)]["supportrole"]:
                                                                        role = guild.get_role(role_id)
                                                                        overwrites[role] = discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                                                            await message.channel.edit(overwrites=overwrites)
                                                            embed = discord.Embed(title="Closed", description=f"Ticket has closed by {message.author.mention}", color=COLOR)
                                                            await message.channel.send(embed=embed)
                                                            embed = discord.Embed(title="Closed", description="🗑️=Delete Ticket\n🔓=Reopen Ticket", color=COLOR)
                                                            mes = await message.channel.send(embed=embed)
                                                            with open("data.json") as f:
                                                                data = json.load(f)
                                                            data[str(message.guild.id)]["support"][id1][str(id)]["closed"][str(message.channel.id)] = mes.id
                                                            with open('data.json', 'w') as f:
                                                                            json.dump(data, f)
                                                            await mes.add_reaction("🗑️")
                                                            await mes.add_reaction("🔓")

                                        except asyncio.TimeoutError:
                                                await message.remove_reaction("❎", client.user)
                                                await message.remove_reaction("✅", client.user)
                                                embed = discord.Embed(title="Timeout",
                                                                      description="You run out of the time!\nThe Progress have been cancelled!",
                                                                      color=COLOR)
                                                await message.channel.send(embed=embed)
                                                return

            if message.content.startswith(PREFIX + "setup-ticket"):
                if message.author.guild_permissions.administrator:
                    embed = discord.Embed(title="SETUP TICKET", color=COLOR)
                    embed.add_field(name=':one:', value="Create a Ticket System", inline=False)
                    embed.add_field(name=':two:', value="Edit a Ticket System", inline=False)
                    embed.add_field(name=':three:', value="Delete a Ticket System", inline=False)
                    mess = await message.channel.send(embed=embed)
                    await mess.add_reaction("1️⃣")
                    await mess.add_reaction("2️⃣")
                    await mess.add_reaction("3️⃣")
                    def check(reaction, user):
                            return user.id == message.author.id and reaction.message.id == mess.id

                    try:
                        reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                        if str(reaction.emoji) == "1️⃣":
                            await mess.remove_reaction("1️⃣", message.author)
                            await mess.remove_reaction("1️⃣", client.user)
                            await mess.remove_reaction("2️⃣", client.user)
                            await mess.remove_reaction("3️⃣", client.user)

                            def check(m):
                                            return m.content is not None and m.author == message.author and  m.channel == message.channel
                            embed = discord.Embed(title="CREATE TICKET", description="In which Channel do you want to open tickets?\nWrite **no** to end this Setup", color=COLOR)
                            await mess.edit(embed=embed)
                            while True:
                                msg2 = await client.wait_for('message', check=check, timeout=120)
                                if "no" in msg2.content.lower():
                                    embed = discord.Embed(title="CREATE TICKET", description="Stopped the Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    return
                                if len(msg2.channel_mentions) == 0:
                                    embed = discord.Embed(title="CREATE TICKET", description="You don´t ping the channel or the ping can´t found\nPlease send the channel again!\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)

                                else:
                                        channel = msg2.channel_mentions[0]


                                        break

                            embed = discord.Embed(title="CREATE TICKET", description="Which Short Topic does this Ticket System have?\nWrite **no** to end this Setup", color=COLOR)
                            await mess.edit(embed=embed)
                            while True:
                                msg3 = await client.wait_for('message', check=check, timeout=120)
                                if "no" == msg3.content.lower():
                                    embed = discord.Embed(title="CREATE TICKET", description="Stopped the Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    return
                                else:
                                    if len(msg3.content) < 256:
                                        break
                                    else:
                                        embed = discord.Embed(title="CREATE TICKET", description="The Topic is too long!\nWhich Short Topic does this Ticket System have?\nWrite **no** to end this Setup", color=COLOR)
                                        await mess.edit(embed=embed)

                            embed = discord.Embed(title="CREATE TICKET", description="Which long Description does this Ticket Panel have?\nWrite **no** to end this Setup", color=COLOR)
                            await mess.edit(embed=embed)
                            while True:
                                msg = await client.wait_for('message', check=check, timeout=120)
                                if "no" == msg.content.lower():
                                    embed = discord.Embed(title="CREATE TICKET", description="Stopped the Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    return
                                else:
                                    if len(msg.content) < 2048:
                                        embed = discord.Embed(title=f"{msg3.content}", description=f"{msg.content}", color=COLOR)
                                        if msg.attachments:
                                                    if msg.attachments[0].filename.split(".")[-1].lower() in ["png", "jpg", "jpeg", "gif", "bpm"]:
                                                            file = await msg.attachments[0].to_file()
                                                            embed.set_image(url="attachment://" + file.filename)
                                                            apply = await channel.send(file=file, embed=embed)
                                                    else:
                                                        apply = await channel.send(embed=embed)
                                        else:
                                                apply = await channel.send(embed=embed)
                                    
                                        if data[str(message.guild.id)]["support"].get(str(channel.id)) is None:
                                            data[str(message.guild.id)]["support"][str(channel.id)] = {}
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)] = {}
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["startchannel"] = channel.id
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["startmessage"] = apply.id
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["supportrole"] = []
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["counter"] = 0
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["tickets"] = []
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["owners"] = {}
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["closed"] = {}
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["opened"] = {}
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["topic"] = str(msg3.content)
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["description"] = str(msg.content)
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["ticket-name"] = "ticket-{count}"
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["create-message"] = None
                                        data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["category"] = None
                                        with open('data.json', 'w') as f:
                                            json.dump(data, f)

                                        await apply.add_reaction("🎟️")

                                        embed = discord.Embed(title="CREATE TICKET", description="Ticket System created successfully", color=COLOR)
                                        await mess.edit(embed=embed)

                                        break
                                    else:
                                        embed = discord.Embed(title="CREATE TICKET", description="The Description is too long!\nWhich long Description does this Ticket Panel have?\nWrite **no** to end this Setup", color=COLOR)
                                        await mess.edit(embed=embed)



                        if str(reaction.emoji) == "2️⃣":
                            def check(m):

                                return m.content is not None and m.author == message.author and  m.channel == message.channel

                            embed = discord.Embed(title="EDIT TICKET", description="Which Ticket System do you want to edit?(Please send the Channel where the Tickets created at the moment)\nWrite **no** to end this Setup", color=COLOR)
                            await mess.edit(embed=embed)
                            while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="EDIT TICKET", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if len(msg.channel_mentions) == 0:
                                                    embed = discord.Embed(title="EDIT TICKET", description="This is an Invalid Channel.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)

                                                chan = msg.channel_mentions[0]

                                                if data[str(message.guild.id)]["support"].get(str(chan.id)) is None:
                                                    embed = discord.Embed(title="EDIT TICKET", description="This is an Invalid Channel.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                            embed = discord.Embed(title="EDIT TICKET", description="\u200b", color=COLOR)
                            embed.add_field(name=':one:', value="Edit the Ticket Roles", inline=False)
                            embed.add_field(name=':two:', value="Edit the Ticket Topic and Description", inline=False)
                            embed.add_field(name=':three:', value="Edit the Channel name from created Tickets", inline=False)
                            embed.add_field(name=':four:', value="Edit the Message in created Tickets", inline=False)
                            embed.add_field(name=':five:', value="Edit the Ticket Category, where tickets created in", inline=False)
                            embed.add_field(name=':six:', value="Set a new Ticket Create Channel", inline=False)
                            await mess.edit(embed=embed)
                            await mess.remove_reaction("2️⃣", message.author)
                            await mess.add_reaction("4️⃣")
                            await mess.add_reaction("5️⃣")
                            await mess.add_reaction("6️⃣")
                            def check(reaction, user):
                                return user.id == message.author.id and reaction.message.id == mess.id

                            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                            if str(reaction.emoji) == "6️⃣":
                                    await mess.remove_reaction("6️⃣", message.author)
                                    await mess.remove_reaction("1️⃣", client.user)
                                    await mess.remove_reaction("2️⃣", client.user)
                                    await mess.remove_reaction("3️⃣", client.user)
                                    await mess.remove_reaction("4️⃣", client.user)
                                    await mess.remove_reaction("5️⃣", client.user)
                                    await mess.remove_reaction("6️⃣", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="SET TICKET CHANNEL", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="SET TICKET CHANNEL", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="SET TICKET CHANNEL", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break
                                    embed = discord.Embed(title="SET TICKET CHANNEL", description="In which Channel do you want to create Tickets?\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)

                                    def check(m):

                                                    return m.content is not None and m.author == message.author and  m.channel == message.channel



                                    while True:

                                        msg2 = await client.wait_for('message', check=check, timeout=120)
                                        if "no" in msg2.content.lower():
                                            embed = discord.Embed(title="SET TICKET CHANNEL", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        if len(msg2.channel_mentions) == 0:
                                            embed = discord.Embed(title="SET TICKET CHANNEL", description="You don´t ping the channel or the ping can´t found\nTry again", color=COLOR)
                                            await mess.edit(embed=embed)
                                        else:
                                                channel = msg2.channel_mentions[0]

                                                embed = discord.Embed(title=data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["topic"], description=data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["description"], color=COLOR)
                                                apply = await channel.send(embed=embed)

                                                await apply.add_reaction("🎟️")

                                                if data[str(message.guild.id)]["support"].get(str(channel.id)) is None:
                                                    data[str(message.guild.id)]["support"][str(channel.id)] = {}

                                                data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)] = data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]
                                                del data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]
                                                with open('data.json', 'w') as f:
                                                            json.dump(data, f)

                                                data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["startchannel"] = channel.id
                                                data[str(message.guild.id)]["support"][str(channel.id)][str(apply.id)]["startmessage"] = apply.id
                                                with open('data.json', 'w') as f:
                                                            json.dump(data, f)

                                                embed = discord.Embed(title="SET TICKET CHANNEL", description="Changed succesfully", color=COLOR)
                                                await mess.edit(embed=embed)
                                                return


                            if str(reaction.emoji) == "3️⃣":
                                await mess.remove_reaction("3️⃣", message.author)
                                await mess.remove_reaction("1️⃣", client.user)
                                await mess.remove_reaction("2️⃣", client.user)
                                await mess.remove_reaction("3️⃣", client.user)
                                await mess.remove_reaction("4️⃣", client.user)
                                await mess.remove_reaction("5️⃣", client.user)
                                await mess.remove_reaction("6️⃣", client.user)
                                embed = discord.Embed(title="EDIT TICKET CHANNEL NAME", description="\u200b", color=COLOR)
                                embed.add_field(name=':white_check_mark:', value="Set a new Ticket Channel Name", inline=False)
                                embed.add_field(name=':negative_squared_cross_mark:', value="Delete the Custom Ticket Channel Name", inline=False)
                                await mess.edit(embed=embed)
                                await mess.add_reaction("✅")
                                await mess.add_reaction("❎")
                                def check(reaction, user):
                                    return user.id == message.author.id and reaction.message.id == mess.id

                                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "✅":
                                    await mess.remove_reaction("✅", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="SET TICKET CHANNEL NAME", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="SET TICKET CHANNEL NAME", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="SET TICKET CHANNEL NAME", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    embed = discord.Embed(title="SET TICKET CHANNEL NAME", description="Which ticket name do you want?\nWrite Following things for Shortcuts: {count} = Ticket Number, {user} = User Name\nWrite **skip** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                        msg1 = await client.wait_for('message', check=check, timeout=120)
                                        if "skip" in msg1.content.lower():
                                            embed = discord.Embed(title="SET TICKET CHANNEL NAME", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        else:
                                            if len(msg1.content) < 30:
                                    
                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["ticket-name"] = str(msg1.content)
                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["counter"] = 0

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)

                                                    nam = data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["ticket-name"]

                                                    embed = discord.Embed(title="SET TICKET CHANNEL NAME", description=f"Ticket Name set to {nam}", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                            else:
                                                embed = discord.Embed(title="SET TICKET CHANNEL NAME", description="The Name is too long!\nWhich ticket name do you want?\nWrite **skip** to end this Setup", color=COLOR)
                                                await mess.edit(embed=embed)
                                                


                                if str(reaction.emoji) == "❎":
                                    await mess.remove_reaction("❎", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="DELETE TICKET CHANNEL NAME", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="DELETE TICKET CHANNEL NAME", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="DELETE TICKET CHANNEL NAME", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break


                                    while True:

                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["ticket-name"] = "ticket-{count}"

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)

                                                    nam = data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["ticket-name"]

                                                    embed = discord.Embed(title="DELETE TICKET CHANNEL NAME", description=f"Ticket Name resetted to {nam}", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return



                            if str(reaction.emoji) == "4️⃣":
                                await mess.remove_reaction("4️⃣", message.author)
                                await mess.remove_reaction("1️⃣", client.user)
                                await mess.remove_reaction("2️⃣", client.user)
                                await mess.remove_reaction("3️⃣", client.user)
                                await mess.remove_reaction("4️⃣", client.user)
                                await mess.remove_reaction("5️⃣", client.user)
                                await mess.remove_reaction("6️⃣", client.user)
                                embed = discord.Embed(title="EDIT TICKET MESSAGE", description="\u200b", color=COLOR)
                                embed.add_field(name=':white_check_mark:', value="Set a Ticket Message", inline=False)
                                embed.add_field(name=':negative_squared_cross_mark:', value="Delete the Ticket Message", inline=False)
                                await mess.edit(embed=embed)
                                await mess.add_reaction("✅")
                                await mess.add_reaction("❎")
                                def check(reaction, user):
                                    return user.id == message.author.id and reaction.message.id == mess.id

                                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "✅":
                                    await mess.remove_reaction("✅", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="SET TICKET MESSAGE", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="SET TICKET MESSAGE", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="SET TICKET MESSAGE", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    embed = discord.Embed(title="SET TICKET MESSAGE", description="Which ticket message do you want?\nWrite Following things for Shortcuts: {user} = User Mention\nWrite **skip** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                        msg1 = await client.wait_for('message', check=check, timeout=120)
                                        if "skip" == msg1.content.lower():
                                            embed = discord.Embed(title="SET TICKET MESSAGE", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        else:
                                            if len(msg1.content) < 1700:
                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["create-message"] = str(msg1.content)

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)


                                                    embed = discord.Embed(title="SET TICKET MESSAGE", description="Ticket Message setted", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                            else:
                                                embed = discord.Embed(title="SET TICKET MESSAGE", description="The Message is too long!\nWhich Ticket message do you want?\nWrite **skip** to end this Setup", color=COLOR)
                                                await mess.edit(embed=embed)
                                                


                                if str(reaction.emoji) == "❎":
                                    await mess.remove_reaction("❎", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="DELETE TICKET MESSAGE", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="DELETE TICKET MESSAGE", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="DELETE TICKET MESSAGE", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    while True:

                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["create-message"] = None

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)



                                                    embed = discord.Embed(title="DELETE TICKET MESSAGE", description=f"Ticket Message deleted", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return

                            if str(reaction.emoji) == "5️⃣":
                                await mess.remove_reaction("5️⃣", message.author)
                                await mess.remove_reaction("1️⃣", client.user)
                                await mess.remove_reaction("2️⃣", client.user)
                                await mess.remove_reaction("3️⃣", client.user)
                                await mess.remove_reaction("4️⃣", client.user)
                                await mess.remove_reaction("5️⃣", client.user)
                                await mess.remove_reaction("6️⃣", client.user)
                                embed = discord.Embed(title="EDIT TICKET CATEGORY", description="\u200b", color=COLOR)
                                embed.add_field(name=':white_check_mark:', value="Set the Ticket Category", inline=False)
                                embed.add_field(name=':negative_squared_cross_mark:', value="Delete the Ticket Category", inline=False)
                                await mess.edit(embed=embed)
                                await mess.add_reaction("✅")
                                await mess.add_reaction("❎")
                                def check(reaction, user):
                                    return user.id == message.author.id and reaction.message.id == mess.id

                                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "✅":
                                    await mess.remove_reaction("✅", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="SET TICKET CATEGORY", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="SET TICKET CATEGORY", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="SET TICKET CATEGORY", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    embed = discord.Embed(title="SET TICKET CATEGORY", description="Which ticket Category do you want?\nPlease write the Category ID!\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                        msg1 = await client.wait_for('message', check=check, timeout=120)
                                        if "no" in msg1.content.lower():
                                            embed = discord.Embed(title="SET TICKET CATEGORY", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        else:
                                            for i in message.guild.categories:
                                                if int(msg1.content) == i.id:
                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["category"] = int(msg1.content)

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)


                                                    embed = discord.Embed(title="SET TICKET CATEGORY", description="Ticket Category setted", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                            embed = discord.Embed(title="SET TICKET CATEGORY", description="Invalid Category ID\nWhich ticket Category do you want?\nPlease write the Category ID!\nWrite **no** to end this Setup", color=COLOR)
                                            await mess.edit(embed=embed)


                                                



                                if str(reaction.emoji) == "❎":
                                    await mess.remove_reaction("❎", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="DELETE TICKET CATEGORY", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="DELETE TICKET CATEGORY", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="DELETE TICKET CATEGORY", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    while True:

                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["category"] = None

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)



                                                    embed = discord.Embed(title="DELETE TICKET CATEGORY", description=f"Ticket Category deleted", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return

                            if str(reaction.emoji) == "1️⃣":
                                await mess.remove_reaction("1️⃣", message.author)
                                await mess.remove_reaction("1️⃣", client.user)
                                await mess.remove_reaction("2️⃣", client.user)
                                await mess.remove_reaction("3️⃣", client.user)
                                await mess.remove_reaction("4️⃣", client.user)
                                await mess.remove_reaction("5️⃣", client.user)
                                await mess.remove_reaction("6️⃣", client.user)
                                embed = discord.Embed(title="EDIT TICKET ROLE", description="\u200b", color=COLOR)
                                embed.add_field(name=':white_check_mark:', value="Set a Ticket Role", inline=False)
                                embed.add_field(name=':negative_squared_cross_mark:', value="Delete a Ticket Role", inline=False)
                                await mess.edit(embed=embed)
                                await mess.add_reaction("✅")
                                await mess.add_reaction("❎")
                                def check(reaction, user):
                                    return user.id == message.author.id and reaction.message.id == mess.id

                                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "✅":
                                    await mess.remove_reaction("✅", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="SET TICKET ROLE", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="SET TICKET ROLE", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="SET TICKET ROLE", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    embed = discord.Embed(title="SET TICKET ROLE", description="Which role should have access to the ticket system?\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                        msg1 = await client.wait_for('message', check=check, timeout=120)
                                        if "no" in msg1.content.lower():
                                            embed = discord.Embed(title="SET TICKET ROLE", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        else:
                                            if len(msg1.role_mentions) == 0:
                                                embed = discord.Embed(title="SET TICKET ROLE", description="You don´t ping the role or the ping can´t found\nWhich role should have access to the ticket system?\nWrite **no** to end this Setup", color=COLOR)
                                                await mess.edit(embed=embed)

                                            else:
                                                role = msg1.role_mentions[0]

                                                if role.id not in data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["supportrole"]:

                                                    data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["supportrole"].append(role.id)

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)
                                        
                                                    embed = discord.Embed(title="SET TICKET ROLE", description="Role was set successfully\nWhich role should have access to the ticket system?\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)

                                                else:
                                                    embed = discord.Embed(title="SET TICKET ROLE", description="This role is already set\nWhich role should have access to the ticket system?\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)


                                if str(reaction.emoji) == "❎":
                                    await mess.remove_reaction("❎", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="DELETE TICKET ROLE", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="DELETE TICKET ROLE", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="DELETE TICKET ROLE", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    embed = discord.Embed(title="DELETE TICKET ROLE", description="Which Role do you want to remove out of your Ticket System?\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                        msg1 = await client.wait_for('message', check=check, timeout=120)
                                        if "no" in msg1.content.lower():
                                            embed = discord.Embed(title="DELETE TICKET ROLE", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        else:
                                            if len(msg1.role_mentions) == 0:
                                                embed = discord.Embed(title="DELETE TICKET ROLE", description="You don´t ping the role or the ping can´t found\nWhich Role do you want to remove out of your Ticket System?\nWrite **no** to end this Setup", color=COLOR)
                                                await mess.edit(embed=embed)

                                            else:
                                                role = msg1.role_mentions[0]

                                                if role.id in data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["supportrole"]:

                                            
                                                    index = data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["supportrole"].index(role.id)
                                                    del data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["supportrole"][index]

                                                    with open('data.json', 'w') as f:
                                                        json.dump(data, f)
                                        
                                                    embed = discord.Embed(title="DELETE TICKET ROLE", description="Role was successfully removed\nWhich Role do you want to remove out of your Ticket System?\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)

                                                else:
                                                    embed = discord.Embed(title="DELETE TICKET ROLE", description="This role is not set\nWhich Role do you want to remove out of your Ticket System?\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)



                            if str(reaction.emoji) == "2️⃣":
                                await mess.remove_reaction("2️⃣", message.author)
                                embed = discord.Embed(title="EDIT TICKET THEMES", description="\u200b", color=COLOR)
                                embed.add_field(name=':one:', value="Edit the Ticket Description", inline=False)
                                embed.add_field(name=':two:', value="Edit the Ticket Topic", inline=False)
                                await mess.edit(embed=embed)
                                await mess.remove_reaction("3️⃣", client.user)
                                await mess.remove_reaction("4️⃣", client.user)
                                await mess.remove_reaction("5️⃣", client.user)
                                await mess.remove_reaction("6️⃣", client.user)
                                def check(reaction, user):
                                    return user.id == message.author.id and reaction.message.id == mess.id

                                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "1️⃣":
                                    await mess.remove_reaction("1️⃣", message.author)
                                    await mess.remove_reaction("1️⃣", client.user)
                                    await mess.remove_reaction("2️⃣", client.user)

                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="EDIT TICKET DESCRIPTION", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="EDIT TICKET DESCRIPTION", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="EDIT TICKET DESCRIPTION", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    embed = discord.Embed(title="EDIT TICKET DESCRIPTION", description="Which new Description do you want?\nWrite **skip** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                        msg1 = await client.wait_for('message', check=check, timeout=120)
                                        if "skip" == msg1.content.lower():
                                            embed = discord.Embed(title="EDIT TICKET DESCRIPTION", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        else:
                                            if len(msg1.content) < 2048:
                                                data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["description"] = str(msg1.content)
                                                with open('data.json', 'w') as f:
                                                            json.dump(data, f)

                                                channel = client.get_channel(data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["startchannel"])
                                                ms = await channel.fetch_message(data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["startmessage"])

                                                embed = discord.Embed(title=data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["topic"], description=data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["description"], color=COLOR)
                                                
                                                if msg1.attachments:
                                                    if msg1.attachments[0].filename.split(".")[-1].lower() in ["png", "jpg", "jpeg", "gif", "bpm"]:
                                                            file = await msg1.attachments[0].to_file()
                                                            embed.set_image(url="attachment://" + file.filename)
                                                            await ms.edit(file=file, embed=embed)
                                                    else:
                                                        await ms.edit(embed=embed)
                                                else:
                                                
                                                    await ms.edit(embed=embed)

                                                embed = discord.Embed(title="EDIT TICKET DESCRIPTION", description="Edited Successfully", color=COLOR)
                                                await mess.edit(embed=embed)
                                                return
                                            else:
                                                embed = discord.Embed(title="EDIT TICKET DESCRIPTION", description="The new Description is too long!\nWhich new Description do you want?\nWrite **skip** to end this Setup", color=COLOR)
                                                await mess.edit(embed=embed)
                                            


                                if str(reaction.emoji) == "2️⃣":
                                    await mess.remove_reaction("2️⃣", message.author)
                                    await mess.remove_reaction("1️⃣", client.user)
                                    await mess.remove_reaction("2️⃣", client.user)
                                    def check(m):
                                        return m.content is not None and m.author == message.author and  m.channel == message.channel

                                    embed = discord.Embed(title="EDIT TICKET TOPIC", description="Which Ticket System do you want to edit?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="EDIT TICKET TOPIC", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                    embed = discord.Embed(title="EDIT TICKET TOPIC", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                    embed = discord.Embed(title="EDIT TICKET TOPIC", description="Which new Topic do you want?\nWrite **skip** to end this Setup", color=COLOR)
                                    await mess.edit(embed=embed)
                                    while True:
                                        msg1 = await client.wait_for('message', check=check, timeout=120)
                                        if "skip" == msg1.content.lower():
                                            embed = discord.Embed(title="EDIT TICKET TOPIC", description="Stopped the Setup", color=COLOR)
                                            await mess.edit(embed=embed)
                                            return
                                        else:
                                            if len(msg1.content) < 256:
                                                data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["topic"] = str(msg1.content)
                                                with open('data.json', 'w') as f:
                                                            json.dump(data, f)


                                                channel = client.get_channel(data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["startchannel"])
                                                ms = await channel.fetch_message(data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["startmessage"])

                                                embed = discord.Embed(title=data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["topic"], description=data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]["description"], color=COLOR)
                                                

                                                if msg1.attachments:
                                                    if msg1.attachments[0].filename.split(".")[-1].lower() in ["png", "jpg", "jpeg", "gif", "bpm"]:
                                                            file = await msg1.attachments[0].to_file()
                                                            embed.set_image(url="attachment://" + file.filename)
                                                            await ms.edit(file=file, embed=embed)
                                                    else:
                                                        await ms.edit(embed=embed)
                                                else:
                                                    await ms.edit(embed=embed)


                                                embed = discord.Embed(title="EDIT TICKET TOPIC", description="Edited Successfully", color=COLOR)
                                                await mess.edit(embed=embed)
                                                return
                                            else:
                                                embed = discord.Embed(title="EDIT TICKET TOPIC", description="The new Topic is too long!\nWhich new Topic do you want?\nWrite **skip** to end this Setup", color=COLOR)
                                                await mess.edit(embed=embed)
                                            



                        if str(reaction.emoji) == "3️⃣":
                                await mess.remove_reaction("3️⃣", message.author)
                                await mess.remove_reaction("1️⃣", client.user)
                                await mess.remove_reaction("2️⃣", client.user)
                                await mess.remove_reaction("3️⃣", client.user)
                                def check(m):
                                                return m.content is not None and m.author == message.author and  m.channel == message.channel


                                embed = discord.Embed(title="DELETE TICKET", description="Which Ticket System do you want to delete?(Please send the Channel where the Tickets created at the moment)\nWrite **no** to end this Setup", color=COLOR)
                                await mess.edit(embed=embed)
                                while True:
                                                msg = await client.wait_for('message', check=check, timeout=120)
                                                if "no" in msg.content.lower():
                                                    embed = discord.Embed(title="DELETE TICKET", description="Stopped the Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                    return
                                                if len(msg.channel_mentions) == 0:
                                                    embed = discord.Embed(title="DELETE TICKET", description="This is an Invalid Channel.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)

                                                chan = msg.channel_mentions[0]

                                                if data[str(message.guild.id)]["support"].get(str(chan.id)) is None:
                                                    embed = discord.Embed(title="DELETE TICKET", description="This is an Invalid Channel.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                    await mess.edit(embed=embed)
                                                else:

                                                    break

                                embed = discord.Embed(title="DELETE TICKET", description="Which Ticket System do you want to delete?(Please send the Message ID)\nWrite **no** to end this Setup", color=COLOR)
                                await mess.edit(embed=embed)
                                while True:
                                            msg = await client.wait_for('message', check=check, timeout=120)
                                            if "no" in msg.content.lower():
                                                embed = discord.Embed(title="DELETE TICKET", description="Stopped the Setup", color=COLOR)
                                                await mess.edit(embed=embed)
                                                return
                                            if data[str(message.guild.id)]["support"][str(chan.id)].get(str(msg.content)) is None:
                                                embed = discord.Embed(title="DELETE TICKET", description="This is an Invalid ID.\nPlease Try again!\nWrite **no** to end this Setup", color=COLOR)
                                                await mess.edit(embed=embed)
                                            else:
                                                break

                                def check(reaction, user):
                                    return user.id == message.author.id and reaction.message.id == mess.id
                                embed = discord.Embed(title="DELETE TICKET", description="Are you sure, that you want to delete the Ticket System?", color=COLOR)
                                await mess.edit(embed=embed)
                                await mess.add_reaction("✅")
                                await mess.add_reaction("❎")
                                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "✅":
                                    await mess.remove_reaction("✅", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)

                                    del data[str(message.guild.id)]["support"][str(chan.id)][str(msg.content)]


                                    with open('data.json', 'w') as f:
                                               json.dump(data, f)


                                    embed = discord.Embed(title="DELETE TICKET", description="Ticket System deleted successfully", color=COLOR)
                                    await mess.edit(embed=embed)
                                    return
                                    
                                if str(reaction.emoji) == "❎":
                                    await mess.remove_reaction("❎", message.author)
                                    await mess.remove_reaction("✅", client.user)
                                    await mess.remove_reaction("❎", client.user)
                                    embed = discord.Embed(title="DELETE TICKET", description="Stopped the Process!", color=COLOR)
                                    await mess.edit(embed=embed)
                                    return
                            

                    except asyncio.TimeoutError:
                                embed = discord.Embed(title="Timeout", description="The Process have been stopped", color=COLOR)
                                await message.channel.send(embed=embed)

                                return
                else:
                    embed = discord.Embed(title="Permissions", description="You don´t have enough Permissions", color=COLOR)
                    await message.channel.send(embed=embed)




            if message.content.startswith(PREFIX + "setprefix"):
                if message.author.guild_permissions.administrator:
                            if len(message.content.split(" "))-1 > 1 or len(message.content.split(" "))-1 == 1:
                                pre = message.content.split(" ")[1]
                            else:
                                embed = discord.Embed(title="Prefix", description="You don´t send a new Prefix", color=COLOR)
                                await message.channel.send(embed=embed)
                                return                  

                            if len(pre) > 5:
                                embed = discord.Embed(title="Prefix", description="The Prefix is too long! (Max. 5 characters)", color=COLOR)
                                await message.channel.send(embed=embed)
                            else:
                                data[str(message.guild.id)]["prefix"] = str(pre)
                                with open('data.json', 'w') as f:
                                    json.dump(data, f)


                                embed = discord.Embed(title="Successfully", description="New Prefix was set successfully", color=COLOR)
                                await message.channel.send(embed=embed)


                else:
                    embed = discord.Embed(title="Permissions", description="You don´t have enough Permissions", color=COLOR)
                    await message.channel.send(embed=embed)


    async def on_raw_reaction_add(self, payload):
        with open("data.json") as f:
            data = json.load(f)


        if client.get_guild(payload.guild_id) is not None:
         if data.get(str(payload.guild_id)) is not None:

            try:
                channel = client.get_channel(payload.channel_id)
                author = client.get_user(payload.user_id)
                message = await channel.fetch_message(payload.message_id)
                guild = client.get_guild(payload.guild_id)
            except:
                print("An error occured in fetching data in Raw Reaction add Event")
                return

            if not author.bot and not author == client.user:


               
                if str(payload.emoji) == "⚙️":
                    list = []
                    for key in data[str(guild.id)]["support"].keys():
                                    list.append(key)

                    for id1 in list:
                        list = []
                        for key in data[str(guild.id)]["support"][id1].keys():
                                        list.append(key)

                        for id in list:
                            if channel.id in data[str(guild.id)]["support"][id1][str(id)]["tickets"]:
                                if message.id == data[str(guild.id)]["support"][id1][str(id)]["opened"][str(channel.id)]:
                                        try:
                                            await message.remove_reaction("⚙️", author)
                                        except:
                                                    embed = discord.Embed(title="Error", description="An error occured on " + guild.name + "in Ticket System add/remove a user by removing Emoji", color=COLOR)
                                                    await channel.send(embed=embed)
                                                    return

                                        def check(m):
                                            return m.content is not None and m.author == author and  m.channel == channel
                                        try:
                                            embed = discord.Embed(title="Ticket", description="Please Ping the User or send the User ID to add/remove him to/from the Ticket", color=COLOR)
                                            await message.channel.send(embed=embed)
                                            msg = await client.wait_for('message', check=check, timeout=120)
                                            if msg.mentions:
                                                if isinstance(msg.mentions[0], discord.Member) or isinstance(msg.mentions[0], discord.User):
                                                    member = msg.mentions[0]
                                                else:
                                                    member = await client.fetch_user(msg.content)
                                            else:
                                                member = await client.fetch_user(msg.content)
                                            no = True
                                            for key in channel.overwrites:
                                                if key in guild.members:
                                                    if key.id == member.id:
                                                        no = False
                                            if no:
                                                perms = channel.overwrites_for(member)
                                                perms.send_messages=True
                                                perms.read_messages=True
                                                perms.add_reactions=True
                                                perms.embed_links=True
                                                perms.attach_files=True
                                                perms.read_message_history=True
                                                perms.external_emojis=True
                                                await channel.set_permissions(member, overwrite=perms)
                                                embed = discord.Embed(title="Ticket", description=f"Successfully added **{member.mention} | {member}** to the Ticket", color=COLOR)
                                                await channel.send(embed=embed)
                                            else:
                                                overwrite = channel.overwrites_for(member)
                                                if overwrite.send_messages == False or overwrite.read_messages == False:
                                                    perms = channel.overwrites_for(member)
                                                    perms.send_messages=True
                                                    perms.read_messages=True
                                                    perms.add_reactions=True
                                                    perms.embed_links=True
                                                    perms.attach_files=True
                                                    perms.read_message_history=True
                                                    perms.external_emojis=True
                                                    await channel.set_permissions(member, overwrite=perms)
                                                    embed = discord.Embed(title="Ticket", description=f"Successfully added **{member.mention} | {member}** to the Ticket", color=COLOR)
                                                    await channel.send(embed=embed)
                                                else:
                                                    perms = channel.overwrites_for(member)
                                                    perms.send_messages=False
                                                    perms.read_messages=False
                                                    perms.add_reactions=False
                                                    perms.embed_links=False
                                                    perms.attach_files=False
                                                    perms.read_message_history=False
                                                    perms.external_emojis=False
                                                    await channel.set_permissions(member, overwrite=perms)
                                                    embed = discord.Embed(title="Ticket", description=f"Successfully removed **{member.mention} | {member}** from the Ticket", color=COLOR)
                                                    await channel.send(embed=embed)


                                        except asyncio.TimeoutError:
                                                    embed = discord.Embed(title="Timeout",
                                                                          description="You run out of the time!\nThe Progress have been cancelled!",
                                                                          color=COLOR)
                                                    await channel.send(embed=embed)
                                                    return

                                        except:
                                                    embed = discord.Embed(title="Ticket", description="Mention or ID not Found", color=COLOR)
                                                    await channel.send(embed=embed)
                                                    return


                if str(payload.emoji) == "🔓":
                    list = []
                    for key in data[str(guild.id)]["support"].keys():
                                    list.append(key)

                    for id1 in list:
                        list = []
                        for key in data[str(guild.id)]["support"][id1].keys():
                                        list.append(key)

                        for id in list:
                            if channel.id in data[str(guild.id)]["support"][id1][str(id)]["tickets"]:
                                if message.id == data[str(guild.id)]["support"][id1][str(id)]["closed"][str(channel.id)]:
                                    try:
                                        await message.remove_reaction("🔓", author)
                                    except:
                                                embed = discord.Embed(title="Error", description="An error occured on " + guild.name + "in Tickt System reopen ticket by removing a Emoji", color=COLOR)
                                                await channel.send(embed=embed)
                                                return
                                    ow = data[str(guild.id)]["support"][id1][str(id)]["owners"][str(channel.id)]
                                    owner = await client.fetch_user(ow)
                                    overwrites = {
                                                guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=False, external_emojis=False),
                                                owner: discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                                                }
                                    if data[str(guild.id)]["support"][id1][str(id)]["supportrole"] != []:
                                                pinged_msg_content = ""
                                                for role_id in data[str(guild.id)]["support"][id1][str(id)]["supportrole"]:
                                                    role = guild.get_role(role_id)
                                                    overwrites[role] = discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                                    await channel.edit(overwrites=overwrites)
                                    with open("data.json") as f:
                                        data = json.load(f)
                                    data[str(guild.id)]["support"][id1][str(id)]["closed"][str(channel.id)] = None
                                    with open('data.json', 'w') as f:
                                        json.dump(data, f)
                                    embed = discord.Embed(title="Reopen", description=f"Ticket has Reopened by {author.mention}", color=COLOR)
                                    await channel.send(embed=embed)


                if str(payload.emoji) == "🔒":
                    list = []
                    for key in data[str(guild.id)]["support"].keys():
                                    list.append(key)

                    for id1 in list:
                        list = []
                        for key in data[str(guild.id)]["support"][id1].keys():
                                        list.append(key)

                        for id in list:
                            if channel.id in data[str(guild.id)]["support"][id1][str(id)]["tickets"]:
                                if message.id == data[str(guild.id)]["support"][id1][str(id)]["opened"][str(channel.id)]:
                                        try:
                                            await message.remove_reaction("🔒", author)
                                        except:
                                                    embed = discord.Embed(title="Error", description="An error occured on " + guild.name + "in Ticket System close Ticket by removing Emoji", color=COLOR)
                                                    await channel.send(embed=embed)
                                                    return

                                        try:
                                            await message.add_reaction("✅")
                                            await message.add_reaction("❎")
                                        except:
                                            return

                                        def check(payload):
                                                                    return (payload.message_id == message.id and payload.user_id == author.id)
                                        try:
                                                        payload = await client.wait_for("raw_reaction_add", check=check, timeout=30)
                                                        if str(payload.emoji) == "❎":
                                                            await message.remove_reaction("❎", author)
                                                            await message.remove_reaction("❎", client.user)
                                                            await message.remove_reaction("✅", client.user)




                                                        if str(payload.emoji) == "✅":
                                                            await message.remove_reaction("✅", author)
                                                            await message.remove_reaction("❎", client.user)
                                                            await message.remove_reaction("✅", client.user)
                                                            overwrites = {
                                                                    guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=False, external_emojis=False),
                                                                }
                                                            if data[str(guild.id)]["support"][id1][str(id)]["supportrole"] != []:
                                                                    pinged_msg_content = ""
                                                                    for role_id in data[str(guild.id)]["support"][id1][str(id)]["supportrole"]:
                                                                        role = guild.get_role(role_id)
                                                                        overwrites[role] = discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                                                            await channel.edit(overwrites=overwrites)
                                                            embed = discord.Embed(title="Closed", description=f"Ticket has closed by {author.mention}", color=COLOR)
                                                            await channel.send(embed=embed)
                                                            embed = discord.Embed(title="Closed", description="🗑️=Delete Ticket\n🔓=Reopen Ticket", color=COLOR)
                                                            mes = await channel.send(embed=embed)
                                                            with open("data.json") as f:
                                                                data = json.load(f)
                                                            data[str(guild.id)]["support"][id1][str(id)]["closed"][str(channel.id)] = mes.id
                                                            with open('data.json', 'w') as f:
                                                                            json.dump(data, f)
                                                            await mes.add_reaction("🗑️")
                                                            await mes.add_reaction("🔓")
                                        except asyncio.TimeoutError:
                                                await message.remove_reaction("❎", client.user)
                                                await message.remove_reaction("✅", client.user)
                                                embed = discord.Embed(title="Timeout",
                                                                      description="You run out of the time!\nThe Progress have been cancelled!",
                                                                      color=COLOR)
                                                await message.channel.send(embed=embed)
                                                return


 
                if str(payload.emoji) == "🗑️":
                    list = []
                    for key in data[str(guild.id)]["support"].keys():
                                    list.append(key)

                    for id1 in list:
                        list = []
                        for key in data[str(guild.id)]["support"][id1].keys():
                                        list.append(key)

                        for id in list:
                            if channel.id in data[str(guild.id)]["support"][id1][str(id)]["tickets"]:
                                if message.id == data[str(guild.id)]["support"][id1][str(id)]["closed"][str(channel.id)]:
                                        try:
                                            await message.remove_reaction("🗑️", author)
                                        except:
                                                    embed = discord.Embed(title="Error", description="An error occured on " + guild.name + "in Ticket System Delete Ticket by removing a Emoji", color=COLOR)
                                                    await channel.send(embed=embed)
                                                    return

                                        try:
                                            await message.add_reaction("✅")
                                            await message.add_reaction("❎")
                                        except:
                                            return

                                        def check(payload):
                                                                    return (payload.message_id == message.id and payload.user_id == author.id)
                                        try:
                                                        payload = await client.wait_for("raw_reaction_add", check=check, timeout=30)
                                                        if str(payload.emoji) == "❎":
                                                            await message.remove_reaction("❎", author)
                                                            await message.remove_reaction("❎", client.user)
                                                            await message.remove_reaction("✅", client.user)
                                                           



                                                        if str(payload.emoji) == "✅":
                                                            await message.remove_reaction("✅", author)
                                                            await message.remove_reaction("❎", client.user)
                                                            await message.remove_reaction("✅", client.user)

                                                            with open("data.json") as f:
                                                                data = json.load(f)
                                                            index = data[str(guild.id)]["support"][id1][str(id)]["tickets"].index(channel.id)
                                                            del data[str(guild.id)]["support"][id1][str(id)]["tickets"][index]
                                                            del data[str(guild.id)]["support"][id1][str(id)]["owners"][str(channel.id)]
                                                            del data[str(guild.id)]["support"][id1][str(id)]["closed"][str(channel.id)]
                                                            del data[str(guild.id)]["support"][id1][str(id)]["opened"][str(channel.id)]

                                                            with open('data.json', 'w') as f:
                                                                    json.dump(data, f)
                                
                                                            embed = discord.Embed(title="Close",
                                                                                  description="The ticket will be closed in 5 seconds ...",
                                                                                  color=COLOR)
                                                            await channel.send(embed=embed)
                                                            await asyncio.sleep(5)

                                                            await channel.delete()


                                        except asyncio.TimeoutError:
                                            await message.remove_reaction("❎", client.user)
                                            await message.remove_reaction("✅", client.user)
                                            embed = discord.Embed(title="Timeout",
                                                                  description="You run out of the time!\nThe Progress have been cancelled!",
                                                                  color=COLOR)
                                            await message.channel.send(embed=embed)


                if str(payload.emoji) == "🎟️":
                    if data[str(guild.id)]["support"].get(str(channel.id)) is None:
                            pass
                    else:
                        if data[str(guild.id)]["support"][str(channel.id)].get(str(payload.message_id)) is not None:
                                try:
                                    await message.remove_reaction("🎟️", author)
                                except:
                                        print("An error occured on " + guild.name + "in Ticket System create Ticket by removing a Emoji")
                                        return
                            
                                allowed = False
                                tim = datetime.datetime.utcnow()
                                time_change = datetime.timedelta(seconds=10)
                                end = tim + time_change
                                if data[str(guild.id)]["cooldowns"]["ticket"].get(str(author.id)) is None:
                                    allowed = True
                                    data[str(guild.id)]["cooldowns"]["ticket"][str(author.id)] = str(end)
                                    with open('data.json', 'w') as f:
                                        json.dump(data, f)
                                else:
                                    old = data[str(guild.id)]["cooldowns"]["ticket"][str(author.id)]
                                    if old < str(tim) or old == str(tim):
                                        allowed = True
                                        data[str(guild.id)]["cooldowns"]["ticket"][str(author.id)] = str(end)
                                        with open('data.json', 'w') as f:
                                            json.dump(data, f)
                                if allowed:
                                    
                                        with open("data.json") as f:
                                            data = json.load(f)
                                        ticket_number = int(data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["counter"])
                                        ticket_number += 1
                                        data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["counter"] = int(ticket_number)
                                        with open('data.json', 'w') as f:
                                                    json.dump(data, f)
                                        if data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["category"] is None:
                                            cat = channel.category_id
                                        else:
                                            tt = False
                                            cate = data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["category"]
                                            for i in message.guild.categories:
                                                if cate == i.id:
                                                    cat = data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["category"]
                                                    tt = True
                                                    break
                                            if not tt:
                                                with open("data.json") as f:
                                                    data = json.load(f)
                                                data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["category"] = None
                                                with open('data.json', 'w') as f:
                                                    json.dump(data, f)
                                                cat = channel.category_id


                                        category = discord.utils.get(message.guild.categories, id=cat)
                                        overwrites = {
                                            guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=False, external_emojis=False),
                                            author: discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                                        }
                                        if data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["supportrole"] != []:
                                            for role_id in data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["supportrole"]:
                                                role = guild.get_role(role_id)
                                                overwrites[role] = discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                                        
                                        nam = data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["ticket-name"]
                                        numb = str(data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["counter"])

                                        
                                        ticket_channel = await message.guild.create_text_channel(nam.replace("{user}", author.name).replace("{count}", numb), category=category, overwrites=overwrites)


                                        if data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["create-message"] is None:
                                            top = data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["topic"]
                                            mesi = f"**Topic:** {top}"
                                        else:
                                            mesi = data[str(message.guild.id)]["support"][str(channel.id)][str(message.id)]["create-message"]

                                        pinged_msg_content = f"{author.mention}\n"
                                        if data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["supportrole"] != []:
                                            for role_id in data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["supportrole"]:
                                                    role = guild.get_role(role_id)
                                                    pinged_msg_content += role.mention

                                        embed = discord.Embed(title=f"Ticket from {author}",
                                                           description=mesi.replace("{user}", author.mention), color=COLOR)
                                        if pinged_msg_content == "":
                                            mes = await ticket_channel.send(embed=embed)
                                        else:
                                            mes = await ticket_channel.send(pinged_msg_content, embed=embed)
                                        await mes.add_reaction("🔒")
                                        await mes.add_reaction("⚙️")

                                        

                                        await mes.pin()
                                        with open("data.json") as f:
                                            data = json.load(f)
                                        data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["tickets"].append(ticket_channel.id)
                                        data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["owners"][str(ticket_channel.id)] = int(author.id)
                                        data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["closed"][str(ticket_channel.id)] = None
                                        data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["opened"][str(ticket_channel.id)] = mes.id
                                        with open('data.json', 'w') as f:
                                                    json.dump(data, f)

                                        try:
                                            top = data[str(guild.id)]["support"][str(channel.id)][str(message.id)]["topic"]
                                            embed = discord.Embed(title="Ticket", description=f"Your Ticket on **{guild.name}** has been created: \n{ticket_channel.mention}\n**Topic:** {top}", color=COLOR)
                                            await author.send(embed=embed)
                                        except:
                                            pass



                    
                    
                    


client = MyClient(intents=discord.Intents.all(), cache=discord.MemberCacheFlags.all())

client.loop.create_task(status())

client.run(config["TOKEN"])
