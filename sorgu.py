import telebot
import time
import sqlite3
import pyfiglet
import os
import time
import requests
import random
import hashlib
import instaloader
import string
import whois
import validators
from telebot import types
import qrcode
from io import BytesIO
from urllib.parse import quote_plus
import sys
from datetime import datetime
import threading


token='7247166229:AAHtgJ1b-auWmhP8DizT_iiD4TTgIZPD_WQ'

bot = telebot.TeleBot(token)

print("yeni Bot Calisiyor")



conn = sqlite3.connect("ip.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ip (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        ip TEXT
    )
''')
conn.commit()

conn = sqlite3.connect("pre.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER
    )
''')
conn.commit()   


conn = sqlite3.connect("phone.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS phone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        phone TEXT
    )
''')
conn.commit()


conn = sqlite3.connect("ban.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ban (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT
    )
''')
conn.commit()


conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT
    )
''')
conn.commit()

admins={7067213241}


"""
def toplu_mesaj_gonder(mesaj):
    with open('users.txt', mode='r') as file:
        for user_id in file:
            user_id = user_id.strip()
            bot.send_message(user_id, f"{mesaj}")
"""

def toplu_mesaj_gonder(mesaj):
    user_id=()
    for user in user_id:
        print(user)
        bot.send_message(user, f"{mesaj}")

def get_pre_info(user_id):
    conn = sqlite3.connect("pre.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pre WHERE user_id=?", (user_id,))
    return cursor.fetchone()

def get_ban_info(user_id):
    conn = sqlite3.connect("ban.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ban WHERE user_id=?", (user_id,))
    return cursor.fetchone()

def add_ban(user_id):
    conn = sqlite3.connect("ban.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ban (user_id) VALUES (?)', (user_id,))
    conn.commit()

@bot.message_handler(commands=['ban'])
def ban(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    
    if user_id not in admins:
        bot.send_message(user_id, "Admin Değilsin Bu Kodu Çalıştırma Yetkin Yok")
        return
    
    try:
        ban_info = message.text.split(maxsplit=1)[1].strip()
        if not ban_info:
            bot.reply_to(message, "Lütfen bir kullanıcı kimliği giriniz. Kullanım: /ban <user_id>")
            return
        if ban_info in admins:
            bot.reply_to(message, "Hey Başka Bir Admini Banlayamazsın")
            return
    except IndexError:
        bot.reply_to(message, "Lütfen bir mesaj giriniz. Kullanım: /ban <user_id>")
        return
    add_ban(user_id=ban_info)
    bot.reply_to(message,f"{ban_info} idli Kullanıcı Banlandı")
    ban_mes=(
                f"╭─━━━━━━━━━━━━━─╮\n"
                f"Botan Banlanmışsınız\n"
                f"Kullanıcı Bilgileri\n"
                f"Kullanıcı Adı: {user_name}\n"
                f"Kullanıcı ID: {user_id}\n"
                f"Botan Banınızın Kalkmasını İstiyorsanız /desteğe Yazın\n"
                f"╰─━━━━━━━━━━━━━─╯"

            )
    bot.send_message(ban_info,f"{ban_mes}")



@bot.message_handler(commands=['unban'])
def unban(message):
    user_id = message.from_user.id
    if user_id not in admins:
        bot.send_message(user_id, "Admin Değilsin Bu Kodu Çalıştırma Yetkin Yok")
        return

    try:
        unban_id = message.text.split()[1]
        if not unban_id:
            bot.reply_to(message, "Lütfen Bir İD Giriniz")
            return 

        conn = sqlite3.connect("ban.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ban WHERE user_id = ?", (unban_id,))
        conn.commit()  # Veritabanını güncelle ve değişiklikleri kaydet
        bot.reply_to(message, f"{unban_id} IdLi Kullanıcının Banı Kaldırıldı")


        unban_mes = (
            f"╭─━━━━━━━━━━━━━─╮\n"
            f"|Botan Banınız Kaldırıldı Botu Özgürce Kullanabilirsin\n"
            f"|Kullanıcı Bilgileri\n"
            f"|Kullanıcı ID: {unban_id}\n"
            f"╰─━━━━━━━━━━━━━─╯"
        )
        bot.send_message(unban_id, unban_mes)
    except Exception as e:
        bot.reply_to(message, f"Hata Meydana Geldi\n\n{e}")
    


@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    if user_id not in admins:
        bot.send_message(user_id,"Admin Degilsin Bu Kodu Çliştırma Yetkın Yok")
        return
    else:
        admin_count = len(admins)
        adminss_kom=(
            f"Admin Menüsüne Hoş Geldin\n\n"
            f"Toplam Admin Sayısı {admin_count}\n"
            f"-> Admin Bilgileri\n"
            f"Admin  Adı: {user_name}\n"
            f"Admin İd: {user_id}\n\n"
            f"Admin Komutları \n\n"
            f"/topmsj Herkese Toplu Mesaj Gönderir\n"
            f"/ban Kulanıcıyı Banlar\n"
            f"/unban Kullanıcın Banını Kaldırır"
        )
        bot.send_message(user_id,adminss_kom)




def is_user_in_channel(chat_id, channel_username):
    try:
        member = bot.get_chat_member(channel_username, chat_id)
        return member.status != "left"
    except telebot.apihelper.ApiException:
        return False

#start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    channel_username1 = '@jetcheck2'
    channel_username2 = '@jetcheck1' 
    if not is_user_in_channel(user_id, channel_username1) or not is_user_in_channel(user_id, channel_username2):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(0.1)
            bot.send_message(user_id, text="Üzgünüm, @jetcheck2 ve @jetcheck1 gruplarına katılmak zorunludur!")
            return
    ban_info=get_ban_info(user_id)
    if ban_info:
        ban_mes=(
                f"╭─━━━━━━━━━━━━━─╮\n"
                f"|Botan Banlanmışsınız\n\n"
                f"|Kullanıcı Bilgileri\n\n"
                f"|Kullanıcı Adı: {user_name}\n"
                f"|Kullanıcı ID: {user_id}\n\n"
                f"|Botan Banınızın Kalkmasını İstiyorsanız /desteğe Yaz\n"
                f"╰─━━━━━━━━━━━━━─╯"
            )
        bot.send_message(user_id,ban_mes)
        return
    chat_id=7067213241
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        pass
    else:
        try:
            cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, user_name))
            conn.commit()
            bot.send_message(chat_id,f"`Yeni Kulanıcı`\n`Toplam Kulanıcı Sayısı {total_users}`\n\n`User_id`: {user_id}\n`User_name`: @{user_name}" ,parse_mode="Markdown")
        except Exception as e:
            bot.send_message(user_id, f"Hata: {e}")

    bot.send_photo(user_id, open('logo.jpg', 'rb'), caption=f"{user_name} (`{user_id}`) Bota Hoşgeldin İyi Eğlenceler\n\n Komutlar için /komutlar  ", parse_mode="Markdown")


import sqlite3
from datetime import datetime
import time
import threading

def get_db_connection():
    """Her thread için yeni bir database bağlantısı oluştur"""
    conn = sqlite3.connect("users.db")
    return conn

@bot.message_handler(commands=['topmsj'])
def handle_topmsj_command(message):
    # Check if sender is admin
    if message.from_user.id not in admins:
        bot.reply_to(message, "Bu komutu kullanma yetkiniz yok!")
        return
    
    # Get the message content after the command
    try:
        broadcast_message = message.text.split(' ', 1)[1]
    except IndexError:
        bot.reply_to(message, "Lütfen gönderilecek mesajı yazın.\nÖrnek: /topmsj Merhaba!")
        return
    
    # Thread-safe database operations
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get users from database and send message
        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()
        total_users = len(users)
        
        # Send initial status message
        status_msg = bot.reply_to(message, f"Toplu mesaj gönderimi başlıyor...\nToplam kullanıcı sayısı: {total_users}")
        
        success_count = 0
        fail_count = 0
        
        for index, user in enumerate(users, 1):
            user_id = user[0]
            try:
                bot.send_message(user_id, broadcast_message)
                success_count += 1
                
                # Update status every 10 messages
                if index % 10 == 0:
                    bot.edit_message_text(
                        f"Mesaj gönderimi devam ediyor...\n"
                        f"İşlenen: {index}/{total_users}\n"
                        f"Başarılı: {success_count}\n"
                        f"Başarısız: {fail_count}",
                        message.chat.id,
                        status_msg.message_id
                    )
                
                time.sleep(0.5)  # 500ms delay between messages
                
            except Exception as e:
                fail_count += 1
                print(f"Error sending message to user {user_id}: {e}")
        
        # Send final status message
        bot.edit_message_text(
            f"✅ Toplu mesaj gönderimi tamamlandı!\n\n"
            f"Toplam: {total_users}\n"
            f"Başarılı: {success_count}\n"
            f"Başarısız: {fail_count}",
            message.chat.id,
            status_msg.message_id
        )
    
    finally:
        # Her durumda bağlantıyı kapat
        cursor.close()
        conn.close()

#komutlar
@bot.message_handler(commands=['komutlar'])
def komutlar(message):
    user_id=message.from_user.id
    user_name=message.from_user.username
    channel_username1 = '@jetcheck2'
    channel_username2 = '@jetcheck1' 
    if not is_user_in_channel(user_id, channel_username1) or not is_user_in_channel(user_id, channel_username2):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(0.1)
            bot.send_message(user_id, text="Üzgünüm, @jetcheck2 ve @jetcheck1 gruplarına katılmak zorunludur!", parse_mode="Markdown")
            return
    ban_info=get_ban_info(user_id)
    if ban_info:
        ban_mes=(
                f"╭─━━━━━━━━━━━━━─╮\n"
                f"|Botan Banlanmışsınız\n\n"
                f"|Kullanıcı Bilgileri\n\n"
                f"|Kullanıcı Adı: {user_name}\n"
                f"|Kullanıcı ID: {user_id}\n\n"
                f"|Botan Banınızın Kalkmasını İstiyorsanız /desteğe Yaz\n"
                f"╰─━━━━━━━━━━━━━─╯"
            )
        bot.send_message(user_id,ban_mes)
        return
    komutlar = (
    "``` RodyPanel'e Hoş Geldin\n\n"
    "𝖉𝖊𝖘𝖙𝖊𝖐\n\n"
    "🆘 /destek - destek talebi oluşturur\n\n"
    "𝕾𝖔𝖗𝖌𝖚\n\n"
    "🔍/sorgu - ad soyad il ilçceden kişi bilgisi veriri\n"
    "🔍/apartman - tc den adres bilgisi verir\n"
    "🔍/adres - tc den adres bilgisi\n"
    "🔍/tckn - tc den bilgi verir\n"
    "🔍/gsmtc - gsm den tc veriri\n"
    "🔍/tcgsm - tc den gsm verir\n"
    "🔍/aile - tc den aile bilgisi verir\n"
    "🔍/sulale - tc den sulalae Bilgisi verir\n"
    "🔍/penis tc den penis boyu verir\n"
    "🔍/ayak - tcden ayak no veriri\n\n"
    "𝖔𝖘𝖎𝖓𝖙\n\n"
    "🔍 /index - site indexini çeker\n"
    "🔍 /whois - Site Whois Bilgilerini Verir\n\n"
    "𝕰𝖌̆𝖑𝖊𝖓𝖈𝖊 \n\n"      
    "🎨 /figlet - mesajı havalı yapar\n"
    "🌐 /ip - ipden Bilgi verir\n"
    "💳 /cc - random cc üretir\n"
    "📩 /sms - sms bomber atar"
    "📷 /ig - instagram infosu verir\n"
    "📝 /yaz - Girilen mesajı Deftere Yazar\n"
    "🎮 /playkod - random Play Kod üretir\n"
    "🕵️ /fakebilgi - Fake Bilgi Üretir\n"
    "🎮 /pubg - random pubg hesabı üretir\n"
    "🔒 /rot13 - girdiğiniz metini rot13 ile şifreler\n"
    "🔑 /md5 - girdiğiniz metini md5 ile şifreler\n"
    "📋 /qr - Qr Kod Oluştur\n"
    "₿ /coin - Coin Fiyatlarını Verir\n"
    "𝖘𝖔̈𝖟𝖑𝖊𝖘̧𝖒𝖊\n\n"
    "📌 **Rody Panel'in** Tüm Hakları Saklıdır📌\n\n```"
    
    )

    bot.send_message(user_id,komutlar,parse_mode="Markdown")

@bot.message_handler(commands=['sozlesme'])
def figlet(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    channel_username1 = '@jetcheck2'
    channel_username2 = '@jetcheck1' 
    if not is_user_in_channel(user_id, channel_username1) or not is_user_in_channel(user_id, channel_username2):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(0.1)
            bot.send_message(user_id, text="Üzgünüm, @jetcheck2 ve @jetcheck1  katılmak zorunludur!", parse_mode="Markdown")
            return
    ban_info=get_ban_info(user_id)
    if ban_info:
        ban_mes=(
                f"╭─━━━━━━━━━━━━━─╮\n"
                f"|Botan Banlanmışsınız\n\n"
                f"|Kullanıcı Bilgileri\n\n"
                f"|Kullanıcı ID: {user_id}\n\n"
                f"|Botan Banınızın Kalkmasını İstiyorsanız /desteğe Yaz\n"
                f"╰─━━━━━━━━━━━━━─╯"
            )
        bot.send_message(user_id,ban_mes)
        return

    kullanici_sozlesmesi = """
```Duck Kullanıcı Sözleşmesi

Bu kullanıcı sözleşmesi, PinkyPanel Telegram botunu kullanırken geçerli olan şartları ve koşulları belirtir. Lütfen bu sözleşmeyi dikkatlice okuyun ve kabul etmeden önce içeriğini anladığınızdan emin olun.

1. Hizmetlerin Kullanımı: PinkyPanel, Telegram platformu üzerinde sunulan bir bot hizmetidir. Botu kullanarak, bu hizmetin şartlarını ve koşullarını kabul etmiş sayılırsınız.

2. Kullanım Şartları: Botu kullanırken aşağıdaki şartlara uymayı kabul edersiniz:
   - Botu yalnızca yasal amaçlarla kullanacaksınız.
   - Botu diğer kullanıcıları rahatsız etmek veya zarar vermek için kullanmayacaksınız.
   - Bot üzerinden paylaşılan bilgilerin doğruluğunu ve güvenilirliğini teyit etmekten siz sorumlusunuz.
   - Botu kullanarak gerçekleştirilen tüm işlemler, tamamen sizin sorumluluğunuzdadır.

3. Gizlilik Politikası: Duck tarafından toplanan kullanıcı verileri, gizlilik politikasına uygun olarak işlenir ve saklanır. Bu konuda daha fazla bilgi almak için gizlilik politikamızı inceleyebilirsiniz.

4. Sorumluluk Sınırlamaları: PinkyPanel hizmetleriyle ilgili olarak, oluşabilecek herhangi bir zarardan dolayı sorumluluk kabul etmez. Botun kullanımı tamamen kendi riskinizdedir.

5. Değişiklikler: Bu kullanıcı sözleşmesi zaman zaman güncellenebilir. Güncellemeler hakkında sizi bilgilendirmek için elimizden geleni yapacağız.

Bu kullanıcı sözleşmesini kabul etmek için botu kullanmaya devam etmeniz yeterlidir. Bu sözleşmeyi kabul etmiyorsanız, lütfen botu kullanmayı durdurun.

Yapılan İşlemler ve Kullanıcı Sorumluluğu: Botu kullanarak gerçekleştirilen tüm işlemler, kullanıcının kendi sorumluluğundadır. Duck ve sahipleri, bu işlemlerden kaynaklanabilecek herhangi bir zarardan sorumlu tutulamazlar.

Not: Start ve Sözleşme Komutları hariç Diğer Komutları Kullanrak Sözleşmeyi Kabul Etmiş Olursunuz```
"""


    bot.send_message(user_id,kullanici_sozlesmesi,parse_mode="Markdown")

#destek
@bot.message_handler(commands=["destek"])
def destek(message):
    id=-1002200729940
    user_id = message.from_user.id
    user_name = message.from_user.username
    channel_username1 = '@jetcheck1'
    channel_username2 = '@jetcheck2'
    if not is_user_in_channel(user_id, channel_username1) or not is_user_in_channel(user_id, channel_username2):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(0.1)
            bot.send_message(user_id, text="Üzgünüm, @jetcheck2 ve @jetcheck1 gruplarına katılmak zorunludur!", parse_mode="Markdown")
            return
    mesaj = message.text.split(maxsplit=1)
    if mesaj is None:
        bot.reply_to(message,f"Lütfen Bir Mesaj Giriniz")
        return
    if len(mesaj) > 1:
        mesaj = mesaj[1]
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.1)
        bot.send_message(id, f"*Destek Talebi Var!\n\nMesaj:* `{mesaj}`\n\n*Kullanıcı: @{user_name}*\n*Kullanıcı ID:* `{user_id}`", parse_mode="Markdown")
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.1)
        bot.reply_to(message, "*Destek talebiniz alındı. En kısa sürede size dönüş yapılacaktır*.", parse_mode="Markdown")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.1)
        bot.reply_to(message, "⚠️ *Lütfen geçerli bir destek mesajı girin.*\n\n*Örnek:* `/destek Merhaba, yardıma ihtiyacım var gibi`.", parse_mode="Markdown")

#figlet
@bot.message_handler(commands=['figlet'])
def figlet(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    channel_username1 = '@jetcheck2'
    channel_username2 = '@jetcheck1' 
    if not is_user_in_channel(user_id, channel_username1) or not is_user_in_channel(user_id, channel_username2):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(0.1)
            bot.send_message(user_id, text="Üzgünüm, @jetcheck2 ve @jetcheck1 gruplarına katılmak zorunludur!", parse_mode="Markdown")
            return
    ban_info=get_ban_info(user_id)
    if ban_info:
        ban_mes=(
                f"╭─━━━━━━━━━━━━━─╮\n"
                f"|Botan Banlanmışsınız\n\n"
                f"|Kullanıcı Bilgileri\n\n"
                f"|Kullanıcı Adı: {user_name}\n"
                f"|Kullanıcı ID: {user_id}\n\n"
                f"|Botan Banınızın Kalkmasını İstiyorsanız /desteğe Yaz\n"
                f"╰─━━━━━━━━━━━━━─╯"
            )
        bot.send_message(user_id,ban_mes)
        return
    text = message.text.split(maxsplit=1)[1].strip()
    
    if not text:
        bot.reply_to(message, "Lütfen bir mesaj giriniz.\n\nÖrnek: /figlet (mesaj)")
        return
    
    figlet_text = pyfiglet.figlet_format(text)
    with open("figlet.txt", mode='w') as figlet_file:
        figlet_file.write(figlet_text)
    
    with open("figlet.txt", mode='rb') as file_content:
        bot.send_document(user_id, file_content, caption=f"Bilgilerin Dosya İçinde: {user_name}", reply_to_message_id=message.message_id)

    os.remove('figlet.txt')

last_call_times = {}

@bot.message_handler(commands=['call'])
def call(message):
    user_id = message.from_user.id
    
    # Kullanıcının son arama zamanını kontrol edin
    last_call_time = last_call_times.get(user_id)
    if last_call_time is not None and time.time() - last_call_time < 300:
        # Son aramadan bu yana 5 dakikadan az bir süre geçti
        bot.reply_to(message, "Lütfen 5 dakika bekleyin ve tekrar deneyin.")
        return

    user_name = message.from_user.username
    channel_username1 = '@jetcheck2'
    channel_username2 = '@jetcheck1' 
    if not is_user_in_channel(user_id, channel_username1) or not is_user_in_channel(user_id, channel_username2):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(0.1)
            bot.send_message(user_id, text="Üzgünüm, @jetcheck2 ve @jetcheck1 gruplarına katılmak zorunludur!", parse_mode="Markdown")
            return
    ban_info=get_ban_info(user_id)
    if ban_info:
        ban_mes=(
                f"╭─━━━━━━━━━━━━━─╮\n"
                f"|Bo
