import telebot, os, tempfile, re
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ydl_opts = {
    'format': 'best[filesize<45M]/best',
    'quiet': True,
    'noplaylist': True,
    'extractor_args': {'youtube': {'player_client': ['android','web']}},
}

@bot.message_handler(commands=['start','help'])
def start(m):
    bot.send_message(m.chat.id, "Салам! Кидай ссылку на TikTok / Insta / YouTube")

@bot.message_handler(content_types=['text'])
def dl(m):
    url = m.text.strip()
    if "http" not in url: return
    msg = bot.send_message(m.chat.id, "⏳ Качаю...")
    try:
        with tempfile.TemporaryDirectory() as d:
            path = d + "/%(title)s.%(ext)s"
            opts = {**ydl_opts, 'outtmpl': path}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file = ydl.prepare_filename(info)
            bot.send_video(m.chat.id, open(file, 'rb'))
            bot.delete_message(m.chat.id, msg.id)
    except Exception as e:
        print(e)
        bot.edit_message_text(f"🙈 Ошибка: {e}", m.chat.id, msg.id)

bot.infinity_polling()
