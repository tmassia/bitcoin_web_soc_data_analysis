import asyncio
import logging
from dotenv import load_dotenv
import os
from collect_data import collect_data
from analyze_data import analyze_delays
from visualization import plot_boxplot

# Load environment variables
load_dotenv()

# Define constants from environment variables
BASE_URL = os.getenv('BASE_URL')
SYMBOL = os.getenv('SYMBOL')
NUM_CONNECTIONS = int(os.getenv('NUM_CONNECTIONS', 5))  # Default to 5 connections if not provided
COLLECT_TIME = int(os.getenv('COLLECT_TIME', 60))  # Default to collecting data for 60 seconds if not provided
RETRY_LIMIT = int(os.getenv('RETRY_LIMIT', 3))  # Default retry limit of 3 if not provided
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))  # Default retry delay of 5 seconds if not provided
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Default log level INFO if not provided

# Validate environment variables
if not BASE_URL or not SYMBOL or NUM_CONNECTIONS <= 0 or COLLECT_TIME <= 0 or RETRY_LIMIT <= 0 or RETRY_DELAY <= 0:
    raise ValueError(
        "Invalid environment variables. Please check BASE_URL, SYMBOL, NUM_CONNECTIONS, COLLECT_TIME, RETRY_LIMIT, and RETRY_DELAY.")

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(levelname)s - %(message)s')


# Main function to manage WebSocket connections and data collection
async def main():
    delays = []
    tasks = []
    # Establish connections
    for i in range(NUM_CONNECTIONS):
        ws_url = f"{BASE_URL}{SYMBOL}"
        logging.info(f"Connecting to {ws_url} with connection_id {i}")
        tasks.append(collect_data(ws_url, delays, i, COLLECT_TIME, RETRY_LIMIT, RETRY_DELAY))
    try:
        # Collect data concurrently
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error during data collection: {e}")
    finally:
        return delays


# Run the main function and analyze the collected data
if __name__ == "__main__":
    try:
        delays = asyncio.run(main())
        analyze_delays(delays, NUM_CONNECTIONS)
        # Ensure delays are converted to numeric type if they are in string format
        delays = [[float(row[0]), row[1], row[2]] for row in delays]
        plot_boxplot(delays, NUM_CONNECTIONS)
        print("Quick update ratios and statistical test results are logged.")
        print("Saved plots as delay_boxplot.png")
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
    finally:
        logging.info("Script execution finished.")