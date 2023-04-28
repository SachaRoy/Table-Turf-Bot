# Importation des bibliothèques
import discord
from discord.ext import commands
from random import randint as rd
import datetime
from Database.db_handler import DatabaseHandler

# Initialisation des instances et variables nécessaires
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix = "/", intents = intents, descritption = "Table Turf Bot")
database_handler = DatabaseHandler("data.db")
partie = []

maps = {
    1: "<:X_Marks_the_Garden:1081928640511606916>",
    2: "<:Thunder_Point:1081928637772742717>",
    3: "<:Double_Gemini:1081928635981770854>",
    4: "<:Square_Squared:1081928571989266472>",
    5: "<:River_Drift:1081928570605154405>",
    6: "<:Main_Street:1081928566968688650>",
    7: "<:Lakefront_Property:1081928562208145439>",
    8: "<:Board_Box_Seats:1081927979820650596>"
}

# Fonctions
def print_commande_terminal(nom: str, ctx)->None:
    '''Affiche les commandes utilisées en temps réel: -[date + heure] -commande -utilisateur -salon.'''
    print("[" + str(datetime.datetime.today())[:19] + "] " + str(nom) + " used by " + str(ctx.author.name) + " on #" + str(ctx.channel))

def distance(n1: int, n2: int)->int:
    '''Calcule la distance entre n1 et n2.'''
    if n1 == n2:
        return 1
    elif n1 > n2:
        return n1 - n2
    else:
        return n2 - n1

def calc_power(id1, s1, id2, s2):
    '''Renvoie le tupple ('gain j1', 'gain j2', 'power j1', 'power j2').'''
    p1 = database_handler.get_power(id1)
    p2 = database_handler.get_power(id2) 

    if s1 > s2:
        g1 = 20 + round(10*distance(s1, s2)*1/distance(p1, p2))
        g2 = -20 - round(10*distance(s1, s2)*1/distance(p1, p2))
    else:
        g2 = 20 + round(10*distance(s1, s2)*1/distance(p1, p2))
        g1 = -20 - round(10*distance(s1, s2)*1/distance(p1, p2))

    return (g1, g2, p1 + g1, p2 + g2)


# Commandes
@bot.event
async def on_ready():
    print("")
    print("[" + str(datetime.datetime.today())[:19] + "] En ligne")

    await bot.change_presence(activity = discord.Game(name = "/aide"))

@bot.command()
async def rdmap(ctx):
    print_commande_terminal("'rdmap'", ctx)
    await ctx.send(maps[rd(1, 8)])

@bot.command()
async def login(ctx):
    if ctx.channel.name == "login-bot":
        if database_handler.is_in(ctx.author.id):
            await ctx.send(ctx.author.name + " est déjà inscrit.")
        else:
            database_handler.add(ctx.author.id, ctx.author.name)
            await ctx.send(ctx.author.name + " est inscrit :white_check_mark: !")
    print_commande_terminal("'login'", ctx)

@bot.command()
async def game(ctx):
    if ctx.channel.category.id == 1081905548192120932 or ctx.channel.name == "tests-bot":
        print_commande_terminal("'game'", ctx)

        if ctx.channel.id not in partie:
            partie.append(ctx.channel.id)

            def join(message):
                return message.content == "!j" and message.channel == ctx.channel

            await ctx.send("**Partie crée**")
            await ctx.send("Il reste encore **2** places, tapez **'!j'** pour la rejoindre.")
            j1 = await bot.wait_for("message", timeout = 10000, check = join)

            if database_handler.is_in(j1.author.id):
                await ctx.send(f"<@&{1081918052209274920}> Il reste encore **1** place, tapez **'!j'** pour rejoindre la partie.")
                j2 = await bot.wait_for("message", timeout = 10000, check = join)

                if database_handler.is_in(j2.author.id):
                    if j1.author != j2.author:
                        await ctx.send("La game se jouera en **BO5**")
                        await ctx.send("Vous pouvez jouer avec les maps que vous voulez, vous pouvez également utiliser la commande **'/rdmap'** pour obtenir une map aléatoire.")
                        await ctx.send(f"A chaque manche, donnez le vainqueur en envoyant **!1** s'il s'agit de <@{j1.author.id}> ou **!2** s'il s'agit de <@{j2.author.id}>.")

                        def check(message):
                            return (message.author == j1.author or message.author == j2.author) and (message.content == "!1" or message.content == "!2")

                        manche = 1
                        s1, s2 = 0, 0

                        while s1 < 3 and s2 < 3:
                            await ctx.send("__**Manche "+str(manche)+"**__")
                            rep_client = await bot.wait_for("message", timeout = 10000, check = check)
                            gagnant = str(rep_client.content)

                            if gagnant == "!1":
                                s1 += 1
                                manche += 1

                            else:
                                s2 += 1
                                manche += 1

                        if s1 == 3:
                            database_handler.add_win(j1.author.id)
                            database_handler.add_game(j2.author.id)
                        else:
                            database_handler.add_win(j2.author.id)
                            database_handler.add_game(j1.author.id)

                        g1, g2, p1, p2 = calc_power(j1.author.id, s1, j2.author.id, s2)
                        # p1 = int(j1.author.id, database_handler.get_power(j1.author.id))
                        # p2 = int(j2.author.id, database_handler.get_power(j2.author.id))

                        database_handler.set_power(j1.author.id, p1)
                        database_handler.set_power(j2.author.id, p2)

                        await ctx.send("Les scores ont bien étés pris en compte, merci d'avoir joué !")
                        partie.remove(ctx.channel.id)
                        await ctx.send(f"Power de <@{j1.author.id}>: **"+str(database_handler.get_power(j1.author.id))+"** ("+str(g1)+")")
                        await ctx.send(f"Power de <@{j2.author.id}>: **"+str(database_handler.get_power(j2.author.id))+"** ("+str(g2)+")")
                    
                    else:
                        await ctx.send("Il n'est pas possible de lancer une partie contre soi-même.")
                        partie.remove(ctx.channel.id)
                else:
                    await ctx.send("Tu n'es pas dans la base de donnée. Va t'inscrire en tapant '/login' dans #login-bot avant de jouer.")
                    partie.remove(ctx.channel.id)
            else:
                await ctx.send("Tu n'es pas dans la base de donnée. Va t'inscrire en tapant '/login' dans #login-bot avant de jouer.")
                partie.remove(ctx.channel.id)
        else:
            await ctx.send("Une partie est déjà en cours dans ce salon, merci d'aller à une autre table pour jouer.")



@bot.command()
async def aide(ctx):
    print_commande_terminal("'aide'", ctx)

    embed_commandes = discord.Embed(title = "Commandes", description = "Préfixe à mettre avant le nom de la commande: /", color = 0x5900FF)
    embed_commandes.add_field(name = "rdmap", value = "Donne une map aléatoire.", inline = False)
    embed_commandes.add_field(name = "game", value = "Lance une ranked.", inline = False)
    embed_commandes.add_field(name = "aide", value = "Affiche la liste des commandes.", inline = False)
    await ctx.send(embed=embed_commandes)

    embed_support = discord.Embed(title = "Support", description = "Si vous rencontrer des problèmes ou un bug, merci de contacter **Bass#2362**.", color = 0x000000)
    await ctx.send(embed=embed_support)

    embed_soutien = discord.Embed(title = "Nous soutenir", description = "Si l'envie vous en dit, vous pouvez faire un don sur Paypal pour pouvoir continuer à heberger le bot.", color = 0xFFFFFF)
    await ctx.send(embed=embed_soutien)


# Lancer le bot
bot.run("TOKEN")