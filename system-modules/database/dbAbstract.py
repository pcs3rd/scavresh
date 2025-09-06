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
    def __init__(self):
        pass

    def session(self, name="default.db"):
        db = sqlite3.connect(name)
        #cursor = db.cursor()
        return db.cursor()
    
    def kill_session(self, cursor):
        cursor.close()

    def init_dabase_and_commit(self, cursor):
        querry = f'''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY, 
                setting text NOT NULL, 
                value text NOT NULL
            );

            CREATE TABLE IF NOT EXISTS user-data (
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

            CREATE TABLE IF NOT EXISTS scavenger-hunts (
                id INTERGER PRIMARY KEY, 
                scavenger_name TEXT NOT NULL, 
                scavenger_hunt_description TEXT NOT NULL,
                scavenger_table TEXT NOT NULL, 
                scavenger_time_constrained BOOL NOT NULL, 
                scavenger_start_time_ISO8601 TEXT, 
                scavenger_end_time_ISO8601 TEXT,
                scavenger_last_activity_ISO8601 TEXT,
                scavenger_last_user TEXT,
                scavenger_edit_ISO8601 TEXT
            );
        '''
        cursor.execute(querry)
        cursor.commit()

    def write_setting(self, cursor, setting, value): # Used to update a setting property value
        query = f'''
            INSERT OR REPLACE INTO settings SET value = '{value}' WHERE setting='{setting};'
        '''
        cursor.execute(query)
        cursor.commit()

    def read_setting(self, cursor, setting): # Used to read a setting's property value
        query = f'''
            SELECT value FROM settings WHERE setting='{setting};'
        '''
        cursor.execute(query)
        return cursor.fetchone()[0]
    
    def update_user_property(self, cursor, user, property, value, editor='not provided'):
        query = f'''
            INSERT OR REPLACE INTO user-data SET {property}='{value}' WHERE node_num='{user};'
            UPDATE user-data SET last-edit_ISO8601 = '{datetime.datetime.now().isoformat()}' WHERE node_num='{user}';
        '''
        cursor.execute(query)
        cursor.commit()

    # Scavenger Hunt Management
    def create_scavenger_hunt(self, cursor, scavenger_hunt_name=f"Scavenger_hunt-{datetime.datetime.now().isoformat()}"):
        query = f'''
            INSERT OR REPLACE INTO scavenger-hunts SET {property}='{value}' WHERE node_num='{user};'

            CREATE TABLE IF NOT EXISTS {scavenger_hunt_name} (
                id INTERGER PRIMARY KEY,
                name TEXT NOT NULL, 
                type TEXT NOT NULL,
                required_previous_step BOOL NOT NULL,
                enabled BOOL NOT NULL, 
                previous_step_index INT,
                hint TEXT, 
                longitude NUMERICAL, 
                latitude NUMERICAL, 
                answer TEXT,
                created_by int(9) NOT NULL
            );
            UPDATE scavenger-hunts SET last-edit_ISO8601 = '{datetime.datetime.now().isoformat()}' WHERE scavenger_name='{scavenger_hunt_name}';
        '''
        cursor.execute(query)
        cursor.commit()

    def delete_scavenger_hunt(self, cursor, scavenger_hunt_name):
        query = f'''
            DROP TABLE {scavenger_hunt_name};
            DELETE FROM scavenger-hunts WHERE scavenger_name = '{scavenger_hunt_name}';
            '''
        cursor.execute(query)

    def list_scavenger_hunts(self, cursor):
        query = f'''
            SELECT name FROM scavenger-hunts'
        '''
        cursor.execute(query)
        return cursor.fetchall()
    
    def list_scavenger_hunt_flows(self, cursor, scavenger_hunt_name):
        query = f'''
            SELECT * FROM {scavenger_hunt_name}' WHERE enabled=True
        '''
        cursor.execute(query)
        return cursor.fetchall()
            