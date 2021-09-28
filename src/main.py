import os
import random
import discord
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


bot.author_id = "207281758167760896"  # Change to your discord id!!!

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier



@bot.command(name='name', help='Tells you that the bot is speaking.')
async def speak_bot(ctx):
    response = "```" + str(ctx.author) + " is speaking```"
    await ctx.send(response)


@bot.command(name='count', help='Count')
async def count_bot(ctx): 
    status = {
        'Online' : 0, 'Offline': 0, 'Idle' : 0, 'Do not disturb' : 0
    }

    online = 0
    idle = 0
    offline = 0
 
    for i in client.get_all_members():
         print( i )
    # await client.wait_until_ready()
    if not client.is_closed:
        print('hereee')
        for server in client.servers:
            for member in server.members:
                if str(member.status) == 'online':
                    online += 1
                    print(online)
                elif str(member.status) == 'idle':
                    idle += 1
                    print(idle)
                else:
                    offline += 1
        # await client.close()

    totalUsers = online + idle
    print(totalUsers)
    await ctx.send(totalUsers)

@bot.command(name='admin', help='admin')
async def admin_bot(ctx, member: discord.Member):
    """
    The bot will add an admin role to the user and he will have full access and if the role is not created it will create it and give him the role"  
    !admin <@member>
    """
    if get(ctx.guild.roles, name="Admins"):
        print("Admins role already exists")
    else:
        perms = discord.Permissions.membership()
        perms.update(manage_channels=True, kick_members= True,
                                        ban_members=True, send_messages=True, read_messages=True)
                                        
         
        await ctx.guild.create_role(name="Admins", permissions=perms, colour=discord.Colour(0xF50B0B))
        print("Admins role was created!")

    role = discord.utils.find(lambda r: r.name == 'Admins', ctx.message.guild.roles)
    
    if role in member.roles:
        await ctx.send("{} is already Admins".format(member))

    else:
        await member.add_roles(role)
        await ctx.send("{} was added to Admins".format(member))

         


@bot.command(name='mute', help='create a Ghost role, disabling all textual channels permissions for that member. When typing that command towards an already muted member, the action should be reverted')
async def mute_bot(ctx, member: discord.Member):
    """
    The bot will mute a user and great a Ghost role , if the command is called on a muted user it will unmute him  
    !mute <@member>
    """
    if get(ctx.guild.roles, name="Ghost"):
        print("Ghost role already exists")
    else:
        perms = discord.Permissions(send_messages=False, read_messages=True)
        await ctx.guild.create_role(name="Ghost", permissions=perms, colour=discord.Colour(0x0062ff))
        print("Ghost role was created!")

    role = discord.utils.find(lambda r: r.name == 'Ghost', ctx.message.guild.roles)

    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send("{} was unmuted".format(member))

    else:
        await member.edit(roles=[role]) 
        await ctx.send("{} was muted".format(member))


@bot.command(name='ban', help='`!ban <A member nickname>, your bot should ban that member from the server (Test with caution)')
async def ban_bot(ctx, member: discord.Member, reason="You dont deserve to be here"):
    """
    Ban a member 
    !ban <@member>
    """
    await member.ban(reason=reason) 
    await ctx.send(f'User {member} has been banned from the server.') 


# It's all fun and games
@bot.command(name='xkcd', help='`!xkcd, your post should post a random comic from https://xkcd.com')
async def kcdb_bot(ctx):
    """
    Post a random meme from the site xkcd 
    !xkcd
    """
    number = random.randint(1,2521)
    site = "https://xkcd.com/{}/".format(number) 
    await ctx.send(site) 

#Bonus

@bot.command(name='repeat', help='`!repeat <word>, your bot should repeat the same word you said!')
async def repeat_bot(ctx,arg):
    """
    The bot will repeat what you say  
    !repeat <word>
    """
    await ctx.send(arg)

@bot.command(name='kick', help='`!kick <A member nickname>, your bot will kick a user!')
async def kick_bot(ctx, member: discord.Member, reason="You dont deserve to be here" ):
    """
    The bot will kick a user from the discord server  
    !kick <@Member>
    """ 
    await member.kick(reason=reason) 
    await ctx.send(f'User {member} has been kicked from the server.')     


@bot.command(name='poll', help='')
async def poll(ctx, question, *cmd: str): 
    """
    Conduct a poll 
    !poll
    """

    if len(cmd) <= 1:
        await ctx.send('Not enough options to create a poll!')
        return
    if len(cmd) > 10:
        await ctx.send('Too much options!')
        return
    
    if len(cmd) == 2:
        reactions = ['👍', '👎']
    else:
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    embed = discord.Embed(title=question, description=''.join(cmd))
    react_message = await ctx.send(embed=embed)

    for reaction in reactions[:len(cmd)]:
        await react_message.add_reaction(reaction)
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await react_message.edit_message(embed=embed)

#DO NOT TOUCH
token = ""
bot.run(token)  # Starts the bot