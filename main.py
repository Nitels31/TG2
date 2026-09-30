import log  # Активує перехоплення та налаштування логів

from telebot import *
from telebot import types
from random import *
from google import genai
from dotenv import load_dotenv
import os
import func

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

print("start")

ROOT = os.path.dirname(os.path.abspath(__file__))

dd = set()
dd2 = set()
nic = 0  # Нічия
per = 0  # Перемогли
pro = 0  # Програли

bot = TeleBot(TELEGRAM_TOKEN)
ger = genai.Client(api_key=GEMINI_KEY)

meme_image = os.path.join(ROOT, r"Assets/picture/173meme.jpg")
meme_image_2 = os.path.join(ROOT, r"Assets/picture/uno.png")
scp_173_image = os.path.join(ROOT, r"Assets/picture/173.jpg")
paper_image = os.path.join(ROOT, r"Assets/picture/paper.jpg")
scissors_image = os.path.join(ROOT, r"Assets/picture/scissors.jpg")
music_file = os.path.join(ROOT, r"Assets/music/sinkingship_5.ogg")
backrooms_gif = os.path.join(ROOT, r"Assets/gif/backrooms-crab.gif")
scp_sl_link = "https://store.steampowered.com/app/700330/SCP_Secret_Laboratory/"
scp_cb_link = "https://store.steampowered.com/app/2178380/SCP__Containment_Breach/"

