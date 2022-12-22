from extra_commands import *
from json_commands import *

COOKED_EGG_RECIPES = 3
COOKED_EGG_PICTURES = 5
EASTER_EGG_PICTURES = 5
MAX_NICK_WORDS = 2
WRONG_COMMAND_MESSAGE = "Клоун, напиши /помощь"
WRONG_ARGUMENTS_MESSAGE = "Ты как-то неправильно эту команду используешь"

def get_cooked_egg():
    return get_jpg("CookedEggPictures\\cooked_egg", COOKED_EGG_PICTURES)


def get_cooked_egg_recipe():
    return read_txt(get_txt("CookedEggRecipes\\recipe", COOKED_EGG_RECIPES)).read()


def get_easter():
    return get_jpg("EasterEggPictures\\easter_egg", EASTER_EGG_PICTURES)

def test():
    pass


def get_help():
    return read_txt(get_txt("help_text")).read()


def get_nick():
    res = ""
    if rnd(0, 1) == 1:
        prefix = [word.strip() for word in read_txt(get_txt("NicknameParts\\prefix"))]
        res += prefix[rnd(0, len(prefix) - 1)]
    words = [word.strip() for word in read_txt(get_txt("NicknameParts\\words"))]
    for i in range(rnd(1, MAX_NICK_WORDS)):
        res += words[rnd(0, len(words) - 1)]
    number = [word.strip() for word in read_txt(get_txt("NicknameParts\\number"))]
    res += number[rnd(0, len(number) - 1)]
    return res;


def wrong_command():
    return WRONG_COMMAND_MESSAGE

def wrong_arguments():
    return WRONG_ARGUMENTS_MESSAGE

def get_statistics(chat_id, user_id):
    messages = json_get(json_get_statistics, "statistics",  chat_id, user_id)
    return {f"@id{user_id} (Пользователь) использовал {messages} команд"}

def get_top(args, chat_id, user_id):
    if args == ['яйца']:
        return json_get(json_get_eggs_top, "eggs")
    if args == ['команды']:
        return json_get(json_get_top_statistics, "statistics", chat_id)
    else:
        return wrong_arguments()