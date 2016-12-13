import os

last_path = "C:/Coding/Python/skrf_qtapps/skrf_qtapps"
last_path = os.path.normpath(last_path)

executable_dir = os.getcwd()

if not os.path.isdir(last_path):
    last_path = os.path.expanduser("~")

path_default = last_path

visa_default = ""
config = {
    "visa resource": visa_default,
    "visa timeout": 10000,
    "default directory": path_default,
}
