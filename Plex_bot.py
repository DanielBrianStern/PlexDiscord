import os
import discord
import subprocess
from plexapi.myplex import MyPlexAccount
from plexapi.media import Media
from discord.ext import commands
from discord.utils import get

TOKEN = 'Token'
PLEX_USERNAME = 'Username'
PLEX_PASSWORD = 'Password'
PLEX_SERVER_NAME = 'Server'

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='search', help='Search Plex library for a movie or TV show.')
async def search(ctx, *, query):
    print("Search command called")
    account = MyPlexAccount(PLEX_USERNAME, PLEX_PASSWORD)
    plex = account.resource(PLEX_SERVER_NAME).connect()

    results = plex.search(query)
    print(f"Search results: {results}")

    if not results:
        await ctx.send(f"No results found for '{query}'.")
    else:
        result_titles = "\n".join([f"{i + 1}. {result.title} ({result.type.capitalize()})" for i, result in enumerate(results) if result.type in ['movie', 'show']])
        response = f"Search results for '{query}':\n{result_titles}"
        await ctx.send(response)

@bot.command(name='join', help='Join a voice channel.')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You must be in a voice channel to use this command.")

@bot.command(name='leave', help='Leave the voice channel.')
async def leave(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("I left the voice channel.")
    else:
        await ctx.send("I am not connected to a voice channel.")

@bot.command(name='play', help='Play a video from Plex.')
async def play(ctx, *, title):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        await ctx.send('The bot is not connected to a voice channel.')
        return
        
    if voice_client.is_connected():
        account = MyPlexAccount(PLEX_USERNAME, PLEX_PASSWORD)
        plex = account.resource(PLEX_SERVER_NAME).connect()
        results = plex.search(title)
        
        for result in results:
            if result.type in ['movie', 'episode']:
                media = result.media[0]
                part = media.parts[0]
                audio_url = result.getStreamURL(media=media, part=part)
                video_url = result.getStreamURL(media=media, part=part, videoResolution="1080")
                
                audio_source = discord.FFmpegPCMAudio(audio_url, options="-nostdin")
                video_source = discord.FFmpegPCMAudio(video_url, options="-nostdin")
                player = voice_client.play(discord.PCMVolumeTransformer(audio_source, volume=1.0))
                await ctx.send(f'**Now playing:** {result.title}')
                
                # Pause the audio stream and play the video stream
                player.pause()
                video_player = voice_client.play(discord.PCMVolumeTransformer(video_source, volume=1.0), after=lambda e: print('done', e))
                while video_player.is_playing():
                    await asyncio.sleep(1)
                
                # Resume the audio stream and stop the video stream
                player.resume()
                video_player.stop()
                
                return
        await ctx.send("No matching video found in Plex library.")
    else:
        await ctx.send('The bot is not connected to a voice channel.')

        
@bot.command(name='pause', help='Pause the audio or video.')
async def pause(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send('Playback paused.')
    else:
        await ctx.send('Nothing is playing.')

@bot.command(name='resume', help='Resume playing the audio or video.')
async def resume(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send('Playback resumed.')
    else:
        await ctx.send('Nothing is paused.')

@bot.command(name='stop', help='Stop playing the audio or video.')
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Playback stopped.')
    else:
        await ctx.send('Nothing is playing.')

bot.run(TOKEN)
