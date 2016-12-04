import os

# last_path = os.path.expanduser("~")
# last_path += "/Documents/Data/MuEps measurements/"
last_path = "C:/Coding/Python/pyMultiCal/pyMultiCal/data"
last_path = os.path.normpath(last_path)

executable_dir = os.getcwd()

if not os.path.isdir(last_path):
    last_path = executable_dir

path_default = last_path

visa_default = ""
config = {
    "visa resource": visa_default,
    "visa timeout": 10000,
    "default directory": path_default,
}
