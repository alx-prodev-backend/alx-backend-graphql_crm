import logging
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            customers {
                id
            }
            orders {
                id
                totalAmount
            }
        }
        """
    )

    try:
        result = client.execute(query)

        customers = result.get("customers", [])
        orders = result.get("orders", [])

        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum([o["totalAmount"] for o in orders])

        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(log_entry)

        logger.info("CRM report generated successfully")
        return log_entry
    except Exception as e:
        logger.error(f"Failed to generate CRM report: {str(e)}")
        return str(e)
