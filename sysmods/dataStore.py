'''
ABOUT THIS MODULE
----
Author: Raymond Dean (KC3ZXI)
Description: A class to help abstract database functions. 
'''

import sqlite3, datetime, random, re

class dataStore():
    # def __init__(self):
    #     pass
    def sanitize_input(input): # Holy Crap. I'm done dealing with "-" garbo.
        return re.sub("-", "_", input)

    def randomwords(how_many=3):
        one = ["crazy", "fast", "slow", "careful", "horse"]
        two = ["horse", "cat", "dog", "pig", "barfs"]
        three = ["jump", "nap", "sleep", "watch", "ponder"]
        return f"{one[random.randrange(0,5)]} {two[random.randrange(0,5)]} {three[random.randrange(0,5)]}"

    def session(name="default.db"):
        db = sqlite3.connect(name)
        cursor = db.cursor()
        return (db, cursor)
    
    def kill_session(db):
        db.close()

    def init_database_and_commit(session):
        querry = [f'''
            CREATE TABLE IF NOT EXISTS settings (
                setting text NOT NULL UNIQUE PRIMARY KEY, 
                value text NOT NULL
            );''', 
            f'''
            CREATE TABLE IF NOT EXISTS user_data (
                node_num int(9) NOT NULL UNIQUE PRIMARY KEY, 
                node_name varchar(36),
                last_hit TEXT,
                completed_hunts TEXT, 
                current_hunt TEXT,
                last_hunt TEXT, 
                last_step_name TEXT, 
                last_task_completion TEXT,
                last_edit TEXT NOT NULL,
                last_edit_by int(9) NOT NULL
            );
            ''',
            f'''
            CREATE TABLE IF NOT EXISTS scavenger_hunts (
                scavenger_name TEXT UNIQUE PRIMARY KEY, 
                scavenger_hunt_description TEXT,
                scavenger_table TEXT UNIQUE, 
                scavenger_time_constrained BOOL, 
                scavenger_start_time_ISO8601 TEXT, 
                scavenger_end_time_ISO8601 TEXT,
                scavenger_last_activity_ISO8601 TEXT,
                scavenger_last_user TEXT,
                scavenger_last_edit_ISO8601 TEXT,
                scavenger_by int(9)
            );
            '''
            ]
        
        for command in querry:
            session[1].execute(command)
            session[0].commit()




    def write_setting(session, setting, value): # Used to update a setting property value
        query = f'''INSERT OR REPLACE INTO settings (setting, value) VALUES ('{setting}','{value}');'''
        session[1].execute(query)
        session[0].commit()

    def read_setting(session, setting): # Used to read a setting's property value
        query = f'''SELECT value FROM settings WHERE setting = '{setting}';'''
        session[1].execute(query)
        return session[1].fetchone()[0]
    
    def create_user(session):
        pass

    def write_user_property(session, user, property, value, editor='000000000'):
        querry = [f'''INSERT OR REPLACE INTO user_data (node_num,{property},last_edit_by,last_edit) VALUES ({user},'{value}','{editor}','{datetime.datetime.now().isoformat()}');'''
        ]
        for command in querry:
            session[1].execute(command)
            session[0].commit()

    def read_user_property(session, user, property):
        query = f'''SELECT "{property}" FROM user_data WHERE node_num = '{user}';'''
        session[1].execute(query)
        return session[1].fetchone()[0]
    
    # Scavenger Hunt Management
    # Need to update scavenger_hunts table. Work not finished yet.
    def create_scavenger_hunt(session, scavenger_hunt_name=f"Scavenger_hunt {randomwords()}", request_user="000000000"):
        query = [f'''
            INSERT INTO scavenger_hunts (scavenger_name, scavenger_by, scavenger_table) VALUES ('{dataStore.sanitize_input(scavenger_hunt_name)}','{request_user}','{dataStore.sanitize_input(scavenger_hunt_name)}');
            ''',
            f'''
            CREATE TABLE IF NOT EXISTS '{dataStore.sanitize_input(scavenger_hunt_name)}' (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                type TEXT,
                required_previous_step BOOL,
                previous_step_index INT,
                hint TEXT, 
                longitude NUMERICAL, 
                latitude NUMERICAL, 
                answer TEXT,
                enabled BOOL
            );
            ''', 
            f'''
            UPDATE scavenger_hunts SET scavenger_last_edit_ISO8601 = '{datetime.datetime.now().isoformat()}' WHERE scavenger_name='{dataStore.sanitize_input(scavenger_hunt_name)}';
            ''', 
        ]
        try:
            for command in query:    
                session[1].execute(command)
                session[0].commit()
        except sqlite3.IntegrityError:
            raise "scavenger creation has failed. Ensure name is unique"


    def delete_scavenger_hunt(session, scavenger_hunt_name):
        query = [f'''
            DROP TABLE {scavenger_hunt_name};''',
            f'''
            DELETE FROM scavenger-hunts WHERE scavenger_name = '{scavenger_hunt_name}';
            ''']
        for command in query:    
            session[1].execute(command)
            session[0].commit()

    def modify_scavenger_hunt(session, scavenger_name, property, value):
        query = f'''
            INSERT OR REPLACE INTO settings SET {property} = '{value}' WHERE name='{dataStore.sanitize_input(scavenger_name)};'
        '''
        session[1].execute(command)
        session[0].commit()  

    def get_scavenger_hunts(session):
        query = f'''
            SELECT scavenger_name FROM scavenger_hunts
        '''
        session[1].execute(query)
        return session[1].fetchall()
    
    def get_scavenger_steps(session, scavenger_hunt_name):
        query = f'''
            SELECT * FROM '{dataStore.sanitize_input(scavenger_hunt_name)}';
        '''
        session[1].execute(query)
        return session[1].fetchall()
    
    def create_scavenger_hunt_step(session, scavenger_name):
        query = f'''INSERT INTO {dataStore.sanitize_input(scavenger_name)} DEFAULT VALUES;'''
        session[1].execute(query)
        session[0].commit()
    
    def write_scavenger_step_property(session, scavenger_name, id, property, value):
        query = f'''UPDATE {dataStore.sanitize_input(scavenger_name)} SET {property} = '{value}' WHERE id={id};'''
        session[1].execute(query)
        session[0].commit()

    def write_scavenger_step_properties(session, scavenger_name, id, propertyDict):
        for property, value in propertyDict.items():
            query = f'''UPDATE {dataStore.sanitize_input(scavenger_name)} SET {property} = '{value}' WHERE id={id};'''
            session[1].execute(query)
        session[0].commit()