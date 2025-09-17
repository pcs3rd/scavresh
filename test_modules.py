import sys, os
from datetime import datetime
path = os.path.dirname(os.path.realpath(__file__)) + '/sysmods'
if not path in sys.path:
    sys.path.insert(1, path)
del path

from interpret import interpret

command_cache = interpret.load_cmd_mods(os.path.dirname(os.path.realpath(__file__)) + '/Module_Bin')
for command, key in command_cache.items():
    print(f"{command} \n {key}")