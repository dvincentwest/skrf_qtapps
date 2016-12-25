import os

this_dir = os.path.normpath(os.path.dirname(__file__))
executable_dir = os.getcwd()
user_dir = os.path.expanduser("~")

last_path = os.path.join(this_dir, "data/")

if not os.path.isdir(last_path):
    last_path = user_dir

path_default = last_path
