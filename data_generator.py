import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_and_save_load_profiles():
    """
    This function generates realistic consumption data for 30 customers
    over 3 months and saves it into a CSV file.
    """
    print("Starting consumption data generation...")
    
    np.random.seed(42)  # Fix randomness to get reproducible results

    # 1. Define the time period
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 3, 31, 23, 45)  # Full 3 months
    date_range = pd.date_range(start=start_date, end=end_date, freq='15T')
    
    num_customers = 30

    # 2. Function to create a daily load profile
    def create_daily_profile():
        # Each day has 96 intervals (24 hours * 4 intervals/hour)
        # Morning peak (6 AM to 12 PM)
        morning_peak = np.linspace(0.3, 1.5, 24)
        # Afternoon lull (12 PM to 6 PM)
        afternoon_lull = np.linspace(1.5, 0.4, 24)
        # Evening peak (6 PM to 12 AM)
        evening_peak = np.linspace(0.4, 2.5, 24)
        # Night base load (12 AM to 6 AM)
        night_base = np.linspace(2.5, 0.3, 24)
        
        profile = np.concatenate([night_base, morning_peak, afternoon_lull, evening_peak])
        
        # Add noise to make it more realistic
        noise = np.random.normal(0, 0.1, 96)
        profile = profile + noise
        
        # Ensure no negative or extremely small values
        return np.maximum(profile, 0.05)

    # 3. Generate data for each customer for each day
    all_records = []
    
    # Pre-generate a unique profile for each customer (to save time)
    customer_profiles = [create_daily_profile() for _ in range(num_customers)]

    for timestamp in date_range:
        time_index = timestamp.hour * 4 + timestamp.minute // 15
        is_weekend = timestamp.weekday() >= 4  # Friday and Saturday

        for i in range(num_customers):
            # Get base consumption from the customer's profile
            base_consumption = customer_profiles[i][time_index]
            
            # Adjust consumption with random variation and weekend effect
            consumption = base_consumption * (0.9 + 0.2 * np.random.rand())
            if is_weekend:
                consumption *= 1.2  # Slightly higher consumption on weekends

            all_records.append({
                'Timestamp': timestamp,
                'Customer_ID': i + 1,
                'P_consumption_kw': round(consumption, 4)  # Power consumption in kW
            })

    # 4. Convert records to DataFrame and save as CSV
    consumption_df = pd.DataFrame(all_records)
    
    file_path = 'consumption_data.csv'
    consumption_df.to_csv(file_path, index=False)

    print(f"{len(consumption_df)} consumption records successfully generated!")
    print(f"Data saved to: {file_path}")
    
    return consumption_df

if __name__ == '__main__':
    consumption_df = generate_and_save_load_profiles()
    
    print("\n--- Sample of generated consumption data ---")
    print(consumption_df.head())
