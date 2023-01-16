import discord
from discord.ext import commands

import json


#import stuff


client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())






#fix math
#fix add price flaot //310



numar = 0


@client.event
async def on_ready():
    print("M-am trezit. Bagati-ma in seama!")

    global numar
    with open("data_file.json", "r") as read_file:
        numar = json.load(read_file)



@client.command()
async def numara(ctx):
    global numar
    numar += 1
    await ctx.send(numar)

    with open("data_file.json", "w") as write_file:
        json.dump(numar, write_file)
    

host = 0
total_players = 0

game_started = False
@client.command()
async def start(ctx):
    global game_started
    if game_started == False:
        await ctx.send("The game of *Price is right* is starting.")
        game_started = True
        player_list.append(ctx.author)

        

        global game_channel
        game_channel = ctx

        player_score.append(0)
        player_prices.append(0)
        global host
        host = ctx.author
        global total_players
        total_players += 1

        await give_host(ctx.message.author)
        
        
        
    else:
        await ctx.send("There is already a game going on")
    



@client.event
async def give_host(user):
    role = discord.utils.get(user.guild.roles, name="priceisright-host")
    global host
    host = user
    message = "{} is now the host.".format(host.mention)
    await game_channel.send(message)
    await user.add_roles(role)

async def take_host(user):
    role = discord.utils.get(user.guild.roles, name="priceisright-host")
    await user.remove_roles(role)

#@client.event
async def remove_player(user):


    if user not in player_list:
        await game_channel.send("{} you didn't even join.".format(user.mention))
        return
    



    global total_players

    for i in range(total_players):
        if player_list[i] == user:
        
            player_list.pop(i)
            player_score.pop(i)
            player_prices.pop(i)
            break

    
    
    
    await game_channel.send("{} left the game".format(user.mention))

    total_players -= 1
    
    

    global curr_host
    #curr_host += 1
    if curr_host >= total_players:
        curr_host = 0

    if total_players <= 0:
        await end_game()
    else:
        if host == user:
            await give_host(player_list[curr_host])



async def end_game():
    global game_started
    game_started = False
    end_voters = []
    await game_channel.send("The game of *price is right* is over. Hope you didn't ecounter too many bugs (:)")

    #somethign else I can t think of right now
    #or maybe this is enough, idk



async def show_score():
    await game_channel.send("The current score is: ")
    for i in range(total_players):
        await game_channel.send("{} has the score of {}".format(player_list[i].mention, player_score[i]))

async def end_round():
    global price
    global k
    k = 1

    await game_channel.send("The round is over!")
    await game_channel.send("The price was {}".format(price))

    l = 0
    if player_list[0] == host:
        l = 1
    min = player_prices[l]
    for i in range(total_players):


        if player_list[i] == host:
            await game_channel.send("{} was the host".format(player_list[i].mention))
        else:
            if player_prices[i] > price:
                
                if player_score[i] > 0:
                    player_score[i] -= 1
                    await game_channel.send("{} guessed too high and lost a point.".format(player_list[i].mention))
                else:
                    await game_channel.send("{} guessed too high but there's nothing to take away.".format(player_list[i].mention))
            else:
                if    player_prices[i] > min: # player_prices[i]> max:
                    #max = player_prices[i]
                    min = player_prices[i]
    

    for i in range(total_players):
        if player_list[i] != host  and min <= price and player_prices[i] <= price  :
            if player_prices[i] == min : #player_prices[i] == max:
                player_score[i] += 1
                if player_prices[i] == price:
                    await game_channel.send("{} guessed the exact price, woah! The point won is surely well deserved.".format(player_list[i].mention))
                else:
                    await game_channel.send("{}'s guess was the closest and won a point.".format(player_list[i].mention))
            elif  player_prices[i]   < min     : # player_prices[i] < max
                await game_channel.send("{}'s guess was too off.".format(player_list[i].mention))

    await show_score()

    await take_host(host)
    global curr_host
    curr_host += 1
    if curr_host >= total_players:
        curr_host = 0
    await give_host(player_list[curr_host])

    for iop in range(total_players):
        player_prices[iop] = 0

    
    price = 0

curr_host = 0


@client.event
async def send_info():
    

    #await show_image()
    

    message = "The players are {}".format(player_list)
    await game_channel.send(message)
    message = "The score is {}".format(player_score)
    await game_channel.send(message)
    message = "The price guesses are {}".format(player_prices)
    await game_channel.send(message)
    message = "This thing costs {}".format(price)
    await game_channel.send(message)
    message = "The host is {}".format(host.mention)
    await game_channel.send(message)

    #get_user



