#!/usr/bin/env python3
import asyncio
import logging
from datetime import datetime, timedelta

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

# إعداد اللوج
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# GraphQL query
query = gql("""
    query GetRecentOrders($since: DateTime!) {
        orders(orderDate_Gte: $since) {
            id
            customer {
                email
            }
            orderDate
        }
    }
""")

async def main():
    # Last 7 Days report
    since_date = (datetime.utcnow() - timedelta(days=7)).isoformat()

    #GraphQL endpoint
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    async with Client(transport=transport, fetch_schema_from_transport=True,) as session:
        result = await session.execute(query, variable_values={"since": since_date})

        orders = result.get("orders", [])
        for order in orders:
            order_id = order["id"]
            email = order["customer"]["email"]
            logging.info(f"Order ID: {order_id} | Email: {email}")

    print("Order reminders processed!")

if __name__ == "__main__":
    asyncio.run(main())
