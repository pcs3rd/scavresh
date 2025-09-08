import sys, os, datetime
path = os.path.dirname(os.path.realpath(__file__)) + '/sysmods'
if not path in sys.path:
    sys.path.insert(1, path)
del path

print(os.path.dirname(os.path.realpath(__file__)) + '/sysmods')

print(f"----\nPython Path:\n{sys.path}\n----\n")



#import mypackage

#del sys.path[-1]

from dataStore import dataStore


db = dataStore.session("test-db.db")

print(db)

print ("STEP: Test DB Configure")
dataStore.init_database_and_commit(db)

print("Test Setting Write: (test_setting = 'test success <time>')")
dataStore.write_setting(db, 'test_setting', f'test success {datetime.datetime.now().isoformat()}')

print("STEP: Test Read Setting")
print(f"Test Setting is Value: {dataStore.read_setting(db, 'test_setting')}")