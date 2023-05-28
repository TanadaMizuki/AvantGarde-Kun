from datetime import datetime
import aiohttp
import discord
from discord.ext import commands, tasks


class timesignal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timesignal.start()
        self.message = None
        self.embed = None
    
    

    @tasks.loop(minutes=1)
    async def timesignal(self):
        now = datetime.now().strftime('%H')
        if now == '04' or now == '14' or now == '16' or now == '18' or now == '03':
            if datetime.now().strftime('%M') == '00':
                self.embed = discord.Embed(title='時報', colour=discord.Colour(0x128bfb), description=f'{now}時ぐらいをお知らせします')

                self.embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/733707711228674102/986178408696393768/spin.gif')

                if now =='04':
                    name = '日付更新'
                    value = '昨日のデイリーはちゃんと回収し終わったかしら?'
                    self.embed.add_field(name = name,value=value)
                elif now == '14':
                    name = '戦術対抗戦報酬受け取り権更新'
                    value = '忘れずに回収することね'
                    self.embed.add_field(name = name,value=value)
                elif now == '16':
                    name = 'カフェ更新'
                    value = ':left_side_balloon_with_tail:💦:right_side_balloon_without_tail:'
                    self.embed.add_field(name = name,value='💦')
                elif now == '18':
                    name = 'デイリーAP受け取り'
                    value = '今日もあと少しね'
                    self.embed.add_field(name = name,value=value)
                elif now == '03':
                    name = '日付更新1時間前'
                    value = 'デイリーは回収したかしら?'
                    self.embed.add_field(name = name,value=value)
                async with aiohttp.ClientSession() as session:
                    async with session.post(('https://misskey.io/api/notes/create'), headers={'Content-Type': 'application/json'},json={'i': self.bot.mktoken, 'text': f'{now}時くらいをお知らせします\n\n**{name}**\n{value}', 'channelId': '9c0i1s4abg'}) as resp:
                        print(resp.status)
                        print(await resp.text())
                print(f'時報({now}時)')

            if self.embed != None:
                if self.message != None:
                    await self.message.delete()
                self.message = await self.bot.guild.get_channel(1110268182729592973).send(embed=self.embed)
                self.embed = None

    async def cog_unload(self):
            self.timesignal.stop()


async def setup(bot):
    await bot.add_cog(timesignal(bot))
