# config.py

from pathlib import Path
from typing import Dict

DATASET_ROOT_PATH = str(Path(__file__).parent.parent / "dataset")
QUERIES_ROOT_PATH = str(Path(__file__).parent.parent / "queries")
QUERY_RESULTS_ROOT_PATH = str(Path(__file__).parent.parent / "tests/query_results")
PUBLIC_HOLIDAYS_URL = "https://date.nager.at/api/v3/publicholidays"
SQLITE_BD_ABSOLUTE_PATH = str(Path(__file__).parent.parent / "olist.db")


def get_csv_to_table_mapping() -> Dict[str, str]:
    return dict(
        [
            ("olist_orders_dataset.csv", "olist_orders"),
            ("olist_customers_dataset.csv", "olist_customers"),
            ("olist_geolocation_dataset.csv", "olist_geolocation"),
            ("olist_order_items_dataset.csv", "olist_order_items"),
            ("olist_order_payments_dataset.csv", "olist_order_payments"),
            ("olist_order_reviews_dataset.csv", "olist_order_reviews"),
            ("olist_products_dataset.csv", "olist_products"),
            ("olist_sellers_dataset.csv", "olist_sellers"),
            ("product_category_name_translation.csv", "product_category_name_translation"),
        ]
    )