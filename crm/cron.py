import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    #
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    #  GraphQL endpoint
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
            query {
                hello
            }
        """)
        result = client.execute(query)
        message = f"{message.strip()} | GraphQL says: {result.get('hello')}\n"
    except Exception as e:
        message = f"{message.strip()} | GraphQL check failed: {str(e)}\n"

    #
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)
