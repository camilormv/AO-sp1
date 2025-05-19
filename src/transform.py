from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

import pandas as pd
from pandas import DataFrame, read_sql
from sqlalchemy import text
from sqlalchemy.engine.base import Engine

from src.config import QUERIES_ROOT_PATH

QueryResult = namedtuple("QueryResult", ["query", "result"])

class QueryEnum(Enum):
    DELIVERY_DATE_DIFFERECE = "delivery_date_difference"
    GLOBAL_AMMOUNT_ORDER_STATUS = "global_ammount_order_status"
    REVENUE_BY_MONTH_YEAR = "revenue_by_month_year"
    REVENUE_PER_STATE = "revenue_per_state"
    TOP_10_LEAST_REVENUE_CATEGORIES = "top_10_least_revenue_categories"
    TOP_10_REVENUE_CATEGORIES = "top_10_revenue_categories"
    REAL_VS_ESTIMATED_DELIVERED_TIME = "real_vs_estimated_delivered_time"
    ORDERS_PER_DAY_AND_HOLIDAYS_2017 = "orders_per_day_and_holidays_2017"
    GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP = "get_freight_value_weight_relationship"

def read_query(query_name: str) -> str:
    with open(f"{QUERIES_ROOT_PATH}/{query_name}.sql", "r") as f:
        sql_file = f.read()
        sql = text(sql_file)
    return sql

def query_delivery_date_difference(database: Engine) -> QueryResult:
    query_name = QueryEnum.DELIVERY_DATE_DIFFERECE.value
    query = read_query(QueryEnum.DELIVERY_DATE_DIFFERECE.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_global_ammount_order_status(database: Engine) -> QueryResult:
    query_name = QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value
    query = read_query(QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_revenue_by_month_year(database: Engine) -> QueryResult:
    query_name = QueryEnum.REVENUE_BY_MONTH_YEAR.value
    query = read_query(QueryEnum.REVENUE_BY_MONTH_YEAR.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_revenue_per_state(database: Engine) -> QueryResult:
    query_name = QueryEnum.REVENUE_PER_STATE.value
    query = read_query(QueryEnum.REVENUE_PER_STATE.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_top_10_least_revenue_categories(database: Engine) -> QueryResult:
    query_name = QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value
    query = read_query(QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_top_10_revenue_categories(database: Engine) -> QueryResult:
    query_name = QueryEnum.TOP_10_REVENUE_CATEGORIES.value
    query = read_query(QueryEnum.TOP_10_REVENUE_CATEGORIES.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_real_vs_estimated_delivered_time(database: Engine) -> QueryResult:
    query_name = QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value
    query = read_query(QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_freight_value_weight_relationship(database: Engine) -> QueryResult:
    query_name = QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value

    # Get orders from olist_orders table
    orders = read_sql("SELECT * FROM olist_orders", database)
    # Get items from olist_order_items table
    items = read_sql("SELECT * FROM olist_order_items", database)
    # Get products from olist_products table
    products = read_sql("SELECT * FROM olist_products", database)

    # Merge items with orders on order_id, then merge with products on product_id
    data = pd.merge(items, orders, on="order_id", how="inner")
    data = pd.merge(data, products, on="product_id", how="inner")

    # Filter only delivered orders
    delivered = data[data["order_status"] == "delivered"]

    # For each order, sum freight_value and product_weight_g
    aggregations = delivered.groupby("order_id")[["freight_value", "product_weight_g"]].sum().reset_index()

    return QueryResult(query=query_name, result=aggregations)

# src/transform.py
from pandas import read_sql, to_datetime
import pandas as pd

def query_orders_per_day_and_holidays_2017(database) -> QueryResult:
    """
    Build a table with number of orders per day during 2017 and
    a Boolean that tells whether the day was a public holiday.
    Columns returned: order_count | date | holiday
    """
    query_name = QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value

    # 1. Read tables ---------------------------------------------------------
    holidays = read_sql("SELECT * FROM public_holidays", database)
    orders   = read_sql("SELECT * FROM olist_orders", database)

    # 2. Convert the purchase timestamp to datetime and keep only 2017 -------
    orders["order_purchase_timestamp"] = to_datetime(
        orders["order_purchase_timestamp"]
    )
    orders_2017 = orders[orders["order_purchase_timestamp"].dt.year == 2017]

    # 3. Create a pure-date column and aggregate -----------------------------
    orders_2017["date"] = orders_2017["order_purchase_timestamp"].dt.date
    daily = (
        orders_2017.groupby("date")
                   .size()
                   .reset_index(name="order_count")
    )

    # 4. Mark holidays -------------------------------------------------------
    # holidays['date'] column is already datetime -> turn to date objects
    holidays_set = set(to_datetime(holidays["date"]).dt.date)
    daily["holiday"] = daily["date"].apply(lambda d: d in holidays_set)

    # 5. Return in requested order -------------------------------------------
    result_df = daily[["order_count", "date", "holiday"]]

    return QueryResult(query=query_name, result=result_df)

def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    return [
        query_delivery_date_difference,
        query_global_ammount_order_status,
        query_revenue_by_month_year,
        query_revenue_per_state,
        query_top_10_least_revenue_categories,
        query_top_10_revenue_categories,
        query_real_vs_estimated_delivered_time,
        query_orders_per_day_and_holidays_2017,
        query_freight_value_weight_relationship,
    ]

def run_queries(database: Engine) -> Dict[str, DataFrame]:
    query_results = {}
    for query in get_all_queries():
        query_result = query(database)
        query_results[query_result.query] = query_result.result
    return query_results