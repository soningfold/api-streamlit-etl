# api-streamlit-etl

## Project Description

This project is an ETL (Extract, Transform, Load) pipeline that uses the Coinbase API to pull data on the top 50 cryptocurrencies and some statistics about them. The data is then visualized using Streamlit.

## Features

- Extracts data from the Coinbase API
- Transforms the data to a suitable format
- Loads the data for visualization
- Visualizes the data using Streamlit

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/api-streamlit-etl.git
    ```
2. Navigate to the project directory:
    ```bash
    cd api-streamlit-etl
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the ETL pipeline:
    ```bash
    python src/etl.py
    ```
2. Start the Streamlit app:
    ```bash
    streamlit run src/app.py
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.