import os
import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Cargar las llaves ocultas del archivo .env
load_dotenv()
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GKEY = os.getenv("GEMINI_KEY")

# 2. Configurar la Inteligencia Artificial
genai.configure(api_key=GKEY)
# Usamos el modelo flash que es ultra rápido
modelo_ia = genai.GenerativeModel('gemini-3.5-flash') 

# 3. Configurar el Bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot listo como {bot.user}")
    await bot.tree.sync()
@bot.tree.command(name="ia_help", description="Muestra la ayuda de los comandos de IA")
@app_commands.guild_only()
async def ia_help(interaction: discord.Interaction):
    help_message = (
        "Información Acerca de la IA\n"
        "La IA por ahora no tiene memoria de conversaciones anteriores o contexto persistente.\n"
        "Esto quiere decir que cada vez que le hagas una pregunta, no recordará lo que le preguntaste antes.\n")
    await interaction.response.send_message(help_message, ephemeral=True)   
# 4. El Comando de Barra con IA
@bot.tree.command(name="preguntar", description="Hazle una pregunta a la Inteligencia Artificial (Chat Externo)")
@app_commands.guild_only()
async def preguntar(interaction: discord.Interaction, pregunta: str):
    """
    Al poner 'pregunta: str' dentro del paréntesis, Discord automáticamente 
    le creará una casilla de texto al usuario para que escriba su duda.
    """
    # 1. Le avisamos a Discord que la IA va a tardar en pensar. 
    # Esto hace que salga el mensaje "El bot está pensando..." y nos da 15 minutos de tiempo extra.
    await interaction.response.defer()
    
    try:
        # 2. Le mandamos la pregunta a Gemini usando la versión ASÍNCRONA (_async)
        # Así el bot puede atender a otros usuarios mientras Gemini procesa el texto
        respuesta_ia = await modelo_ia.generate_content_async(pregunta)
        
        # 3. Como usamos defer(), ya no podemos usar 'send_message'. 
        # Ahora usamos 'followup.send' para enviar la respuesta final.
        await interaction.followup.send(f"**Pregunta:** {pregunta}\n\n**Respuesta:** {respuesta_ia.text}")
        
    except Exception as e:
        await interaction.followup.send(f"Ocurrió un error al procesar la IA: {e}")

bot.run(TOKEN_DISCORD)