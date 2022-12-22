import json
import vk_api

from extra_commands import *

def json_change_statistics(data, chat_id, user_id):
    chat_id = str(chat_id)
    user_id = str(user_id)
    if chat_id not in data['chats'].keys():
        data['chats'][chat_id] = {}
    if user_id not in data['chats'][chat_id]:
        data['chats'][chat_id][user_id] = 0
    data['chats'][chat_id][user_id] += 1
    return data

def json_get_statistics(data, chat_id, user_id):
    return data['chats'][str(chat_id)][str(user_id)]

def json_get_top_statistics(data, chat_id):
    usernames = json_get(json_get_usernames, "usernames")
    usage = [(data['chats'][str(chat_id)][key], key) for key in data['chats'][str(chat_id)].keys()]
    usage = sorted(usage)[::-1][:10]
    res = "&#128285;Десять главных спамеров командами в этом чате&#127775; \n"
    for i in range(min(10, len(usage))):
        cur_id = int(usage[i][1])
        if str(cur_id) in usernames.keys():
            username = usernames[str(cur_id)]
        else:
            username = " ".join(get_username(int(usage[i][1])))
            json_update(json_write_username, "usernames", cur_id, username)
        res += f'{i+1}. [id{int(usage[i][1])}|{username}] написал команду {usage[i][0]} раз!\n'
    return res

def json_add_eggs(data, chat_id, user_id):
    try:
        data['eggs'][str(user_id)] += 1
    except KeyError:
        data['eggs'][str(user_id)] = 1
    return data

def json_get_eggs(data, chat_id, user_id):
    try:
        return data['eggs'][str(user_id)]
    except KeyError:
        data['eggs'][str(user_id)] = 0
        return data['eggs'][str(user_id)]

def json_get_usernames(data):
    return data["usernames"]

def json_write_username(data, id, username):
    data['usernames'][str(id)] = username
    return data

def json_get_eggs_top(data):
    usernames = json_get(json_get_usernames, "usernames")
    eggs = [(data['eggs'][key], key) for key in data['eggs'].keys()]
    eggs = sorted(eggs)[::-1][:10]
    res = "&#128285;Десять богатейших яйцевладельцев во всех чатах&#128200;&#129370; \n"
    for i in range(min(10, len(eggs))):
        cur_id = int(eggs[i][1])
        if str(cur_id) in usernames.keys():
            username = usernames[str(cur_id)]
        else:
            username = " ".join(get_username(int(eggs[i][1])))
            json_update(json_write_username, "usernames", cur_id, username)
        res += f'{i+1}. [id{int(eggs[i][1])}|{username}] имеет {eggs[i][0]} шт. яиц\n'
    return res


def json_get_chats(data):
    chats = list(data['chats'].keys())
    return chats

def json_update(command, file, *args):
    data = json.load(open(get_path(f"Data\\{file}.json"), "r",encoding="utf-8"))
    data = command(data, *args)
    with open(get_path(f"Data\\{file}.json"), "w") as write_file:
        write_file.write(json.dumps(data, indent=4))

def json_get(command, file, *args):
    data = json.load(open(get_path(f"Data\\{file}.json"), "r",encoding="utf-8"))
    res = command(data, *args)
    with open(get_path(f"Data\\{file}.json"), "w") as write_file:
        write_file.write(json.dumps(data, indent=4))
    return res

