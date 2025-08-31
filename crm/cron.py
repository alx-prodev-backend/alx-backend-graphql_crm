import os
from datetime import datetime

#  GraphQL
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"


def log_crm_heartbeat():
    """Logs heartbeat message every 5 mins"""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Append log
    with open(LOG_FILE, "a") as f:
        f.write(message)

    # test GraphQL hello field
    try:
        asyncio.run(query_hello())
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} GraphQL hello query failed: {e}\n")


async def query_hello():
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            hello
        }
        """
    )
    async with client as session:
        result = await session.execute(query)
        ts = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{ts} GraphQL hello response: {result}\n")
import os
from datetime import datetime

# GraphQL
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"


def log_crm_heartbeat():
    """Logs heartbeat message every 5 mins"""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Append log
    with open(LOG_FILE, "a") as f:
        f.write(message)

    # test GraphQL hello field
    try:
        asyncio.run(query_hello())
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} GraphQL hello query failed: {e}\n")


async def query_hello():
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            hello
        }
        """
    )
    async with client as session:
        result = await session.execute(query)
        ts = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{ts} GraphQL hello response: {result}\n")
