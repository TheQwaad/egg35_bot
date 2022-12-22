from random import randint as rnd
import os
import vk_api

PATH = os.path.dirname(os.path.abspath(__file__))
token = open("TOKEN.txt", "r").readline().strip()
extra_vk = vk_api.VkApi(token=token)

def get_path(sub_path = "", file_format = ""):
    return PATH + "\\" + sub_path + file_format

def get_random_asset(sub_path, variants=0):
    variant = ""
    if variants > 0:
        variant = str(rnd(1, variants))
    return get_asset(sub_path) + variant


def get_jpg(sub_path, variants=0):
    return get_random_asset(sub_path, variants) + '.jpg'


def get_txt(sub_path, variants=0):
    return get_random_asset(sub_path, variants) + '.txt'

def read_txt(path):
    return open(path, "r", encoding="utf-8")

def get_asset(sub_path):
    return PATH + "\\Assets\\" + sub_path

def get_username(user_id):
    token = open("TOKEN.txt", "r").readline().strip()
    username = extra_vk.method("users.get", {"user_ids": user_id})[0]
    return [username['first_name'], username['last_name']]