import asyncio
import websockets
import json
import time
import logging


# Function to collect messages and measure delays
async def collect_data(ws_url, delays, connection_id, collect_time, retry_limit, retry_delay):
    try:
        # Validate inputs
        if not isinstance(ws_url, str) or not ws_url.startswith("ws://") and not ws_url.startswith("wss://"):
            raise ValueError("Invalid WebSocket URL format. Must start with 'ws://' or 'wss://'.")
        if not isinstance(delays, list):
            raise ValueError("Input 'delays' must be a list.")
        if not isinstance(connection_id, int) or connection_id < 0:
            raise ValueError("Invalid 'connection_id'. Must be a non-negative integer.")
        if not isinstance(collect_time, (int, float)) or collect_time <= 0:
            raise ValueError("Invalid 'collect_time'. Must be a positive number.")
        if not isinstance(retry_limit, int) or retry_limit <= 0:
            raise ValueError("Invalid 'retry_limit'. Must be a positive integer.")
        if not isinstance(retry_delay, (int, float)) or retry_delay <= 0:
            raise ValueError("Invalid 'retry_delay'. Must be a positive number.")

        retries = 0
        while retries < retry_limit:
            try:
                async with websockets.connect(ws_url) as ws:
                    logging.info(f"Connected to {ws_url} with connection_id {connection_id}")
                    end_time = time.time() + collect_time
                    try:
                        while time.time() < end_time:
                            message = await ws.recv()
                            data = json.loads(message)
                            event_time = data['E'] / 1000  # convert to seconds
                            delay = time.time() - event_time
                            delays.append((delay, data['u'], connection_id))
                    except websockets.ConnectionClosed as e:
                        logging.error(f"Connection closed unexpectedly with connection_id {connection_id}: {e}")
                    finally:
                        logging.info(f"Connection with connection_id {connection_id} is being closed")
                return  # Exit the function if connected and collected data successfully
            except websockets.WebSocketException as e:
                retries += 1
                logging.error(f"Failed to connect to {ws_url} with connection_id {connection_id}: {e}")
                logging.info(f"Retrying ({retries}/{retry_limit})...")
                await asyncio.sleep(retry_delay)
        logging.warning(f"Giving up on connection_id {connection_id} after {retry_limit} retries")
    except ValueError as ve:
        logging.error(f"ValueError in collect_data: {ve}")
    except Exception as e:
        logging.error(f"Error in collect_data: {e}")
