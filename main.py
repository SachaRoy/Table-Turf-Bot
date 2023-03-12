# Importation des bibliothèques
import discord
from discord.ext import commands
from random import randint as rd

# Initialisation des instances et variables nécessaires
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix = "/", intents = intents, descritption = "Table Turf Bot")

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

# Commandes
@bot.event
async def on_ready():
    print("En ligne")
    print("")

@bot.command()
async def rdmap(ctx):
    print("/rdmap utilisée")
    await ctx.send(maps[rd(1, 8)])

@bot.command()
async def aide(ctx):
    embedVar = discord.Embed(title = "Commandes", description = "Préfixe à mettre avant le nom de la commande: /", color = 0x5900FF)
    embedVar.add_field(name = "rdmap", value = "Donne une map aléatoire.", inline = False)
    embedVar.add_field(name = "aide", value = "Affiche la liste des commandes.", inline = False)
    print("/aide utilisée")
    await ctx.send(embed=embedVar)


# Lancer le bot
bot.run("TOKEN")