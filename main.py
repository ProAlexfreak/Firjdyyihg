
import os
from html import escape
from urllib.parse import urlparse

from pyrogram import Client, filters
from pyrogram.enums import ParseMode

app = Client(
    "format_bot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

users = {}


def valid_link(link):
    try:
        parsed = urlparse(link.strip())
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
    except Exception:
        return False


@app.on_message(filters.private & filters.command("format"))
async def start_format(client, message):
    users[message.from_user.id] = {
        "step": "preview"
    }

    await message.reply_text(
        "Send Preview Link 🔗"
    )


@app.on_message(
    filters.private & filters.text & ~filters.command("format")
)
async def receive_links(client, message):
    user_id = message.from_user.id

    if user_id not in users:
        return

    link = message.text.strip()

    if not valid_link(link):
        await message.reply_text(
            "❌ Please send a valid HTTP/HTTPS link."
        )
        return

    data = users[user_id]

    if data["step"] == "preview":
        data["preview"] = link
        data["step"] = "main"

        await message.reply_text(
            "Send Main Link 🔗"
        )
        return

    if data["step"] == "main":
        preview = escape(data["preview"], quote=True)
        main = escape(link, quote=True)

        post = (
            "POSTT\n\n"

            f'<a href="{preview}">'
            "𝘾𝙇𝙄𝘾𝙆 𝙃𝙀𝙍𝙀 𝙁𝙊𝙍 𝙋𝙍𝙀𝙑𝙄𝙀𝙒 🔗⁠"
            "</a>\n"

            f'<a href="{preview}">'
            "𝘾𝙇𝙄𝘾𝙆 𝙃𝙀𝙍𝙀 𝙁𝙊𝙍 𝙋𝙍𝙀𝙑𝙄𝙀𝙒🔗⁠"
            "</a>\n\n"

            "𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗛𝗘𝗥𝗘 𝗢𝗡𝗟𝗬 "
            "𝗙𝗢𝗥 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗨𝗦𝗘𝗥 ⤵️\n"

            f'<blockquote><i><a href="{main}">'
            "Second link here"
            "</a></i></blockquote>\n\n"

            "𝙏𝙝𝙚 𝙉𝙚𝙬 𝙒𝙤𝙧𝙡𝙙"
        )

        await message.reply_text(
            post,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

        del users[user_id]


app.run()
