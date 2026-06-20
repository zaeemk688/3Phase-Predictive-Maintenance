import psycopg2

# ====================================================================
# CREDENTIALS: Adjust to match your local PostgreSQL server settings
# ====================================================================
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "YOUR_POSTGRES_PASSWORD_HERE"  # <-- Put your password here
DB_NAME = "three_phase_maintenance"

def get_connection():
    """Establishes a connection to your dedicated FYP database."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )

def log_telemetry(system_mode, smoke_level, flame_tripped, voltages, currents):
    """Inserts a standard real-time data frame into the telemetry_logs table."""
    query = """
        INSERT INTO telemetry_logs (system_mode, smoke_level, flame_tripped, v1, v2, v3, v4, v5, v6, c1, c2, c3, c4, c5, c6)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        params = (
            system_mode, smoke_level, flame_tripped,
            voltages[0], voltages[1], voltages[2], voltages[3], voltages[4], voltages[5],
            currents[0], currents[1], currents[2], currents[3], currents[4], currents[5]
        )
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ Database Logging Warning: {e}")

def save_blackbox_emergency(fault_type, trigger_source, smoke, flame, voltages, currents, ai_state):
    """Flight Data Recorder: Instantly logs system state details right before a shutdown."""
    query = """
        INSERT INTO blackbox_fault_logs (fault_type, trigger_source, last_known_smoke, last_known_flame, voltages_snapshot, currents_snapshot, ai_diagnostic_state)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (fault_type, trigger_source, smoke, flame, voltages, currents, ai_state))
        conn.commit()
        print(f"🔒 [BLACKBOX LOCKED] Critical event saved. Reason: {fault_type}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Critical Blackbox Write Error: {e}")