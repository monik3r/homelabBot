#!/usr/bin/python3

from discord.ext.commands import Bot
from os import getenv
import discord, json, pyombi

# Set up Ombi stuff
ombi = pyombi.Ombi(
    ssl=True,
    host=getenv("ombiHost"),
    port = "443",
    username = getenv("ombiUsername"),
    api_key= getenv("ombiKey")
)

ombi.authenticate()
try:
    ombi.test_connection()
except pyombi.OmbiError as e:
    print(e)

client = discord.Client()
bot = Bot(command_prefix='!')

@bot.command(pass_context=True)
async def addrole(ctx, role: discord.Role):
    member = ctx.message.author
    await member.add_roles(role)

@bot.command(pass_context=True)
async def removerole(ctx, role: discord.Role):
    member = ctx.message.author
    await member.remove_roles(role)

@bot.command(pass_context=True)
async def request(ctx, desire, title):
    member = ctx.message.author
    channel = ctx.message.channel

    role_names = [role.name for role in member.roles]
    if "Videos" in role_names:
        #await channel.send('Send me that 👍 reaction, mate')
        if(desire == 'movie'):
            res = ombi.search_movie(title)
            printyprint = "Here are the top 7 results, we already track those with (%) :\n```\n"
            i = 0
            for title in res[:7]:
                if(title["requested"]):
                    printyprint += ("(%) ")
                printyprint +=(str(i) + ") " + (title["originalTitle"] + " : "+ title["overview"])[:200] + "\n")
                i+=1
            printyprint+="```\nRespond with the result number to select a show"
            await channel.send(printyprint)

            def check(m):
                if m.content.isdigit() and m.author == member:
                    return(int(m.content) < 7)
                else:
                    return False

            whichShow = await bot.wait_for('message', check=check, timeout=30.0)
            
            if whichShow is None:
                await channel.send("Request timed out, yell at andrew if this is too short (if you're seeing this it probably is :crab: )")
            else:
                imgUrl = "https://image.tmdb.org/t/p/w500" + res[int(whichShow.content)]["posterPath"]
                await channel.send("Is this the right movie? (y/n) \n" + imgUrl)
                
                def checkYes(m):
                    if m.content == 'y' or m.content == 'n':
                        return True
                    return False

                yesOrNo = await bot.wait_for('message', check = checkYes, timeout =30.0)
                if(yesOrNo) is None:
                    await channel.send("F, sorry fam :'(")
                elif(yesOrNo.content) == 'y':
                    await channel.send("You got it fam")
                    ombi.request_movie(res[int(whichShow.content)]["theMovieDbId"])
                elif(yesOrNo.content) == 'n':
                    await channel.send("F, sorry fam :'(")

            #print(json.dumps(res))
        elif(desire == 'tv'):
            res = ombi.search_tv(title)
            printyprint = "Here are the top 7 results:\n```\n"
            i = 0
            for title in res[:7]:
                printyprint +=(str(i) + ") " + (title["title"] + " : "+ title["overview"])[:200] + "\n")
                i+=1
            printyprint+="```\nRespond with the result number to select a show"
            await channel.send(printyprint)

            def check(m):
                if m.content.isdigit() and m.author == member:
                    return(int(m.content) < 7)
                else:
                    return False

            whichShow = await bot.wait_for('message', check=check, timeout=30.0)
            
            if whichShow is None:
                await channel.send("Request timed out, yell at andrew if this is too short (if you're seeing this it probably is :crab: )")
            else:
                imgUrl = res[int(whichShow.content)]["banner"]
                await channel.send("Is this the right show? (y/n) \n" + imgUrl)
                
                def checkYes(m):
                    if m.content == 'y' or m.content == 'n':
                        return True
                    return False

                yesOrNo = await bot.wait_for('message', check = checkYes, timeout =30.0)
                if(yesOrNo) is None:
                    await channel.send("F, sorry fam :'(")
                elif(yesOrNo.content) == 'y':
                    await channel.send("You got it fam")
                    ombi.request_tv(res[int(whichShow.content)]["id"], request_latest=True)
                elif(yesOrNo.content) == 'n':
                    await channel.send("F, sorry fam :'(")
    else:
        await channel.send("You don't have the right permissions! Check out `!addrole Videos`")

@bot.command(pass_context=True)
async def wgGen(ctx, desire, title):
    await channel.send("This doesn't quite work yet, tomorrow though! Also need to update firewall off of roles.")

bot.run(getenv("discordKey"))