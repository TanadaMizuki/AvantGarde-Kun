import discord
from discord.ext import commands
import os
from os.path import join, dirname
from dotenv import load_dotenv
from os import listdir
import shutil
import traceback

#.envファイルの呼び出し処理
#.envにはDiscordとMisskeyのトークンが入っています
load_dotenv()

dotenv_path = join(dirname(__file__), '.env') #dirname(__file__)でカレントフォルダを指定
load_dotenv(dotenv_path)

#Discord botの要件定義
token = os.environ['DISCORD_BOT_TOKEN'] #load_dotenv()で取得した.env内の定数を取得
bot = commands.Bot(
    command_prefix='/', #コマンドのprefixを指定 '/'の場合、ユーザは'/form'と入力する
    case_insensitive=True,
    activity=discord.Activity(
        name='アバンギャルド君、起動します', type=discord.ActivityType.playing), #nameはプレイしているゲームの欄に表示する文字列を指定
    intents=discord.Intents.all(),
)

#bot起動処理
@bot.event
async def on_ready():
    #モジュールの読み込み
    #cogsフォルダ内を探索
    directories = filter(lambda x: os.path.isdir(os.path.join("cogs", x)), os.listdir("cogs"))
    for directory in directories:
        for file in os.listdir(os.path.join("cogs", directory)):
            #名前が.pyで終わるファイルをモジュールと見なして読み込み
            if file.endswith(".py"):
                try:
                    cogpath = f"cogs.{directory}.{file[:-3]}"
                    await bot.load_extension(cogpath)
                    print("Cog loaded:", cogpath)
                #読み込み失敗時のエラー処理
                except:
                    traceback.print_exc

    await bot.load_extension('jishaku')

    #所属するDiscordのサーバIDを指定
    #デフォルトでは怪文書図書館が指定されています
    bot.guild = bot.get_guild(1096798894932889641)
    bot.lib_guild = bot.get_guild(1096798894932889641)

    #Misskeyのアクセストークンを指定
    bot.mktoken = os.environ['MISSKEY_TOKEN']
    bot.mkbase_url = 'https://misskety.io/api/'

    #botの起動処理が正常に終了したら、コンソールにReadyと出力する
    print('Ready')

#エラー処理
@bot.event
async def on_command_error(ctx, error):
    error_ch = bot.get_channel(1110268182729592973)
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(
        traceback.TracebackException.from_exception(orig_error).format())
    embed = discord.Embed(title="✖ Error!", description='エラーが発生しました',
                          timestamp=ctx.message.created_at, color=discord.Colour.red())
    embed.add_field(
        name='メッセージID', value=f'お問い合わせの際にはこちらのidもお持ちください:\n`{ctx.message.id}`')
    embed.add_field(name='エラー内容', value=error, inline=False)
    embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
    await ctx.send(embed=embed)
    embed2 = discord.Embed(title='エラー情報', description='',
                           timestamp=ctx.message.created_at, color=discord.Colour.red())
    embed2.add_field(
        name='チャンネル', value=ctx.message.channel.name, inline=False)
    embed2.add_field(name='コマンド', value=ctx.message.content, inline=False)
    embed2.add_field(name='実行ユーザー名', value=ctx.author, inline=False)
    embed2.add_field(name='id', value=ctx.message.id, inline=False)
    embed2.add_field(name='内容', value=error, inline=False)
    await error_ch.send(embed=embed2)


#botの動作を開始
bot.run(token)