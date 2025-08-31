import requests
import logging
from datetime import datetime

# Log prepare
LOG_FILE = "/tmp/crmreportlog.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def generatecrmreport():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        if response.status_code == 200:
            data = response.json()
            logging.info("CRM Report generated successfully with %d records", len(data))
        else:
            logging.error("Failed to fetch CRM data. Status code: %d", response.status_code)
    except Exception as e:
        logging.error("Error generating CRM report: %s", str(e))
