Electricity Theft Detection Agent

A physics-inspired, machine learning-driven toolkit to detect electricity theft in low-voltage distribution grids.  
The system simulates realistic consumption, injects theft scenarios, and provides fully automated unsupervised anomaly detection—all visualized in an interactive dashboard.

Features
--------
- End-to-end power grid simulation using real physical equations  
- Synthetic consumption and theft scenario generation  
- Per-customer unsupervised anomaly detection via residual analysis  
- Interactive web dashboard for visual analytics  
- No hardware changes needed — works with existing meter readings  

Project Structure
-----------------
.
├── network_builder.py     # Build virtual power distribution grid
├── data_generator.py      # Generate synthetic consumption data
├── simulation_runner.py   # Simulate power flows & inject theft
├── detector.py            # Train models & detect anomalies
├── app2.py                # Streamlit dashboard for results
├── requirements.txt       # Python dependencies
└── ...

Quick Start
-----------
1. Clone the repository
   git clone <YOUR_REPO_URL>
   cd <YOUR_PROJECT_DIRECTORY>

2. Create & activate a virtual environment
   On Unix/macOS:
       python3 -m venv .venv
       source .venv/bin/activate

   On Windows:
       python -m venv .venv
       .venv\Scripts\activate

3. Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt

4. Run the project pipeline

   Step 1: Build grid and generate synthetic data (only needed once)
       python network_builder.py
       python data_generator.py
       python simulation_runner.py

   Step 2: Launch the dashboard app
        python app.py

   Open the displayed local URL in your browser to view results.

Requirements
------------
- Python 3.8+
- See requirements.txt for full list of package dependencies  

-----
- Edit data_generator.py and simulation_runner.py to change the number of customers or the simulation period.  
- All output CSV files will be generated in the project root directory.  
