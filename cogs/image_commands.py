from discord.ext import commands
import discord
import function_helper
import random

wrong_channel_text='The command you sent is not authorized for use in this channel.'
welcome_footer='HusekrBot welcomes you!'
huskerbot_footer="Generated by HuskerBot"

# Reference - https://www.cougcenter.com/2013/6/28/4445944/common-ncaa-football-penalties-referee-signals
ref_dict = {'bs': ['Bull shit', 'Referee still gets paid for that horrible call','https://i.imgur.com/0nQGIZs.gif'],
            'chip': ['Blocking below the waist', 'OFF: 15 yards\nDEF: 15 yards and an automatic first down', 'https://i.imgur.com/46aDB8t.gif'],
            'chop': ['Blocking below the waist', 'OFF: 15 yards\nDEF: 15 yards and an automatic first down', 'https://i.imgur.com/cuiRu7T.gif'],
            'encroachment': ['Encroachment', 'DEF: 5 yards', 'https://i.imgur.com/4ekGPs4.gif'],
            'facemask': ['Face mask', 'OFF: Personal foul, 15 yards\nDEF: Personal foul, 15 yards from the end spot of the play, automatic first down', 'https://i.imgur.com/xzsJ8MB.gif'],
            'falsestart': ['False start', 'OFF: 5 yards', 'https://i.imgur.com/i9ZyMpn.gif'],
            'hand2face': ['Hands to the face', 'OFF: Personal foul, 15 yards\nDEF: Personal foul, 15 yards, automatic first down', 'https://i.imgur.com/DNw5Qsq.gif'],
            'hold': ['Holding', 'OFF: 10 yards from the line of scrimmage and replay the down.\nDEF: 10 yards', 'https://i.imgur.com/iPUNHJi.gif'],
            'illfwd': ['Illegal forward pass', 'OFF: 5 yards from the spot of the foul and a loss of down', 'https://i.imgur.com/4CuuTDH.gif'],
            'illshift': ['Illegal shift', 'OFF: 5 yards', 'https://i.imgur.com/RDhSuUw.gif'],
            'inelrec': ['Inelligible receiver downfield', 'OFF: 5 yards', 'https://i.imgur.com/hIfsc5D.gif'],
            'persfoul': ['Personal foul', 'OFF: 15 yards\nDEF: 15 yards from the end spot of the play, automatic first down', 'https://i.imgur.com/dyWMN7p.gif'],
            'pi': ['Pass interference', 'OFF: 15 yards\nDEF: Lesser of either 15 yards or the spot of the foul, and an automatic first down (ball placed at the 2 yard line if penalty occurs in the endzone)', 'https://i.imgur.com/w1Tglj4.gif'],
            'ruffkick': ['Roughing/Running into the kicker', 'DEF: (running) 5 yards, (roughing, personal foul) 15 yards and automatic first down ', 'https://i.imgur.com/UuTBUJv.gif'],
            'ruffpass': ['Roughing the passer', 'DEF: 15 yards and an automatic first down (from the end of the play if pass is completed)', 'https://i.imgur.com/XqPE1Pf.gif'],
            'safety': ['Safety', 'DEF: 2 points and possession, opponent free kicks from their own 20 yard line', 'https://i.imgur.com/Y8pKXaH.gif'],
            'targeting': ['Targeting', 'OFF/DEF: 15 yard penalty, ejection ', 'https://i.imgur.com/qOsjBCB.gif'],
            'td': ['Touchdown', 'OFF: 6 points', 'https://i.imgur.com/UJ0AC5k.mp4'],
            'unsport': ['Unsportsmanlike', 'OFF: 15 yards\nDEF: 15 yards', 'https://i.imgur.com/6Cy9UE4.gif'],
            }
