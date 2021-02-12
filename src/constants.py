# Table names
TABLE_NAMES = ["courier", "product", "customer", "transaction", "basket"]

# Table keys
TABLE_KEYS = {
    "COURIER_KEYS": ["courier_id", "courier_name", "courier_phone"],
    "PRODUCT_KEYS": ["product_id", "product_name", "product_price"],
    "CUSTOMER_KEYS": [
        "customer_id",
        "customer_name",
        "customer_address",
        "customer_phone",
    ],
    "TRANSACTION_KEYS": [
        "transaction_id",
        "transaction_time",
        "customer_id",
        "courier_id",
        "transaction_status",
    ],
    "BASKET_KEYS": ["basket_id", "transaction_id", "product_id", "basket_amount"],
}


# Variable python types
VARIABLE_PYTHON_TYPES = {
    "id": int,
    "name": str,
    "phone": int,
    "price": float,
    "time": str,
    "address": str,
    "status": str,
    "amount": int,
}

# Variable MySQL types
VARIABLE_DB_TYPES = {
    "id": "int",
    "name": "varchar(255)",
    "phone": "varchar(15)",
    "price": "decimal(10,2)",
    "time": "datetime",
    "address": "varchar(255)",
    "status": "varchar(30)",
    "amount": "int",
}