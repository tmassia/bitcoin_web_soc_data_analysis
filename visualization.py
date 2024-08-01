import matplotlib.pyplot as plt
import logging
from datetime import datetime
import os

# ensure 'media' directory exists
if not os.path.exists('media'):
    os.makedirs('media')


# function for boxplot graph
def plot_boxplot(delays, num_connections):
    try:
        # validate data types before
        if not isinstance(delays, list):
            raise ValueError("Input 'delays' must be a list.")
        if not isinstance(num_connections, int) or num_connections <= 0:
            raise ValueError("Input 'num_connections' must be a positive integer.")

        plt.figure(figsize=(14, 10))

        # prepare data for boxplot
        data = [[] for _ in range(num_connections)]
        for delay, update_id, connection_id in delays:
            # validate data
            if not isinstance(delay, (int, float)):
                logging.warning(f"Ignoring invalid delay value: {delay}")
                continue
            if not isinstance(update_id, int):
                logging.warning(f"Ignoring invalid update_id value: {update_id}")
                continue
            if not isinstance(connection_id, int) or connection_id < 0 or connection_id >= num_connections:
                logging.warning(f"Ignoring invalid connection_id value: {connection_id}")
                continue

            data[connection_id].append(delay)

        # check data for each connection
        for i, d in enumerate(data):
            if len(d) == 0:
                logging.warning(f"No data for connection {i}")
                continue

        # create custom set for  boxplot
        plt.boxplot(data, sym='.', showmeans=True)
        plt.xlabel('Connection ID')
        plt.ylabel('Delay (seconds)')
        plt.title('Boxplot of Delays for Each Connection')
        plt.xticks(ticks=range(1, num_connections + 1), labels=[f'Connection {i}' for i in range(num_connections)])

        # sett Y for better view on the graph details
        min_delay = min([min(d) for d in data if len(d) > 0])
        max_delay = max([max(d) for d in data if len(d) > 0])
        plt.ylim(min_delay - (max_delay - min_delay) * 0.1, max_delay * 1.1)

        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        # create unique file_name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join('media', f'delay_boxplot_{timestamp}.png')
        plt.savefig(filename)
        plt.close()
        logging.info(f"Box plot saved as {filename}")

    except Exception as e:
        logging.error(f"Error plotting box plot: {e}")
    finally:
        logging.info("Box plot created successfully.")