@client.command()
async def leave(ctx):

    if game_started == False:
        await ctx.send("What are you leaving, there's not even a game started.")
        return

    if host == ctx.message.author:
        await take_host(host)

    await remove_player(ctx.author)
    
    

player_list = []
player_score = []
@client.command()
async def join(ctx):

    if game_started == False:
        await ctx.send("Sorry, there is no game to join. Maybe you want to start one yourself?")
        return

    if ctx.author not in player_list:
        player_list.append(ctx.author)
        message = "{} joined the game.".format(ctx.author.mention)
    

        player_score.append(0)
        player_prices.append(0)
        global total_players
        total_players += 1

    else:
        message = "{}, you are already playing.".format(ctx.author.mention)
    await ctx.send(message)







player_prices = []
k = 1
@client.command()
async def guess(ctx, pricee):

    

    if ctx.author == host:
        await game_channel.send("You can't try to guess your own submissions!")
        return
    
    if float(price) == 0:
        await ctx.send("Be patient.")
        return
    
    
    canbefloat=False
    for l in pricee:
        if l == "." or l.isnumeric():
            canbefloat = True

    if canbefloat == False:
        await ctx.send("Try again, but this time you should enter a number (Use . as decimal point if you need.")
        return
    

    pricee = float(pricee)

    if pricee < 0:
        await ctx.send("You're supposed to type a positive number...")
        return

    global k
    #k = 0 + 1
    for iop in range(total_players):
        if player_list[iop] == ctx.author:

            if player_prices[iop] == 0:
                k+=1
                await game_channel.send("{}/{} players took a guess.".format(k-1, total_players-1))

            player_prices[iop] = float(pricee)
        
    if k == total_players:
        #await game_channel.send("We checked all guesses of prices yada yada")
        await end_round()


game_channel = 0
"""
@client.command()
async def info(ctx):
    
    if game_started == False:
        await ctx.send("There is no info to be shown, you should start a game first!")
        return

    await send_info()
"""

f = 0
embed = 0
price = 0
@client.command()
async def add(ctx, pricee):
    

    if ctx.author != host:
        await ctx.send("It's not your turn!")
        return
    

    canbefloat=True
    for l in pricee:
        if not (l == "." or l.isnumeric()):
            canbefloat = False

    if canbefloat == False:
        await ctx.send("Try again, but this time you should enter a number (Use *.* as decimal point if you need).")
        return

    
    global price
    price = float(pricee)


    global f
    f = await ctx.message.attachments[0].to_file()
   

    embed = discord.Embed()
    embed.set_image(url=f"attachment://{f.filename}")
    await game_channel.send(file=f, embed=embed)

    await game_channel.send("You started the game with {} players. Try to guess what is the price of this item.".format(total_players))
    #await show_image()

async def show_image():

    await game_channel.send(file=f, embed=embed)


end_vote_count = 0
end_voters = []
@client.command()
async def end(ctx):

    global player_list, player_prices, player_score, total_players

    global end_voters
    if ctx.author not in end_voters:
        end_voters.append(ctx.author)
    else:
        await ctx.send("You can only vote once!")
        return

    if ctx.message.author not in player_list:
        await ctx.send("You can't vote to end the game if you aren't playing!")
        return

    votes_needed = total_players - 1
    global end_vote_count
    end_vote_count += 1
    if votes_needed - end_vote_count > 0:
        await game_channel.send("{} players voted to end the game. We need {} more votes to end the game. ".format(end_vote_count, votes_needed - end_vote_count))
    else:
        await game_channel.send("{} chose to end the game.".format(ctx.author.mention))
    
    if end_vote_count >= votes_needed:
        end_vote_count = 0

        
        player_list = []
        player_prices = []
        player_score = []
        total_players = 0

        await end_game()


@client.command()
async def info(ctx):
    await ctx.send("!info - shows you this list")
    await ctx.send("!start - start a game")
    await ctx.send("!add *number* + attachment - use this command when you want to start a round. You must attach an image and write a price")
    await ctx.send("!join - join an ongoing game")
    await ctx.send("!leave - leave the game")
    await ctx.send("!end - vote for the game to end, all players but one must vote for the game to end")



client.run('MTA2MDUwMDQ5NDQ5NTI2NDgyOQ.G5ANUb.8vx1zIxmGsPBkMHJMoZZkjs7eV1WmSDt9Zjl0E')