@bot.message_handler(commands=["start"])
def start(message):
    k = types.InlineKeyboardMarkup()
    k1 = types.InlineKeyboardButton(text="mem", callback_data="mem")
    k.add(k1)
    k2 = types.InlineKeyboardButton(text="audio", callback_data="audio")
    k.add(k2)
    k3 = types.InlineKeyboardButton(text="SCP: SL", callback_data="game")
    k.add(k3)
    k4 = types.InlineKeyboardButton(text="Увімкнути ШІ", callback_data="gem")
    k.add(k4)
    k5 = types.InlineKeyboardButton(text="Вимкнути ШІ", callback_data="gemoff")
    k.add(k5)
    bot.send_message(
        message.chat.id,
        "Привіт! Це альфа версія!",
        reply_markup=k,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "mem":
        bot.send_photo(
            call.message.chat.id,
            open(meme_image, "rb")
        )
    elif call.data == "audio":
        bot.send_audio(
            call.message.chat.id,
            open(music_file, "rb")
        )
    elif call.data == "game":
        bot.send_message(
            call.message.chat.id,
            scp_sl_link,
        )
    elif call.data == "gem":
        dd2.discard(call.from_user.id)
        dd.add(call.from_user.id)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Геміні увімкнено!")
    elif call.data == "gemoff":
        dd2.add(call.from_user.id)
        dd.discard(call.from_user.id)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Геміні вимкнено!")


# @bot.message_handler(commands=["SCP"])
# def lol(message):
#     bot.send_message(message.chat.id,"Lol! Ще немає статі по SCP!")
@bot.message_handler(commands=["Привіт"])
def hello(message):
    bot.send_message(message.chat.id, "Привіт!")


@bot.message_handler(commands=["Cправи?"])
def spr(message):
    bot.send_message(message.chat.id, "Гарно, а в тебе?")


@bot.message_handler(commands=["Гарно!"])
def spr1(message):
    bot.send_message(message.chat.id, "Це круто!")


@bot.message_handler(content_types=["photo"])
def photo1(message):
    bot.send_message(message.chat.id, "Фотки не принімаю!")


tim = False


@bot.message_handler(content_types=["audio"])
def audio(message):
    bot.send_message(
        message.chat.id,
        "Хочеш прикол? А він тебе не хоче! Ладно я також аудіо не приймаю!",
    )


@bot.message_handler(content_types=["text"])
def text(message):
    if message.from_user.id in dd:
        try:
            res = ger.models.generate_content(
                model="gemini-3.6-flash", contents=message.text
            )
            bot.reply_to(message, res.text)
        except Exception as e:
            bot.reply_to(message, "Вибачте, сталася помилка при генерації відповіді.")
            print(f"Error: {e}")
    elif message.from_user.id in dd2:
        dd2.discard(message.from_user.id)
        dd.discard(message.from_user.id)
        bot.reply_to(message, "Геміні вимкнено!")
        return
    global nic, per, pro, tme
    t = types.ReplyKeyboardMarkup(resize_keyboard=True)
    t1 = types.KeyboardButton("Гіфка")
    t2 = types.KeyboardButton("Факт")
    t.add(t1, t2)
    t3 = types.KeyboardButton("SCP: SL")
    t4 = types.KeyboardButton("SCP: CB")
    t.add(t3, t4)
    t5 = types.KeyboardButton("Зіграти у камень-ножицуі папір")
    t.add(t5)

    user_msg = message.text.lower().strip()
    if "привіт" in user_msg:
        bot.send_message(message.chat.id, "Привіт? Але чому ти це написав без /? А?!")
    elif "що робиш?" in user_msg:
        r = randint(1, 5)
        if r == 1:
            bot.send_message(message.chat.id, "Тобі відповідаю", reply_markup=t)
        elif r == 2:
            bot.send_message(message.chat.id, "На базі MEG відпочиваю", reply_markup=t)
        elif r == 3:
            bot.send_message(message.chat.id, "Про 3008 читаю, а що?", reply_markup=t)
        elif r == 4:
            bot.send_message(message.chat.id, "Мигдалеву воду собираю", reply_markup=t)
        elif r == 5:
            bot.send_message(message.chat.id, "Нічого", reply_markup=t)
    elif "StickWar" in user_msg:
        bot.send_message(
            message.chat.id,
            "Order Empire!"
        )
    elif "да" in user_msg:
        bot.send_message(
            message.chat.id,
            "нет"
        )
    elif "scp: sl" in user_msg:
        bot.send_message(
            message.chat.id,
            scp_sl_link,
        )
    elif "31" in user_msg:
        bot.send_message(
            message.chat.id,
            "Windy31!",
        )
    elif "день" in user_msg:
        bot.send_message(
            message.chat.id,
            func.day(),
        )
    elif "бажання" in user_msg:
        bot.send_message(
            message.chat.id,
            func.generate_wish(),
        )
    elif "анекдот" in user_msg:
        bot.send_message(
            message.chat.id,
            func.generate_joke(),
        )
    elif "roll" in user_msg or "dice" in user_msg:
        bot.send_message(
            message.chat.id,
            f"Випало число: {func.roll_dice()}",
        )
    elif "flip" in user_msg or "coin" in user_msg:
        bot.send_message(
            message.chat.id,
            f"Випало: {'Орел' if func.flip_coin() == 1 else 'Решка'}",
        )
    elif "password" in user_msg:
        bot.send_message(
            message.chat.id,
            f"Згенерований пароль: {func.generate_password()}",
        )
    elif "scp: cb" in user_msg:
        bot.send_message(
            message.chat.id,
            scp_cb_link,
        )
    elif "зрозуміло" in user_msg:
        bot.send_message(
            message.chat.id,
            "Мені також!"
        )
    elif "пока" in user_msg:
        bot.send_message(
            message.chat.id,
            "ТИ поняв що легше на сайт глянути?"
        )
    elif "ну дай глянути scp" in user_msg or "давай scp" in user_msg:
        bot.send_message(
            message.chat.id,
            "Тебе Alpha-1 знайде"
        )
    elif "у мене карта рівня 4" in user_msg:
        bot.send_message(
            message.chat.id,
            "Скинь 682 тоді"
        )
    elif "я дешка" in user_msg:
        bot.send_message(
            message.chat.id,
            "Хто тобі телефон дав?"
        )
    elif "хочеш 096 покажу" in user_msg:
        bot.send_message(
            message.chat.id,
            "Сам подивися"
        )
    elif (
        "хочеш 79 покажу" in user_msg
    ):
        bot.send_message(message.chat.id, "Нє")
    elif (
        "хочеш 939 покажу" in user_msg
        or "хочеш 939 покажу" in user_msg
    ):
        bot.send_message(
            message.chat.id,
            "Нє Нє Нє!"
        )
    elif "хочеш 001 покажу" in user_msg or "хочеш 001 покажу?" in user_msg:
        bot.send_message(message.chat.id, "До тебе вже їдуть всі MTF")
    elif ("fpv тобі прилетить" in user_msg or "шахед тобі прилетить" in user_msg):
        bot.send_photo(message.chat.id, open(meme_image_2, "rb"))
    elif "alpha-1" in user_msg:
        bot.send_message(
            message.chat.id, "Що? Я нічого не знаю про них! Зачем ти це питаєш???"
        )
    elif message.text == "28":
        bot.send_message(message.chat.id, "28 ударів ножем! Ти действував навернека!")
    elif "o5" in user_msg:
        bot.send_message(message.chat.id, "Open 5?")
    elif "хаос" in user_msg:
        bot.send_message(message.chat.id, "СI? у них сильна могнева міць у SCP: SL")
    elif "мог" in user_msg:
        bot.send_message(message.chat.id, "MTF? Толпой все знищать!")
#    elif "гок" in user_msg:
#        bot.send_message(
#           message.chat.id, "GOK? Я не знаю що це бо я за них у SL ніколи не грав!"
#        )
    elif "scp" in user_msg:
        bot.send_message(
            message.chat.id,
            "SCP? Я не знаю як за них грати. Я за них ніколи не грав у SL попри свої 14.5 години у цю гру!",
        )
    elif "o5-1" in user_msg or "o5-1?" in user_msg:
        bot.send_message(
            message.chat.id, "А це ще що? Опен 5-1? Нова камера? Об*єктив?"
        )
    elif "твої досягнення" in user_msg:
        bot.send_message(
            message.chat.id,
            "1) Про розмову\nЯк Повстанець Хаосу, використовуйте радіо для зв'язку з МОГ",
        )
        bot.send_message(
            message.chat.id, "2) Майстер втечі\nУтечіть з лабораторії за три хвилини."
        )
        bot.send_message(
            message.chat.id,
            "3) Хтось завжди лишається, браття!\nУтечіть персоналом класу D.",
        )
        bot.send_message(
            message.chat.id,
            "4) ... Ви думаєте про те ж, що і я?\nЗнайдіть зброю, граючи за персонал класу D.",
        )
        bot.send_message(
            message.chat.id,
            "5) Зворотний відлік: 90 секунд...\nПереживіть вибух боєголовки «Альфа».",
        )
        bot.send_message(
            message.chat.id, "6) Ларі - ваш друг!\nУтечіть із кишенькового виміру."
        )
        bot.send_message(
            message.chat.id,
            "7) Дружба\nЯк науковець успішно поліпште свою картку доступу поблизу персоналу класу D.",
        )
        bot.send_message(
            message.chat.id, "8) Надсила!\nЗнайдіть картку доступу рівня 05."
        )
        bot.send_message(
            message.chat.id,
            "9)Це ваш перший раз?\nДозвольте SCP-173 вхопити вас за шию.",
        )
        bot.send_message(
            message.chat.id, "10) ХАО-О-ОК!\nВідродіться як повстанець хаосу."
        )
        bot.send_message(
            message.chat.id,
            "11) Озброюємося, хлопці!\nВідродіться як член загону «Дев'ятихвостої лисиці».",
        )
    elif (
        "ти просто код! Ти ніхто!" in user_msg
        or "ти гівно!" in user_msg
        or "Ти нікому не треба!" in user_msg
    ):
        bot.send_message(message.chat.id, "І що?")
    elif message.text == "Гіфка":
        bot.send_document(message.chat.id, open(backrooms_gif, "rb"))
    elif message.text == "Зіграти у камень-ножицуі папір":
        gra = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kamini = types.KeyboardButton("Камінь")
        nosichi = types.KeyboardButton("Ножиці")
        papirr = types.KeyboardButton("Папір")
        gra.add(kamini, nosichi, papirr)
        bot.send_message(
            message.chat.id, "А тепер ви оберіть дію! Я підожду!", reply_markup=gra
        )
    elif "камінь" in user_msg:
        bot.send_message(message.chat.id, "Ви обрали камінь!")
        bot.send_photo(message.chat.id, open(scp_173_image, "rb"))
        bo = randint(1, 3)
        if bo == 1:
            nic += 1
            bot.send_message(message.chat.id, "Бот обрав камінь!")
            bot.send_photo(message.chat.id, open(scp_173_image, "rb"))
            bot.send_message(message.chat.id, "Нічия" + str(nic) + "раз!")
        elif bo == 2:
            per += 1
            bot.send_message(message.chat.id, "Бот обрав ножиці!")
            bot.send_photo(
                message.chat.id, open(scissors_image, "rb")
            )  # 4К - ми це не потягнемо!
            bot.send_message(message.chat.id, "Ви перемогли!" + str(per) + "раз!")
        elif bo == 3:
            pro += 1
            bot.send_message(message.chat.id, "Бот обрав папір!")
            bot.send_photo(message.chat.id, open(paper_image, "rb"))
            bot.send_message(message.chat.id, "Ви програли!" + str(pro) + "раз!")
    elif "ножиці" in user_msg:
        bot.send_message(message.chat.id, "Ви обрали ножиці!")
        bot.send_photo(message.chat.id, open(scissors_image, "rb"))
        bo = randint(1, 3)
        if bo == 1:
            pro += 1
            bot.send_message(message.chat.id, "Бот обрав камінь!")
            bot.send_photo(message.chat.id, open(scp_173_image, "rb"))
            bot.send_message(message.chat.id, "Ви програли!" + str(pro) + "раз!")
        elif bo == 2:
            nic += 1
            bot.send_message(message.chat.id, "Бот обрав ножиці!")
            bot.send_photo(
                message.chat.id, open(scissors_image, "rb")
            )  # 4К - ми це не потягнемо!
            bot.send_message(message.chat.id, "Нічія!" + str(nic) + "раз!")
        elif bo == 3:
            per += 1
            bot.send_message(
                message.chat.id,
                f"Бот обрав папір! {per} раз!")
            bot.send_photo(message.chat.id, open(paper_image, "rb"))
            bot.send_message(message.chat.id, "Ви перемогли!")
    elif "папір" in user_msg:
        bot.send_message(
            message.chat.id,
            "Ви обрали папір!"
        )
        bot.send_photo(
            message.chat.id,
            open(paper_image, "rb")
        )
        bo = randint(1, 3)
        if bo == 1:
            per += 1
            bot.send_message(
                message.chat.id,
                "Бот обрав камінь!"
            )
            bot.send_photo(
                message.chat.id,
                open(scp_173_image, "rb")
            )
            bot.send_message(
                message.chat.id,
                "Ви перемогли!" + str(per) + "раз!"
            )
        elif bo == 2:
            pro += 1
            bot.send_message(
                message.chat.id,
                "Бот обрав ножиці!"
            )
            bot.send_photo(
                message.chat.id,
                open(scissors_image, "rb")
            )  # 4К - ми це не потягнемо!
            bot.send_message(
                message.chat.id,
                "Ви програли" + str(pro) + "раз!"
            )
        elif bo == 3:
            nic += 1
            bot.send_message(
                message.chat.id,
                "Бот обрав папір!"
            )
            bot.send_photo(
                message.chat.id,
                open(paper_image, "rb")
            )
            bot.send_message(
                message.chat.id,
                "Нічія!" + str(nic) + "раз!"
            )
    elif message.text == "Факт":
        f = randint(1, 7)
        if f == 1:
            bot.send_message(
                message.chat.id,
                "якщо ви бачите 173 то не кліпайте очима. А якщо ви це зробите то буде не приємний масаж шиї",
            )
        elif f == 2:
            bot.send_message(
                message.chat.id,
                "106 - садист"
            )
        elif f == 3:
            bot.send_message(
                message.chat.id,
                "173 називають печенкою/печиво; статуя"
            )
        elif f == 4:
            bot.send_message(
                message.chat.id,
                "SCP-500 - таблетки що лічуть все"
            )
        elif f == 5:
            bot.send_message(
                message.chat.id,
                "914 - машина що має режими: дуже грубо, грубо, 1:1, тонко, дуже тонко"
            )
        elif f == 6:
            bot.send_message(
                message.chat.id,
                "049 або чумний доктор одним доторком убиває"
            )
        elif f == 7:
            bot.send_message(
                message.chat.id,
                "А я що? А я нічого!")
    else:
        re = randint(1, 6)
        if re == 1:
            bot.send_message(
            message.chat.id,
            "Я тебе не понімать!")
        elif re == 2:
            bot.send_message(
                message.chat.id,
                "Хм... Я закодований! І за цього я не зрозумів що ти прислав!",
            )
        elif re == 3:
            bot.send_message(
                message.chat.id,
                "Пришли інше!")
        elif re == 4:
            bot.send_message(
                message.chat.id,
                "Nu-7 це армія фонду! Але пришли мені інше!"
            )
        elif re == 5:
            bot.send_message(
                message.chat.id,
                "Я цього не розумію! Як і фотографії!")
        elif re == 6:
            bot.send_message(
                message.chat.id,
                "28 ударів ножем! Ти действував навернека!"
            )

if __name__ == "__main__":
    bot.polling(none_stop=True)
