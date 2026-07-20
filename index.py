import os
import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv

# .env
load_dotenv()
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GKEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=GKEY)
# el modelo tiene q ser ese pq no me da para otro eh
modelo_ia = genai.GenerativeModel('gemini-3.5-flash') 

# Intents y Prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"logged como {bot.user}")
    await bot.tree.sync()
@bot.tree.command(name="ia_help", description="Muestra la ayuda de los comandos de IA")
@app_commands.guild_only()
async def ia_help(interaction: discord.Interaction):
    help_message = (
        "Información Acerca de la IA\n"
        "La IA por ahora no tiene memoria de conversaciones anteriores o contexto persistente.\n"
        "Esto quiere decir que cada vez que le hagas una pregunta, no recordará lo que le preguntaste antes.\n")
    await interaction.response.send_message(help_message, ephemeral=True)   

@bot.tree.command(name="preguntar", description="Hazle una pregunta a la Inteligencia Artificial (Chat Externo)")
@app_commands.guild_only()
async def preguntar(interaction: discord.Interaction, pregunta: str):
    
    await interaction.response.defer()
    
    try:
        
        respuesta_ia = await modelo_ia.generate_content_async(pregunta)
        # por ahora ningun chat tiene memoria cosa que se aclara en el comando /ia_help
        await interaction.followup.send(f"**Pregunta:** {pregunta}\n\n**Respuesta:** {respuesta_ia.text}")
        
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error al procesar la IA: {e}")

bot.run(TOKEN_DISCORD)