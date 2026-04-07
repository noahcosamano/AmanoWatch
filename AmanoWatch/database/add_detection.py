import sqlite3

DB_PATH = "AmanoWatch/database/amanowatch.db"

def add_detection(timestamp, detector_type, severity, summary, src_ip=None, src_mac=None, 
                  src_port=None, dst_ip=None, dst_mac=None, dst_port=None, details=None):
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO detections (
            timestamp,
            detector_type,
            severity,
            src_ip,
            src_mac,
            src_port,
            dst_ip,
            dst_mac,
            dst_port,
            details,
            summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        detector_type,
        severity,
        src_ip,
        src_mac,
        src_port,
        dst_ip,
        dst_mac,
        dst_port,
        details,
        summary
    ))
    
    conn.commit()
    conn.close()