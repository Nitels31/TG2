import random as rand
from datetime import datetime
from zoneinfo import ZoneInfo

today_day = datetime.now(ZoneInfo("America/Los_Angeles")).day

wish = [
    'Гарного дня!',
    'Бажаю успіхів!',
    'Нехай щастить!', 
    'Всього найкращого!',
]
joke = [
    "Чому програмісти не люблять природу? Бо там занадто багато bag.",
    "Чому комп'ютери не можуть грати в футбол? Бо вони бояться вірусів.",
    "Знаєш як називається програміст, який не може знайти помилку? Дебагер.",
]

fact = [
    "Сьогодні"
]

def roll_dice():
    roll = rand.randint(1, 6)
    return roll

def flip_coin():
    flip = rand.randint(1, 2)
    return flip

def generate_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password_length = rand.randint(8, 16)
    password = ''.join(rand.choice(characters) for _ in range(password_length))
    return password

def generate_wish():
    gen_wish = rand.choice(wish)
    return gen_wish

def generate_joke():
    gen_joke = rand.choice(joke)
    return gen_joke

def day():
    day_str = "За тихоокеанським часом сьогодні " + str(today_day) + " число."
    return day_str
