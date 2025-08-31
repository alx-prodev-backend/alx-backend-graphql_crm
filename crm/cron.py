import datetime

def log_crm_heartbeat():
    """Logs heartbeat message to /tmp/crm_heartbeat_log.txt every 5 mins"""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:  # append mode
        f.write(message)

