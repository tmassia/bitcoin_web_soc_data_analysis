import pandas as pd
import logging
from scipy.stats import ttest_ind


# Function to analyze delays and print results
def analyze_delays(delays, num_connections):
    try:
        # Validate inputs
        if not isinstance(delays, list):
            raise ValueError("Input 'delays' must be a list.")
        if not isinstance(num_connections, int) or num_connections <= 0:
            raise ValueError("Input 'num_connections' must be a positive integer.")

        delays_df = pd.DataFrame(delays, columns=['delay', 'update_id', 'connection_id'])

        # calculate quick update ratios
        delays_df['min_update_id'] = delays_df.groupby('update_id')['delay'].transform('min')
        delays_df['is_fastest'] = delays_df['delay'] == delays_df['min_update_id']
        quick_ratios = delays_df.groupby('connection_id')['is_fastest'].mean()
        logging.info("Quick update ratios per connection:")
        logging.info(quick_ratios)

        # statistical tests
        delay_arrays = [delays_df[delays_df['connection_id'] == conn_id]['delay'].values for conn_id in
                        range(num_connections)]
        for i in range(num_connections):
            for j in range(i + 1, num_connections):
                if len(delay_arrays[i]) == 0 or len(delay_arrays[j]) == 0:
                    logging.warning(f"No data available for connection {i} or {j}")
                    continue
                t_stat, p_val = ttest_ind(delay_arrays[i], delay_arrays[j])
                logging.info(f"T-test between connection {i} and connection {j}: t-stat = {t_stat}, p-val = {p_val}")
    except ValueError as ve:
        logging.error(f"ValueError in analyze_delays: {ve}")
    except Exception as e:
        logging.error(f"Error analyzing delays: {e}")
