import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


#
def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} CRM cron job executed\n")


#
def update_low_stock():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} Running low stock update...\n"

    try:
        # Transport GraphQL
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",  # Endpoint بتاع GraphQL
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # GraphQL Mutation
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    message
                    updatedProducts {
                        name
                        stock
                    }
                }
            }
        """)

        result = client.execute(mutation)
        data = result["updateLowStockProducts"]

        log_message += f"{data['message']}\n"
        for p in data["updatedProducts"]:
            log_message += f" - {p['name']} now has stock {p['stock']}\n"

    except Exception as e:
        log_message += f"GraphQL mutation failed: {str(e)}\n"

    # Log file
    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(log_message)
