import sys, os
from datetime import datetime
path = os.path.dirname(os.path.realpath(__file__)) + '/sysmods'
if not path in sys.path:
    sys.path.insert(1, path)
del path

if os.path.exists("test-db.db"):
  os.remove("test-db.db")
else:
  print("Database does not already exist.")

print(os.path.dirname(os.path.realpath(__file__)) + '/sysmods')

print(f"----\nPython Path:\n{sys.path}\n----\n")



#import mypackage

#del sys.path[-1]

from dataStore import dataStore

now = datetime.now()
formatted_date = now.strftime("%H%M%S")
user_date = str(formatted_date)

db = dataStore.session("test-db.db")

print(db)


print ("STEP: Test DB Configure")
dataStore.init_database_and_commit(db)

print(f"\nTest Setting Write")
dataStore.write_setting(db, 'test_setting', f'test success {user_date}')

print("STEP: Test Read Setting")
print(f"\n---> Result should be 'test success {user_date}'")
print(f"Test Setting is Value: {dataStore.read_setting(db, 'test_setting')}")

print("STEP: Test User Data")
dataStore.write_user_property(db, f"13{user_date}", "current_hunt", f"testHunt-temp")

print("STEP: Read User Data")
print(f"\n---> Result should be 'testHunt-{user_date}'")
print(f"Test UserDat is Value: {dataStore.read_user_property(db, f"13{user_date}", "current_hunt")}")

print("\n\n_______SECTION_______: Scavenger Data")
dataStore.create_scavenger_hunt(db, f"testHunt")
print("\n_______SECTION_______: List Scavenger Hunts")
for hunt in dataStore.get_scavenger_hunts(db):
    print(hunt[0])

print("\n_______SECTION_______: add Scavenger Hunt steps to test hunt")


dataStore.create_scavenger_hunt_step(db, f"testHunt")
dataStore.write_scavenger_step_property(db, f"testHunt", "1", f"type", f"loc")

dataStore.create_scavenger_hunt_step(db, "testHunt")
dataStore.write_scavenger_step_properties(db, "testHunt", "2", {"type":"loc","enabled":True,"longitude":"12","latitude":"13"})

print("\n_______SECTION_______: READ Scavenger Hunts")
print(dataStore.get_scavenger_steps(db, "testHunt"))