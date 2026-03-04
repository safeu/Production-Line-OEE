import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

os.makedirs("data", exist_ok=True)
DB_PATH = os.path.join("data", 'oee.db')

def database_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS machines (
        machine_id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_name TEXT NOT NULL,
        department TEXT
        )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS production_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id INTEGER,
        shift_date TEXT NOT NULL,
        shift TEXT CHECK(shift IN ('morning', 'afternoon', 'night')),
        planned_production_time REAL NOT NULL,
        actual_run_time REAL NOT NULL,
        ideal_cycle_time REAL NOT NULL,
        total_units_produced INTEGER,
        good_units INTEGER,
        FOREIGN KEY (machine_id) REFERENCES machines (machine_id),
        UNIQUE(machine_id, shift_date, shift),
        CHECK (shift_date GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]'))""")
    
    conn.commit()
    conn.close()


def add_machine(name, department):
    try: 
        conn = database_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO machines (machine_name, department)
            VALUES (?, ?)
        """, (name, department)) 

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error adding machine: {e}")


def get_all_machines():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        results = cursor.execute("SELECT * FROM machines").fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Error getting all machines: {e}")

def add_log(machine_id, shift_date, shift, planned_production_time, actual_run_time, ideal_cycle_time, total_units_produced, good_units):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO production_logs (machine_id, shift_date, shift, planned_production_time, actual_run_time, ideal_cycle_time, total_units_produced, good_units)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (machine_id, shift_date, shift, planned_production_time, actual_run_time, ideal_cycle_time, total_units_produced, good_units))

        conn.commit()
        conn.close()

    except Exception as e:
        logger.error(f"Error adding logs: {e}")


def get_logs():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        results = cursor.execute("SELECT * FROM production_logs").fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Error fetching production logs: {e}")

def logs_by_machine(machine_id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        results = cursor.execute("SELECT * FROM production_logs WHERE machine_id = ?", (machine_id,)).fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Error fetching logs per machine: {e}")

def get_logs_by_date(start_date, end_date):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        results = cursor.execute("""
                SELECT * FROM production_logs WHERE shift_date BETWEEN ? AND ?
        """, (start_date, end_date)).fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Error fetching logs by date: {e}")