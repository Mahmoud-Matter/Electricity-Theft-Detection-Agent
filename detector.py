import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

def train_and_detect():
    # --- Part 1: Load and split data ---
    print("1. Loading final dataset...")
    try:
        df = pd.read_csv('final_dataset_with_theft.csv')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    except FileNotFoundError:
        print("Error: 'final_dataset_with_theft.csv' not found.")
        return

    train_df = df[df['Timestamp'] < '2023-03-01'].copy()
    test_df = df[df['Timestamp'] >= '2023-03-01'].copy()
    print(f"Data split: {len(train_df)} training records, {len(test_df)} testing records.")

    # --- Part 2: Feature Engineering ---
    print("2. Building features (neighbors' total consumption)...")
    total_consumption_per_phase = df.groupby(['Timestamp', 'Phase'])['P_consumption_kw'].sum().reset_index()
    total_consumption_per_phase.rename(columns={'P_consumption_kw': 'Total_Phase_Consumption_kw'}, inplace=True)
    train_df = pd.merge(train_df, total_consumption_per_phase, on=['Timestamp', 'Phase'], how='left')
    test_df = pd.merge(test_df, total_consumption_per_phase, on=['Timestamp', 'Phase'], how='left')
    
    # --- Part 3: Train Models ---
    print("3. Training a model for each customer...")
    models = {}
    customer_ids = train_df['Customer_ID'].unique()
    for customer_id in tqdm(customer_ids, desc="Training Models"):
        customer_train_data = train_df[train_df['Customer_ID'] == customer_id]
        features = ['Voltage_V', 'Total_Phase_Consumption_kw']
        target = 'P_consumption_kw'
        X_train = customer_train_data[features]
        y_train = customer_train_data[target]
        model = LinearRegression()
        model.fit(X_train, y_train)
        models[customer_id] = model
    print("All models trained successfully!")

    # --- Part 4: Detection ---
    print("4. Starting detection on test data...")
    results = []
    for customer_id in tqdm(customer_ids, desc="Detecting Anomalies"):
        customer_test_data = test_df[test_df['Customer_ID'] == customer_id].copy()
        if customer_id in models:
            model = models[customer_id]
            X_test = customer_test_data[features]
            predicted_consumption = model.predict(X_test)
            customer_test_data['Residual'] = customer_test_data[target] - predicted_consumption
            anomaly_score = customer_test_data[customer_test_data['Residual'] < 0]['Residual'].sum()
            results.append({
                'Customer_ID': customer_id,
                'Anomaly_Score': anomaly_score
            })

    # --- Part 5: Save and Print Results ---
    print("\n--- Detection Complete! ---")
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by='Anomaly_Score', ascending=True)

    results_df.to_csv('anomaly_results.csv', index=False)
    print("Detection results saved to 'anomaly_results.csv'")

    ranked_df = results_df.reset_index(drop=True)
    try:
        thief_rank = ranked_df[ranked_df['Customer_ID'] == 5].index[0] + 1
        # رسالة بسيطة بدون رموز
        print(f"SUCCESS: Actual thief (Customer #5) detected at rank: #{thief_rank}")
    except IndexError:
        print(f"NOTE: The designated thief (Customer #5) was not found in the results.")

if __name__ == '__main__':
    train_and_detect()
