from lib.commands import Command
from lib import commands

VERSION = "0.0.1"

def init():
    print("Welcome to LogSearch! Version:", VERSION)
    try:
        dir_loc = open("config.txt").readline().strip()
    except:
        dir_loc = input("Location of accounting records: ")
    
    def is_action_class(var):
        return var != Command and type(var) == type and issubclass(var, Command)

    classes = []    
    for attr in dir(commands):
        var = getattr(commands, attr)
        if is_action_class(var):
            classes.append(var)
    instances = [c() for c in classes]
    return dir_loc, instances

def parce(user_input, instances, dir_loc):
    user_data = user_input.split()
    for command in instances:
        for keyword in command.keywords():
            if keyword in user_data:
                print(command.keywords())
                command.process(user_data, dir_loc)
def main():
    dir_loc, instances = init()
    last = ""
    while True:
        user_input = input(">>> ").lower()
        if not user_input.startswith("last"):
            last = user_input
        if user_input.startswith("exit") or user_input.startswith("logout"):
            exit()
        elif user_input.startswith("last"):
            parce(last, instances, dir_loc)
        elif len(user_input) > 0:
            parce(user_input, instances, dir_loc)
main()