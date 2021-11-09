# General
import json


def read_file(filename):
    f = open(filename)
    return json.load(f)


def write_to_file(filename, data):
    f = open(filename, "w+", encoding='utf8')
    f.write(data)
    f.close()
