import pandas as pd
import requests
from io import StringIO
from datetime import datetime
from models import MarketPrice
from app import db
import logging

AGMARKNET_CSV_URL = "https://agmarknet.gov.in/Download/Price_Data/csv/"

MANDIS = ["Dehradun", "Haldwani", "Pithoragarh"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_parse_agmarknet(date_str):
    """
    Fetch Agmarknet CSV for the given date (YYYYMMDD) and parse market prices for selected mandis.
    """
    url = f"{AGMARKNET_CSV_URL}Daily_{date_str}.csv"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to download data for {date_str}, status code: {response.status_code}")
            return
    except Exception as e:
        logger.error(f"Exception occurred while downloading data for {date_str}: {e}")
        return

    csv_data = StringIO(response.text)
    try:
        df = pd.read_csv(csv_data)
    except Exception as e:
        logger.error(f"Failed to parse CSV data for {date_str}: {e}")
        return

    required_columns = ['Market Name', 'Commodity', 'Variety', 'Arrival Date', 'Min Price', 'Max Price', 'Modal Price']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing expected column '{col}' in CSV data for {date_str}")
            return

    # Filter for selected mandis
    df_filtered = df[df['Market Name'].isin(MANDIS)]

    for idx, row in df_filtered.iterrows():
        # Skip rows with missing critical data
        if pd.isna(row['Market Name']) or pd.isna(row['Commodity']) or pd.isna(row['Arrival Date']):
            logger.warning(f"Skipping row {idx} due to missing critical data")
            continue

        try:
            arrival_date = datetime.strptime(row['Arrival Date'], '%d-%b-%Y').date()
        except Exception as e:
            logger.warning(f"Skipping row {idx} due to invalid arrival date format: {row['Arrival Date']}")
            continue

        try:
            min_price = float(row['Min Price']) if pd.notna(row['Min Price']) else None
            max_price = float(row['Max Price']) if pd.notna(row['Max Price']) else None
            modal_price = float(row['Modal Price']) if pd.notna(row['Modal Price']) else None
        except Exception as e:
            logger.warning(f"Skipping row {idx} due to invalid price data: {e}")
            continue

        market_price = MarketPrice(
            mandi=row['Market Name'],
            crop=row['Commodity'],
            variety=row['Variety'],
            arrival_date=arrival_date,
            min_price=min_price,
            max_price=max_price,
            modal_price=modal_price
        )
        db.session.add(market_price)

    try:
        db.session.commit()
        logger.info(f"Market prices for {date_str} imported successfully.")
    except Exception as e:
        logger.error(f"Failed to commit market prices for {date_str} to database: {e}")
        db.session.rollback()

if __name__ == "__main__":
    today_str = datetime.today().strftime('%Y%m%d')
    fetch_and_parse_agmarknet(today_str)
