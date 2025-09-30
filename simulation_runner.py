import pandas as pd
import pandapower as pp
from tqdm import tqdm
# Import the function that builds the network from the first file
from network_builder import create_egyptian_lv_network

def run_full_simulation():
    """
    Main function to run the simulation, merge data, and inject theft scenarios.
    """
    # --- Part 1: Load data and network ---
    print("1. Loading the network and consumption data...")
    net, topology_df = create_egyptian_lv_network()
    consumption_df = pd.read_csv('consumption_data.csv')
    consumption_df['Timestamp'] = pd.to_datetime(consumption_df['Timestamp'])

    # Merge consumption data with topology to get Bus_ID for each record
    merged_df = pd.merge(consumption_df, topology_df, on='Customer_ID')
    
    # --- Part 2: Run power flow simulation ---
    print("2. Starting power flow simulation... This process may take some time.")
    
    all_results = []
    unique_timestamps = merged_df['Timestamp'].unique()

    # Use tqdm to show progress bar
    for timestamp in tqdm(unique_timestamps, desc="Simulating time periods"):
        # Get consumption data for this timestamp only
        time_slice_df = merged_df[merged_df['Timestamp'] == timestamp]

        # Add current loads to the network
        for _, row in time_slice_df.iterrows():
            # Convert consumption from kW to MW
            p_mw = row['P_consumption_kw'] / 1000
            pp.create_load(net, bus=row['Bus_ID'], p_mw=p_mw, q_mvar=0, name=f"Load C{row['Customer_ID']}")
        
        # *** Run the simulation ***
        try:
            pp.runpp(net)
            # Record results (voltage and consumption)
            for _, row in time_slice_df.iterrows():
                bus_id = row['Bus_ID']
                # Read per unit voltage and convert it to Volts
                vm_pu = net.res_bus.vm_pu.at[bus_id]
                vn_kv = net.bus.vn_kv.at[bus_id]
                voltage_v = vm_pu * vn_kv * 1000  # Actual voltage in Volts
                
                all_results.append({
                    'Timestamp': timestamp,
                    'Customer_ID': row['Customer_ID'],
                    'Phase': row['Phase'],
                    'P_consumption_kw': row['P_consumption_kw'],
                    'Voltage_V': round(voltage_v, 2)
                })
        except Exception as e:
            # If the simulation fails (rare), skip this timestamp
            # print(f"Simulation failed at {timestamp}: {e}")
            pass
        
        # Remove loads before next timestamp
        net.load.drop(net.load.index, inplace=True)

    # Convert results to DataFrame
    ground_truth_df = pd.DataFrame(all_results)
    
    print("\n3. Simulation completed! Merging voltage data with consumption.")
    
    # --- Part 3: Inject theft scenario ---
    print("4. Injecting theft scenario...")
    final_df = ground_truth_df.copy()
    
    # Select the stealing customer (e.g., Customer 5)
    thief_id = 5
    # Define theft start date (after 2 months)
    theft_start_date = pd.to_datetime('2023-03-01')
    
    # Filter data for the thief after the theft start date
    theft_indices = final_df[(final_df['Customer_ID'] == thief_id) & (final_df['Timestamp'] >= theft_start_date)].index
    
    # Manipulate the meter: reduce recorded consumption by 90%
    # Keep the voltage unchanged since it reflects the actual high consumption
    final_df.loc[theft_indices, 'P_consumption_kw'] *= 0.1
    
    # Add a column to indicate theft (for evaluation purposes later)
    final_df['Is_Theft'] = 0
    final_df.loc[theft_indices, 'Is_Theft'] = 1

    # 5. Save the final dataset
    file_path = 'final_dataset_with_theft.csv'
    final_df.to_csv(file_path, index=False)
    
    print(f"\nStep 3 completed successfully!")
    print(f"Final dataset ready for training has been saved to: {file_path}")

if __name__ == '__main__':
    run_full_simulation()
