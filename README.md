WebSocket Data Collection and Analysis

This Python project demonstrates a WebSocket data collection and analysis workflow using asyncio, websockets, pandas, 
matplotlib, and scipy.stats libraries.

1. Installation

    Make sure you have Python 3.9+ installed.
    
    ```
    pip install -r requirements.txt
    ```

2. Set Up Environment Variables:
    
    Create a .env file in the root directory with the following variables:
    ```
    BASE_URL=ws://your-base-url.com/
    SYMBOL=symbol_name
    NUM_CONNECTIONS=5
    COLLECT_TIME=60
    RETRY_LIMIT=3
    RETRY_DELAY=5
    LOG_LEVEL=INFO
    ```
    Adjust the values according to your WebSocket server configuration.


3. Usage

    Run the main script main.py to start collecting WebSocket data and analyzing delays:

    ```
    python main.py
    ```
    The script will connect to multiple WebSocket URLs (BASE_URL + SYMBOL) simultaneously, collect data for COLLECT_TIME
    seconds from each connection, and retry connections up to RETRY_LIMIT times with a delay of RETRY_DELAY seconds 
    between retries.


4. Features

    1.WebSocket Data Collection
        Concurrently collects real-time data from multiple WebSocket connections.

    2.Data Analysis
        Analyzes collected data to compute quick update ratios per connection and performs pairwise T-tests to compare
        delays between connections.
    
    3.Visualization
        Generates a boxplot visualizing delay distributions for each WebSocket connection.
    
    4.Troubleshooting
        Ensure all environment variables (BASE_URL, SYMBOL, etc.) are correctly set in the .env file.
        Check the console output for logs (INFO, WARNING, ERROR) to troubleshoot any connection issues or data collection 
        errors.