flag_dict = {'iowa': 'https://i.imgur.com/xoeCOwp.png',
             'northwestern': 'https://i.imgur.com/WG4kFP6.jpg',
             'ohio_state': 'https://i.imgur.com/coxjUAZ.jpg',
             'minnesota': 'https://i.imgur.com/54mF0sK.jpg',
             'michigan': 'https://i.imgur.com/XWEDsFf.jpg',
             'miami': 'https://i.imgur.com/MInQMLb.jpg',
             'iowa_state': 'https://i.imgur.com/w9vg0QX.jpg',
             'indiana': 'https://i.imgur.com/uc0Q8Z0.jpg',
             'colorado': 'https://i.imgur.com/If6MPtT.jpg',
             'wisconsin': 'https://giant.gfycat.com/PolishedFeminineBeardedcollie.gif',
             'texas': 'https://i.imgur.com/rB2Rduq.jpg',
             'purdue': 'https://i.imgur.com/8SYhZKc.jpg',
             'illinois': 'https://i.imgur.com/MxMaS3e.jpg',
             'maryland': 'https://i.imgur.com/G6RX8Oz.jpg',
             'michigan_state': 'https://i.imgur.com/90a9g3v.jpg',
             'penn_state': 'https://i.imgur.com/JkQuMXf.jpg',
             'rutgers': 'https://i.imgur.com/lyng39h.jpg',
             'south_alabama': 'https://i.imgur.com/BOH5reA.jpg',
             'northern_illinois': 'https://i.imgur.com/HpmAoIh.jpg'
             }


