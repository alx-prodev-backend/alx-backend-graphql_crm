#!/usr/bin/env python3
import sys
import os
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# 
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# GraphQL transport
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# 
today = datetime.utcnow()
one_week_ago = today - timedelta(days=7)

# GraphQL query
query = gql(
    """
    query getRecentOrders($fromDate: DateTime!) {
      orders(filter: {orderDate_Gte: $fromDate}) {
        id
        customer {
          email
        }
      }
    }
    """
)

try:
    result = client.execute(query, variable_values={"fromDate": one_week_ago.isoformat()})
    orders = result.get("orders", [])

    for order in orders:
        order_id = order["id"]
        email = order["customer"]["email"]
        timestamp = datetime.now().isoformat()
        logging.info(f"{timestamp} - Order ID: {order_id}, Email: {email}")

    print("Order reminders processed!")

except Exception as e:
    logging.error(f"Error: {e}")
    sys.exit(1)

