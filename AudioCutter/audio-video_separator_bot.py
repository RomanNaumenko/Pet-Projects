"""
A slightly changed conception. Created telegram-bot that take a link from YouTube,
downloads the video(.mp4 format), and separately downloads the audio of this video(.mp3 format)
"""
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from pytube import YouTube
import moviepy.editor


API_TOKEN = os.getenv("API_TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def invitation_message(message: types.Message):
    chat_id = message.chat.id
    text = "Input link to your video, please."
    await bot.send_message(chat_id=chat_id, text=text)


@dp.message_handler()
async def text_message(message: types.Message):
    chat_id = message.chat.id
    url = message.text
    yt = YouTube(url)
    if message.text.startswith == "https://youtu.be/" or "https://www.youtube.com/":
        await bot.send_message(chat_id, f"Video download is started: {yt.title}\n"
                                        f"Video from channel: {yt.author} ({yt.channel_url})")
        await youtube_downloader_and_slicer(url, message, bot)


async def youtube_downloader_and_slicer(url, message, bot):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension="mp4")
    video.get_highest_resolution().download(f'{yt.title}', filename=f'{yt.title}.mp4')
    with open(f"{yt.title}/{yt.title}.mp4", "rb") as video_file:
        await bot.send_video(message.chat.id, video_file, caption="Your video file")
        os.remove(f'{yt.title}/{yt.title}.mp4')

    audio = yt.streams.filter(only_audio=True).first()
    out_file = audio.download(f'{yt.title}', filename=f'{yt.title}.mp4')
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    with open(f"{new_file}", "rb") as audio_file:
        await bot.send_audio(message.chat.id, audio_file, caption="Audio track of video above")
        os.remove(f'{new_file}')


async def audio_cutter(video_file):
    video = moviepy.editor.VideoFileClip(f'{video_file}')
    audio = video.audio
    await audio.write_audiofile(f'{video_file.stem}.mp3')


# @dp.message_handler(content_types=types.ContentType.VIDEO)
# async def try_to_upload_video(message: types.Message):
#     audio_track = audio_cutter(message)
#     await message.reply(audio_track)


if __name__ == "__main__":
    executor.start_polling(dp)
