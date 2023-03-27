# PlexDiscord
Discord / Plex Integration

Developed by: Daniel Stern

This application is a Discord bot that can search a user's Plex library for movies or TV shows and play them in a voice channel. The bot uses the discord.py library to interact with Discord and the PlexAPI library to interact with Plex.

The bot has several commands, including:

!search: searches the user's Plex library for a movie or TV show and returns a list of results.
!join: makes the bot join the voice channel of the user who issued the command.
!leave: makes the bot leave the voice channel.
!play: plays a video from the Plex library in the voice channel.
!pause: pauses the audio or video that is currently playing.
!resume: resumes playing the audio or video that was paused.
!stop: stops playing the audio or video.
When the user issues the !play command, the bot searches the user's Plex library for the specified movie or TV show title. If a match is found, the bot plays the video in the voice channel. The bot retrieves the audio and video stream URLs from the Plex server and uses the FFmpeg library to play the audio and video streams separately. The bot allows the user to pause, resume, or stop playback at any time.

To use this application, the user needs to have a Discord bot token, a Plex account, and the PlexAPI library installed. The user also needs to specify the Plex username, password, and server name in the code.
