import psycopg2
import time
import hashlib
import logging
import os

# PostgreSQL の接続情報
DB_HOST = os.environ.get('DATABASE_HOST', 'postgres')
DB_PORT = os.environ.get('DATABASE_PORT', '5432')
DB_NAME = os.environ.get('DATABASE_NAME', 'firezone')
DB_USER = os.environ.get('DATABASE_USER', 'postgres')
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
FZLOGGING_INTERVAL_SEC = os.environ.get('FZLOGGING_INTERVAL_SEC', 60)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# diff store
last_devices_data = None

def fetch_devices():
    """devices テーブルの内容を取得して出力する"""
    global last_devices_data
    
    try:
        # connetct pg
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        
        # get data
        cursor.execute("SELECT * FROM devices;")
        rows = cursor.fetchall()

        # close db
        cursor.close()
        conn.close()
        

        # create hash
        current_data_hash = hashlib.sha256(str(rows).encode()).hexdigest()
        
        # diff check
        if last_devices_data is not None:
            last_data_hash = hashlib.sha256(str(last_devices_data).encode()).hexdigest()
            
            if current_data_hash != last_data_hash:
                logger.info('[fz device] diff detected')
                for row in rows:
                    logger.info(row)
            else:
                logger.debug('[fz device] No diff')
        else:
            logger.info('[fz device] diff detected (first time)')
            for row in rows:
                logger.info(row)
        
        last_devices_data = rows
    
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    while True:
        fetch_devices()
        time.sleep(FZLOGGING_INTERVAL_SEC)