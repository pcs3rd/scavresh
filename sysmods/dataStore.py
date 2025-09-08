'''
ABOUT THIS MODULE
----
Author: Raymond Dean (KC3ZXI)
Description: A class to help abstract database functions. 

Provided Methods:
> session(database name)
> kill_session(session)
> init_database_and_commit(session)
> write_setting(session, setting, value)
> read_setting(session, setting)
> update_user_property(session, user id, property, value)
> create_scavenger_hunt(session, )
'''

import sqlite3, datetime 

class dataStore():
    # def __init__(self):
    #     pass

    def session(name="default.db"):
        db = sqlite3.connect(name)
        cursor = db.cursor()
        return (db, cursor)
    
    def kill_session(db):
        db.close()

    def init_database_and_commit(session):
        querry = [f'''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY, 
                setting text NOT NULL UNIQUE, 
                value text NOT NULL
            );''', 
            f'''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY, 
                node_num int(9) NOT NULL, 
                node_name varchar(36) NOT NULL,
                last_hit TEXT,
                completed_hunts TEXT, 
                current_hunt TEXT,
                last_hunt TEXT, 
                last_step_name TEXT, 
                last_task_completion TEXT,
                last_edit_ISO8601 TEXT NOT NULL,
                last_edit_by int(9) NOT NULL
            );
            ''',
            f'''
            CREATE TABLE IF NOT EXISTS scavenger_hunts (
                id INTERGER PRIMARY KEY, 
                scavenger_name TEXT, 
                scavenger_hunt_description TEXT,
                scavenger_table TEXT, 
                scavenger_time_constrained BOOL, 
                scavenger_start_time_ISO8601 TEXT, 
                scavenger_end_time_ISO8601 TEXT,
                scavenger_last_activity_ISO8601 TEXT,
                scavenger_last_user TEXT,
                scavenger_edit_ISO8601 TEXT
            );
            '''
            ]
        
        for command in querry:
            print(command)
            session[1].execute(command)
            session[0].commit()




    def write_setting(session, setting, value): # Used to update a setting property value
        query = f'''
            INSERT OR REPLACE INTO settings (setting, value) VALUES ('{setting}', '{value}');        
        '''
        session[1].execute(query)
        session[0].commit()

    def read_setting(session, setting): # Used to read a setting's property value
        query = f'''
            SELECT value FROM settings WHERE setting = '{setting}';
        '''
        session[1].execute(query)
        return session[1].fetchone()[0]
    
    def update_user_property(session, user, property, value, editor='not provided'):
        query = f'''
            INSERT INTO user-data SET {property}='{value}' WHERE node_num='{user};'
            UPDATE user-data SET last-edit_ISO8601 = '{datetime.datetime.now().isoformat()}' WHERE node_num='{user}';
        '''
        session[1].execute(command)
        session[0].commit()

    # Scavenger Hunt Management
    # Need to update scavenger_hunts table. Work not finished yet.
    def create_scavenger_hunt(cursor, request_user, scavenger_hunt_name=f"Scavenger_hunt-{datetime.datetime.now().isoformat()}"):
        query = f'''
            INSERT INTO scavenger-hunts (scavenger_name, created_by) ('{scavenger_hunt_name}', '{request_user}');


            CREATE TABLE IF NOT EXISTS {scavenger_hunt_name} (
                id INTERGER PRIMARY KEY,
                name TEXT NOT NULL, 
                type TEXT,
                required_previous_step BOOL,
                enabled BOOL, 
                previous_step_index INT,
                hint TEXT, 
                longitude NUMERICAL, 
                latitude NUMERICAL, 
                answer TEXT,
                created_by int(9) NOT NULL
            );
            UPDATE scavenger-hunts SET last_edit_ISO8601 = '{datetime.datetime.now().isoformat()}' WHERE scavenger_name='{scavenger_hunt_name}';
        '''
        session[1].execute(query)
        cursor.commit()

    def delete_scavenger_hunt(cursor, scavenger_hunt_name):
        query = f'''
            DROP TABLE {scavenger_hunt_name};
            DELETE FROM scavenger-hunts WHERE scavenger_name = '{scavenger_hunt_name}';
            '''
        session[1].execute(query)

    def modify_scavenger_hunt(cursor, scavenger_name, property, value):
        query = f'''
            INSERT OR REPLACE INTO settings SET {property} = '{value}' WHERE name='{scavenger_name};'
        '''
        session[1].execute(query)
        cursor.commit()        

    def list_scavenger_hunts(cursor):
        query = f'''
            SELECT name FROM scavenger-hunts'
        '''
        session[1].execute(query)
        return cursor.fetchall()
    
    def get_all_scavenger_hunt_flows(cursor, scavenger_hunt_name):
        query = f'''
            SELECT * FROM {scavenger_hunt_name}' WHERE enabled=True
        '''
        session[1].execute(query)
        return cursor.fetchall()
    
    def add_scavenger_hunt_step(cursor, scavenger_name, property, value):
        query = f'''
            INSERT INTO {scavenger_name} SET {property} = '{value}'
        '''
        session[1].execute(query)
        return cursor.fetchall()

                # '''id INTERGER PRIMARY KEY,
                # name TEXT NOT NULL, 
                # type TEXT NOT NULL,
                # required_previous_step BOOL NOT NULL,
                # enabled BOOL NOT NULL, 
                # previous_step_index INT,
                # hint TEXT, 
                # longitude NUMERICAL, 
                # latitude NUMERICAL, 
                # answer TEXT,
                # created_by int(9) NOT NULL'''