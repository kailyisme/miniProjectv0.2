# mini_project v2
Simple program to manage orders in food retail environment
<br/>
<br/>
## To start
Add .env file to run with the following details
- MYSQL_HOST (address to MySQL server)
- MYSQL_PORT (port to MySQL Server; 3306 default)
- MYSQL_PASSWORD
- MYSQL_USER
- DB (Database name you would like to use for app; no need to pre-initialize it)

On root of the project folder run
* 'python -m venv .venv'
* On windows powershell:
  * '.\.venv\Scripts\Activate.ps1'
* 'python -m pip install -r .\requirements.txt'
* 'docker-compose up -d'
* 'python -m src'
<br/>
<br/>

## ToDo
- [x] Separate logic from file_handlers and UI
- [x] Not depending on pre-existing DB
- [x] SubMenu Functions
    - [x] Show table
    - [x] Add to table
    - [x] Update item on table
    - [x] Remove item from table
- [x] Apply SubMenu to Couriers
- [x] Apply SubMenu to Products
- [x] Apply SubMenu to Customers
- [x] Default empty string to "Null"
- [ ] Validating user input for SubMenu
- [x] Order menu
  <!-- - [ ] Make courier_id and customer_id default to Null when original entries deleted -->
  - [x] Make baskets delete in cascade when original transaction deleted
  - [x] Add uuid for order_id (transaction_id)
  - [x] View orders
  - [x] Add order function
  - [x] Basket menu
    - [x] Show basket for a transaction
    - [ ] Add basket entry
    - [ ] Update basket entry
    - [ ] Remove basket entry
  - [ ] Change order status
  - [ ] Update order details
  - [ ] Remove order
- [ ] Separate menu's logic by file
- [x] Save function / export DB in CSV format
- [ ] Load function / import DB in CSV format
- [x] Commented code
- [ ] Unit tested code
- [ ] Add "deleted" field to courier, products and customer tables
- [ ] List orders by status or couriers
- [ ] Track product inventory
- [x] Save uuid as binary(16) for performance