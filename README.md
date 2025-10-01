# Electricity Theft Detection Agent


## Overview

An autonomous electricity theft detection agent for low-voltage distribution grids. While synthetic consumption and theft scenarios are generated externally, the agent takes over to train models, detect anomalies, and manage alerts. It operates end-to-end—from unsupervised detection to case generation and automated reporting—visualized through an interactive dashboard.

## Features

- End-to-end power grid simulation using real physical equations
- Synthetic consumption and theft scenario generation
- Per-customer unsupervised anomaly detection
- Interactive web dashboard
- No hardware changes needed — works with existing meter readings

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd [project-directory]
```

2. Create and activate virtual environment
```bash
python -m venv electric_theft_env

# Windows
electric_theft_env\Scripts\activate

# Linux/Mac
source electric_theft_env/bin/activate
```

3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

1. (Optional) Build grid and generate dataset.This step is only required once to generate the dataset from scratch.Since the dataset is already included in this repository, you can skip this part.

```bash
python network_builder.py
python data_generator.py
python simulation_runner.py
```

2. Start the web interface
```bash
python app.py
```

The web interface will be available at a URL like `http://localhost:7860`

## Project Structure

- `network_builder.py`: Build virtual power distribution grid
- `data_generator.py`: Generate synthetic consumption data
- `simulation_runner.py`: Simulate power flows & inject theft
- `detector.py`: Train models & detect anomalies
- `app.py`: Interactive web dashboard
- `requirements.txt`: Python dependencies

## Data Files

- `consumption_data.csv`: Raw consumption data
- `final_dataset_with_theft.csv`: Processed dataset with theft labels
- `anomaly_results.csv`: Detection results

## Configuration

- Edit `data_generator.py` and `simulation_runner.py` to change the number of customers or simulation period
- All output CSV files will be generated in the project root directory

## Requirements

- Python 3.10+
- Required libraries (see `requirements.txt`):

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
