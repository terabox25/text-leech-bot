import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await asyncio.sleep(3600)  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
    
@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
       f"𝐇𝐞𝐥𝐥𝐨 ❤️\n\n◆〓◆ ❖ 𝐖𝐃 𝐙𝐎𝐍𝐄 ❖ ™ ◆〓◆\n\n❈ I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File Om Telegram So Basically If You Want To Use Me First Send Me ⟰ /upload Command And Then Follow Few Steps..", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✜ 𝐉𝐨𝐢𝐧 𝐔𝐩𝐃𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ✜" ,url=f"https://t.me/Opleech_WD") ],
                    [
                    InlineKeyboardButton("✜ 𝗔𝘀𝗵𝘂𝘁𝗼𝘀𝗵𝗚𝗼𝘀𝘄𝗮𝗺𝗶𝟮𝟰 ✜" ,url="https://t.me/AshutoshGoswami24") ],
                    [
                    InlineKeyboardButton("🦋 𝐅𝐨𝐥𝐥𝐨𝐰 𝐌𝐞 🦋" ,url="https://t.me/Opleech_WD/13") ]                               
            ]))


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐭 ♦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def account_login(bot: Client, m: Message):
    # Ask the user if they want to upload from a link or a .txt file
    editable = await m.reply_text('Do you want to upload from a link or a .txt file?\n\nSend "link" for direct link upload or "file" for .txt file upload.')

    # Listen for user input
    user_choice: Message = await bot.listen(editable.chat.id)
    choice = user_choice.text.lower()
    await user_choice.delete(True)

    # If user chooses to upload from a link
    if choice == "link":
        await editable.edit("Please send the direct download link.")
        input_link: Message = await bot.listen(editable.chat.id)
        link = input_link.text
        await input_link.delete(True)

        # Proceed with the download and upload process for the link
        await editable.edit(f"Starting upload for the provided link: {link}")

        # Ask for batch name
        await editable.edit("Please send me your batch name")
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)

        # Ask for video resolution
        await editable.edit("Enter resolution 🎬\n☞ 144, 240, 360, 480, 720, 1080\nPlease choose quality")
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        try:
            if raw_text2 == "144":
                res = "256x144"
            elif raw_text2 == "240":
                res = "426x240"
            elif raw_text2 == "360":
                res = "640x360"
            elif raw_text2 == "480":
                res = "854x480"
            elif raw_text2 == "720":
                res = "1280x720"
            elif raw_text2 == "1080":
                res = "1920x1080"
            else:
                res = "UN"
        except Exception:
            res = "UN"

        # Ask for caption
        await editable.edit("✏️ Now enter a caption to add on your uploaded file")
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        highlighter = f"️ ⁪⁬⁮⁮⁮"
        if raw_text3 == 'Robin':
            MR = highlighter
        else:
            MR = raw_text3

        # Ask for thumbnail
        await editable.edit("🌄 Now send the Thumb URL\nEg » https://graph.org/file/419c60736fbac058c9e50.jpg\n\nOr if you don't want a thumbnail send 'no'")
        input6 = message = await bot.listen(editable.chat.id)
        raw_text6 = input6.text
        await input6.delete(True)
        await editable.delete()

        thumb = input6.text
        if thumb.startswith("http://") or thumb.startswith("https://"):
            getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
            thumb = "thumb.jpg"
        else:
            thumb = "no"

        # Process the direct link download
        url = link
        name = f'{str(1).zfill(3)}) {raw_text0[:60]}'  # Adjust the file naming convention as per your needs

        if "youtu" in url:
            ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
        else:
            ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

        if "jw-prod" in url:
            cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
        else:
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

        try:
            cc = f'**[ 🎥 ] Vid_ID:** {str(1).zfill(3)}. **{raw_text0}{MR}.mkv\n✉️ Batch » **{raw_text0}**'
            Show = f"❊⟱ Downloading ⟱❊ »\n\n📝 Name » `{name}\n⌨ Quality » {raw_text2}`\n\n**🔗 URL »** `{url}`"
            prog = await m.reply_text(Show)
            res_file = await helper.download_video(url, cmd, name)
            filename = res_file
            await prog.delete(True)
            await helper.send_vid(bot, m, cc, filename, thumb, name, prog)

        except Exception as e:
            await m.reply_text(f"⌘ Downloading interrupted\n{str(e)}\n⌘ Name » {name}\n⌘ Link » `{url}`")

    # If user chooses to upload from a .txt file
    elif choice == "file":
        await editable.edit('Please send the .txt file containing the download links.')
        input: Message = await bot.listen(editable.chat.id)
        x = await input.download()
        await input.delete(True)

        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                links.append(i.split("://", 1))
            os.remove(x)
        except:
            await m.reply_text("Invalid file input.")
            os.remove(x)
            return

        await editable.edit(f"Total links found: {len(links)}\n\nSend the starting point (default is 1)")
        input0: Message = await bot.listen(editable.chat.id)
        raw_text = input0.text
        await input0.delete(True)

        await editable.edit("Now please send me your batch name")
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)

        await editable.edit("Enter resolution 🎬\n☞ 144, 240, 360, 480, 720, 1080\nPlease choose quality")
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        try:
            if raw_text2 == "144":
                res = "256x144"
            elif raw_text2 == "240":
                res = "426x240"
            elif raw_text2 == "360":
                res = "640x360"
            elif raw_text2 == "480":
                res = "854x480"
            elif raw_text2 == "720":
                res = "1280x720"
            elif raw_text2 == "1080":
                res = "1920x1080"
            else:
                res = "UN"
        except Exception:
            res = "UN"

        await editable.edit("✏️ Now enter a caption to add on your uploaded file")
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        highlighter = f"️ ⁪⁬⁮⁮⁮"
        if raw_text3 == 'Robin':
            MR = highlighter
        else:
            MR = raw_text3

        await editable.edit("🌄 Now send the Thumb URL\nEg » https://graph.org/file/419c60736fbac058c9e50.jpg\n\nOr if you don't want a thumbnail send 'no'")
        input6 = message = await bot.listen(editable.chat.id)
        raw_text6 = input6.text
        await input6.delete(True)
        await editable.delete()

        thumb = input6.text
        if thumb.startswith("http://") or thumb.startswith("https://"):
            getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
            thumb = "thumb.jpg"
        else:
            thumb = "no"

        if len(links) == 1:
            count = 1
        else:
            count = int(raw_text)

        try:
            for i in range(count - 1, len(links)):
                V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
                url = "https://" + V

                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.0.0'}) as response:
                            text = await response.read()
                            text = text.decode('utf-8')
                            text = text.split("title>")[1].split("<")[0]
                            name = f'{str(i + 1).zfill(3)}) {text[:60]}'
                            Show = f"❊⟱ Downloading ⟱❊ »\n\n📝 Name » `{name}`\n⌨ Quality » {res}\n\n**🔗 URL »** `{url}`"
                            prog = await m.reply_text(Show)
                            cc = f'**[ 🎥 ] Vid_ID:** {str(i + 1).zfill(3)}. **{raw_text0}{MR}.mkv\n✉️ Batch » **{raw_text0}**'
                            try:
                                await helper.download_video(url, cmd, name)
                                filename = f'{name}.mp4'
                                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                            except Exception as e:
                                await m.reply_text(f"⌘ Downloading interrupted\n{str(e)}\n⌘ Name » {name}\n⌘ Link » `{url}`")
                            await prog.delete(True)
                else:
                     Show = f"❊⟱ Downloading ⟱❊ »\n\n📝 Name » `{name}`\n⌨ Quality » {res}\n\n**🔗 URL »** `{url}`"
                     prog = await m.reply_text(Show)
                     cc = f'**[ 🎥 ] Vid_ID:** {str(i + 1).zfill(3)}. **{raw_text0}{MR}.mkv\n✉️ Batch » **{raw_text0}**'
                     try:
                         await helper.download_video(url, cmd, name)
                         filename = f'{name}.mp4'
                         await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                     except Exception as e:
                         await m.reply_text(f"⌘ Downloading interrupted\n{str(e)}\n⌘ Name » {name}\n⌘ Link » `{url}`")
                    await prog.delete(True)
    
    # Continue to the next link in the loop
                continue

# After all the links are processed
await m.reply_text("✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞")

print("""
█░█░█ █▀█ █▀█ █▀▄ █▀▀ █▀█ ▄▀█ █▀▀ ▀█▀     ▄▀█ █▀ █░█ █░█ ▀█▀ █▀█ █▀ █░█   ░ █▀▀
▀▄▀▄▀ █▄█ █▄█ █▄▀ █▄▄ █▀▄ █▀█ █▀░ ░█░     █▀█ ▄█ █▀█ █▄█ ░█░ █▄█ ▄█ █▀█   ▄ █▄█""")
print("""✅ 𝐃𝐞𝐩𝐥𝐨𝐲 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅""")
print("""✅ 𝐁𝐨𝐭 𝐖𝐨𝐫𝐤𝐢𝐧𝐠 ✅""")

bot.run()
if __name__ == "__main__":
    asyncio.run(main())
