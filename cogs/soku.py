import discord
from discord.ext import commands
from config.sokuhostconfig import hosts
from config.hamachiconfig import rooms
from time import gmtime, strftime
import asyncio


class Soku:
    def __init__(self, bot):
        self.bot = bot
        self.hostlist = {}
        self.emoji_soku = discord.utils.get(bot.get_guild(241271400869003265).emojis, name="soku")

    async def on_message(self, ctx):
        if ctx.content.startswith("谢指教"):
            await ctx.channel.send("<@{}>谢你个头".format(ctx.author.id))

    @commands.command()
    async def addhost(self, ctx, *args):
        if args:
            ip = args[0]
            hamachi = False
            room = ""
            if len(args) == 3:
                if args[1] == "hamachi":
                    hamachi = True
                    room = args[2]
            if await self.valid_ip(ip):
                hosts[ctx.author.id] = {
                    "IP": ip,
                    "hamachi": hamachi,
                    "roomID": room}
                f = open("./config/sokuhostconfig.py", "w")
                f.write("hosts = " + repr(hosts))
                f.close()
                await ctx.channel.send("Host IP has been added.")
                await ctx.message.add_reaction(self.emoji_soku)
                if not hamachi:
                    await ctx.channel.send("Add `hamachi [hamachi room name]` to indicate you are using hamachi.")
            else:
                await ctx.channel.send("Invalid IP format")
                await ctx.channel.send("Example: {}".format(hosts["example"]["IP"]))

    @commands.command()
    async def valid_ip(self, ip):
        if ip.count(":") != 1 or ip.count(".") != 3:
            return False
        return True

    @commands.command()
    async def host(self, ctx, *args):
        txt = ""
        if args:
            for arg in args:
                txt += arg + " "
            txt = ":speaking_head: `{}`".format(txt)

        if ctx.author.id in hosts:
            text = "`{}` hosting at `{}` {}".format(ctx.author.name, hosts[ctx.author.id]["IP"], txt)
            if hosts[ctx.author.id]["hamachi"]:
                text += "\n with hamachi ID: `{}` PW: `{}`".format(hosts[ctx.author.id]["roomID"],
                                                                   rooms[hosts[ctx.author.id]["roomID"]])
            self.hostlist[ctx.author] = await ctx.channel.send(text)
            await ctx.message.add_reaction(self.emoji_soku)
        else:
            await ctx.channel.send("Unknown host!")
            await ctx.channel.send("Please record your IP using !?addhost first.")

    @commands.command()
    async def endhost(self, ctx):
        if ctx.author in self.hostlist:
            await self.hostlist[ctx.author].edit(content="{} has ended hosting.".format(ctx.author.name))
            self.hostlist.pop(ctx.author)
        await ctx.message.add_reaction(self.emoji_soku)

    @commands.command()
    async def addhamachi(self, ctx, roomid, pw):
        rooms[roomid] = pw
        await ctx.channel.send("Hamachi room information has been added.")
        f = open("./config/hamachiconfig.py", "w")
        f.write("rooms = " + repr(rooms))
        f.close()

    @commands.command()
    async def showhost(self, ctx):
        for current_host in self.hostlist.keys():
            text = "`{}` hosting at `{}`".format(current_host.name, hosts[current_host.id]["IP"])
            if hosts[current_host.id]["hamachi"]:
                text += "\n with hamachi ID: `{}` PW: `{}`".format(hosts[current_host.id]["roomID"],
                                                                   rooms[hosts[current_host.id]["roomID"]])
            await ctx.channel.send(text)
        await ctx.message.add_reaction(self.emoji_soku)

    @commands.command()
    async def givemesoku(self, ctx):
        await ctx.channel.send("Here you are:\nhttps://mega.nz/#!ccJhWTYA!pOezX4yFenh5o1_k55KCSF34fXv8EdkvLHu97m-kXZ4")
        await ctx.message.add_reaction(self.emoji_soku)

    @commands.command()
    async def glossary(self, ctx):
        await ctx.channel.send("https://hisouten.koumakan.jp/wiki/Glossary")
        await ctx.message.add_reaction(self.emoji_soku)

    @commands.command()
    async def soku(self, ctx):
        mentions = ""
        for id in hosts:
            if id != "example":
                mentions += "<@{}>".format(id)
        await ctx.channel.send(
            mentions + "\n" + str(self.emoji_soku) + " " + str(self.emoji_soku) + " " + str(
                self.emoji_soku) + "\n" + str(self.emoji_soku) + " :red_car: " + str(self.emoji_soku) + "\n" + str(
                self.emoji_soku) + " " + str(self.emoji_soku) + " " + str(self.emoji_soku))

    async def clean_hosts(self):
        await self.bot.wait_until_ready
        while not self.bot.is_closed():
            if strftime("%H:%M", gmtime()) == "05:00":
                for author in self.hostlist:
                    await self.hostlist[author].edit(content="{} has ended hosting.".format(author.name))
                self.hostlist = {}
                await asyncio.sleep(86400)
            else:
                await asyncio.sleep(59)


def setup(bot):
    bot.add_cog(Soku(bot))
