import random
import string
import discord
import os
my_secret = os.environ['TOKEN']

# Bot ayarları
ayarlar = {
    "on_taki": "$",  # Ön takı (prefix)
    "TOKEN": "Tokeni Buraya Koy"  # Bot tokenini buraya ekleyin
}

# Şifre oluşturucu
def sifre_olusturucu(sifre_uzunlugu):
    ogeler = string.ascii_letters + string.digits + "+-/*!&$#?=@<>"
    return ''.join(random.choice(ogeler) for _ in range(sifre_uzunlugu))

# Emoji oluşturucu
def emoji_olusturucu():
    emoji = ["😀", "🙂", "😂", "🤣", "😎", "😇", "😍", "🥳", "😡", "🤯"]
    return random.choice(emoji)

# Yazı tura
def yazi_tura():
    return random.choice(["YAZI", "TURA"])

# Sayı tahmin oyunu
def sayi_tahmin_oyunu(tahmin, gercek):
    if tahmin == gercek:
        return "Doğru bildiniz! 🎉"
    elif tahmin < gercek:
        return "Daha büyük bir sayı deneyin!"
    else:
        return "Daha küçük bir sayı deneyin!"

# Bot intents ayarları
ayricaliklar = discord.Intents.default()
ayricaliklar.message_content = True
istemci = discord.Client(intents=ayricaliklar)

# Tahmin oyunu için rastgele sayı
tahmin_edilecek_sayi = random.randint(1, 100)

# Bot hazır olduğunda
@istemci.event
async def on_ready():
    print(f'{istemci.user} olarak giriş yaptık!')

# Bot mesaj aldığında
@istemci.event
async def on_message(message):
    global tahmin_edilecek_sayi

    if message.author == istemci.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Merhaba! Ben sizin akıllı botunuzum! 🤖')
    
    elif message.content.startswith('$smile'):
        await message.channel.send(emoji_olusturucu())

    elif message.content.startswith('$coin'):
        await message.channel.send(yazi_tura())

    elif message.content.startswith('$pass'):
        await message.channel.send(sifre_olusturucu(12))

    elif message.content.startswith('$guess'):
        try:
            tahmin = int(message.content.split()[1])
            cevap = sayi_tahmin_oyunu(tahmin, tahmin_edilecek_sayi)
            await message.channel.send(cevap)
            if cevap == "Doğru bildiniz! 🎉":
                tahmin_edilecek_sayi = random.randint(1, 100)
        except (ValueError, IndexError):
            await message.channel.send("Lütfen bir sayı girin: `$guess [sayı]`")

    elif message.content.startswith('$help'):
        await message.channel.send('Komutlar:\n'
                               '$hello - Merhaba! Ben sizin akıllı botunuzum!\n'
                               '$smile - Emoji oluşturur.\n'
                               '$coin - Yazı tura atar.\n'
                               '$pass - Şifre oluşturur.\n'
                               '$help - Bu mesajı gösterir.\n'
                               '$guess [sayı] - Tahmin oyunu oynar.')
    else:
        await message.channel.send("Bu komutu anlayamadım. 😔 Lütfen `$help` komutunu deneyin.")

istemci.run(ayarlar["TOKEN"])
