from bot_commands import *
from json_commands import *

class Bot:
    def __init__(self):
        self.eggs_count = {}
        self.commands = {
            "/яйцо": {"text": "35"},
            "/лох": {"text": "116"},
            "/ник": {"text": get_nick},
            "/яичница": {"image": get_cooked_egg, "text": get_cooked_egg_recipe},
            "/пасха": {"image": get_easter},
            "/помощь": {"text": get_help},
            "/статистика": {"text": get_statistics},
            "/поймать": {"text": self.playing_egg},
            "/мои_яйца": {"text": self.get_eggs},
            "/топ" : {"text" : get_top, "mentions" : "0"},
            "/нацист" : {"text" : "Эй, @masloenok (нацист)! Тебя позвали"},
            "bot" : {"text" : "С ботами не базарю"},
            "error": {"error" : wrong_command}
        }
    def playing_egg(self, chat_id, user_id):
        if str(chat_id) not in self.eggs_count.keys() or self.eggs_count[str(chat_id)] == 0:
            return f"@id{user_id} (Клоун), мне похер, в этой беседе нет яиц для поимки!"
        self.eggs_count[str(chat_id)] -= 1
        json_update(json_add_eggs, "eggs", chat_id, user_id)
        return f"@id{user_id} ({' '.join(get_username(user_id))}) получает яйцо&#129370;! Чтобы вывести баланс - напиши /мои_яйца"

    def start_egg_game(self, chat_id):
        chat_id = str(chat_id)
        if chat_id not in self.eggs_count.keys():
            self.eggs_count[chat_id] = 0
        self.eggs_count[chat_id] += 1
        return {"text" : "Появилось яйцо&#129370; для поимки! Напиши /поймать"}

    def get_eggs(self, chat_id, user_id):
        count = json_get(json_get_eggs, "eggs", chat_id, user_id)
        return f"У @id{user_id} (тебя) {count} шт. яиц&#129370;!"

    def do_command(self, command, args = [], *vk_args):
        if len(args) == 0:
            try:
                return command(*vk_args)
            except TypeError:
                try:
                    return command()
                except TypeError:
                    return wrong_arguments()
        else:
            try:
                return command(args, *vk_args)
            except ZeroDivisionError:
                try:
                    return command(args)
                except ZeroDivisionError:
                    return wrong_arguments()

    def get_command_res(self, message, *vk_args):
        parts = [i.lower() for i in message.split()]
        if parts[0] not in self.commands.keys() :
            return {'error' : wrong_command()}
        command = parts[0]
        args = parts[1:]
        res = {}
        for key in list(self.commands[command].keys()):
            try:
                if type(self.commands[command][key]) == str:
                    res[key] = self.commands[command][key]
                else:
                    res[key] = self.do_command(self.commands[command][key], args, *vk_args)
            except ZeroDivisionError:
                return {'error' : wrong_arguments()}
        return res
