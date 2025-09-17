import glob, os, json


class interpret():
    def load_cmd_mods(File_Path):
        command_cache = dict()
        for file in glob.glob(f"{File_Path}/*.json"):
            print(f"Load file: {file}")
            with open(file, 'r') as incomingData:
                data = json.load(incomingData)
                for command in data["metadata"]["command_list"]:
                    command_cache[command]=file
                return command_cache
    
    def run_cmd(path, command, )






'''
Execute funciton without explicitly naming it
globals()["greet"]("Bob")
'''