class ImageCommands(commands.Cog, name="Image Commands"):
    def __init__(self, bot):
        self.bot = bot
    # Start image commands
    @commands.command(aliases=["rf",])
    async def randomflag(self, ctx):
        """ A random ass, badly made Nebraska flag. """

        # This keeps bot spam down to a minimal.
        await function_helper.check_command_channel(ctx.command, ctx.channel)
        if not function_helper.correct_channel:
            await ctx.send(wrong_channel_text)
            return

        flags = []
        with open("flags.txt") as f:
            for line in f:
                flags.append(line)
        f.close()

        random.shuffle(flags)
        embed = discord.Embed(title="Random Ass Nebraska Flag")
        embed.set_image(url=random.choice(flags))
        await ctx.send(embed=embed)

    @commands.command(aliases=["cf",])
    async def crappyflag(self, ctx, state=""):
        """ Outputs crappy flag. The usage is $crappyflag <state>.

        The states are colorado, illinois, indiana, iowa, iowa_state, maryland:, miami, michigan, michigan_state, minnesota, northern_illinois, northwestern, ohio_state, penn_state, purdue, south_alabama, rutgers, texas, wisconsin """

        # This keeps bot spam down to a minimal.
        await function_helper.check_command_channel(ctx.command, ctx.channel)
        if not function_helper.correct_channel:
            await ctx.send(wrong_channel_text)
            return

        if state:
            state = state.lower()

            embed = discord.Embed(title="Crappy Flags")
            embed.set_image(url=flag_dict[state.lower()])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Crappy Flags")
            random_state = random.choice(list(flag_dict.keys()))
            embed.set_image(url=flag_dict[random_state])
            await ctx.send(embed=embed)

    @commands.command(case_insensitive=False)
    async def OHYEAH(self, ctx):
        """Pour that koolaid baby"""
        embed = discord.Embed(title="OH YEAH!")
        embed.set_image(url='https://media.giphy.com/media/3d9rkLNvMXahgQVpM4/source.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def iowasux(self, ctx):
        """ Iowa has the worst corn. """
        emoji = self.bot.get_emoji(441038975323471874)
        embed = discord.Embed(title="{} IOWA SUX {}".format(emoji, emoji))
        embed.set_image(url='https://i.imgur.com/j7JDuGe.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def potatoes(self, ctx):
        """ Potatoes are love; potatoes are life. """
        authorized = False

        for r in ctx.author.roles:
            if r.id == 583842320575889423:
                authorized = True

        if authorized:
            embed = discord.Embed(title="Po-Tay-Toes")
            embed.set_image(url='https://i.imgur.com/Fzw6Gbh.gif')
            await ctx.send(embed=embed)
        else:
            await ctx.send('You are not a member of the glorious Potato Gang!')

    @commands.command()
    async def asparagus(self, ctx):
        """ I guess some people like asparagus. """
        authorized = False

        for r in ctx.author.roles:
            if r.id == 583842403341828115:
                authorized = True

        if authorized:
            embed = discord.Embed(title="Asparagang")
            embed.set_image(url='https://i.imgur.com/QskqFO0.gif')
            await ctx.send(embed=embed)
        else:
            await ctx.send('You are not a member of the glorious Asparagang!')

    @commands.command()
    async def flex(self, ctx):
        """ S T R O N K """
        embed = discord.Embed(title="FLEXXX 😩")
        embed.set_image(url='https://i.imgur.com/92b9uFU.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def shrug(self, ctx):
        """ Who knows 😉 """
        embed = discord.Embed(title="🤷‍♀️")
        embed.set_image(url='https://i.imgur.com/Yt63gGE.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def ohno(self, ctx):
        """ This is not ideal. """
        embed = discord.Embed(title="Big oof")
        embed.set_image(url='https://i.imgur.com/f4P6jBO.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def bigsexy(self, ctx):
        """ Give it to me Kool Aid man. """
        embed = discord.Embed(title="OOOHHH YEAAHHH 😩")
        embed.set_image(url='https://i.imgur.com/UpKIx5I.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def whoami(self, ctx):
        """ OH YEAH! """
        embed = discord.Embed(title="OHHH YEAAAHHH!!")
        embed.set_image(url='https://i.imgur.com/jgvr8pd.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def thehit(self, ctx):
        """ The hardest clean hit ever. """
        embed = discord.Embed(title="CLEAN HIT!")
        embed.set_image(url='https://i.imgur.com/mKRUPoD.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def strut(self, ctx):
        """ Martinez struttin his stuff """
        embed = discord.Embed(title="dat strut")
        embed.set_image(url='https://media.giphy.com/media/iFrlakPVXLIj8bAqCc/giphy.gif')
        await ctx.send(embed = embed)

    @commands.command()
    async def guzzle(self, ctx):
        """ Let the cup runeth over """
        embed = discord.Embed(title="Give it to me bb")
        embed.set_image(url='https://i.imgur.com/OW7rChr.gif')
        await ctx.send(embed = embed)

    @commands.command(aliases=["td",])
    async def touchdown(self, ctx):
        """ Let the cup runeth over """
        embed = discord.Embed(title="🏈🎈🏈🎈")
        embed.set_image(url='https://i.imgur.com/Wh4aLYo.gif')
        await ctx.send(embed = embed)

    @commands.command(aliases=["ref",])
    async def referee(self, ctx, call):
        """ HuskerBot will tell you about common referee calls. Usage is `$refereee <call>`.\n
        The calls include: chip, chop, encroachment, facemask, hand2face, hold, illfwd, illshift, inelrec, persfoul, pi, ruffkick, ruffpas, safety, targeting, td, unsport """

        # This keeps bot spam down to a minimal.
        await function_helper.check_command_channel(ctx.command, ctx.channel)
        if not function_helper.correct_channel:
            await ctx.send(wrong_channel_text)
            return

        call = call.lower()

        penalty_name = ref_dict[call][0]
        penalty_comment = ref_dict[call][1]
        penalty_url = ref_dict[call][2]

        embed = discord.Embed(title='HuskerBot Referee', color=0xff0000)
        embed.add_field(name='Referee Call', value=penalty_name, inline=False)
        embed.add_field(name='Description', value=penalty_comment, inline=False)
        embed.set_thumbnail(url=penalty_url)
        embed.set_footer(text="Referee calls " + huskerbot_footer)
        await ctx.send(embed=embed)
    # End image commands


def setup(bot):
    bot.add_cog(ImageCommands(bot))