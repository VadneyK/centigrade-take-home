
# Store API Microservice

A FastAPI-based microservice for managing a store's customers, products, and orders with JWT authentication.

## Project Structure

```

centigrade-take-home/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── database.py
│   ├── crud.py
│   └── auth.py
├── alembic/
│   └── versions/
├── requirements.txt
├── alembic.ini
└── README.md
```

## Prerequisites

- Python 3.8+ <3.13 (Pydantic has issues with 3.13)
- PostgreSQL
- pip (Python package installer)

## Environment Setup

1. Copy the example environment file:

```
bash
cp .env.example .env
```

2. Update the values in `.env` with your configuration:

- `DATABASE_URL`: Your PostgreSQL connection string
- `SECRET_KEY`: A secure secret key for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/VadneyK/centigrade-take-home.git
cd centigrade-take-home
```

2. Create and activate virtual environment

```bash
# On Windows
python3.12 -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3.12 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Start and set up PostgreSQL

```bash
# start database
brew services start postgresql
# Create a new PostgreSQL user (if needed)
createuser -s postgres
# Create the database
createdb store_db
```

5. Configure Database Connection

- Open `app/database.py`
- Update `SQLALCHEMY_DATABASE_URL` if needed:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/store_db"
```

## Construct the URL:

Run the following command to connect to PostgreSQL:

```bash
psql postgres
```

### Then in `psql`:

To try to connect to the `store_db`, run:

```bash
\c store_db    # Try to connect to store_db
```

To view your current connection details, run:

```bash
\conninfo      # This will show your current connection details
```

The `\conninfo` command will display output similar to:

```
You are connected to database "store_db" as user "yourusername" via socket in "/tmp" at port "5432"
```

Use this information to construct your URL.

6. Initialize and Run Migrations

```bash
# Initialize alembic
alembic init alembic

# Update your alembic.ini file to use the correct database URL. Find the line with sqlalchemy.url and update it to match your database.py

# Generate initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

7. Start the Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, you can access:

- Swagger UI Documentation: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

## Available Endpoints

### Authentication

- `POST /token`
  - Login and obtain JWT token
  - Required fields: username (email), password

### Customers

- `POST /customers/`
  - Create new customer
  - Required fields: email, full_name, password
- `GET /customers/{customer_id}`
  - Get customer details

### Products

- `POST /products/`
  - Create new product
  - Required fields: name, description, price

### Orders

- `POST /orders/`
  - Create new order
  - Required fields: customer_id, total_amount, product_ids

## Testing the API

1. Create a customer (public endpoint):

```bash
curl -X 'POST' \
  'http://localhost:8000/customers/' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "test@example.com",
  "full_name": "Test User",
  "password": "password123"
}'
```

2. Get authentication token (public endpoint):

```bash
curl -X 'POST' \
  'http://localhost:8000/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=test@example.com&password=password123'
```

The response will include your access token:

```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
```

3. Create a product (protected endpoint):

```bash
curl -X 'POST' \
  'http://localhost:8000/products/' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Test Product",
  "description": "Test Description",
  "price": 99.99
}'
```

4. Create an order (protected endpoint):

```bash
curl -X 'POST' \
  'http://localhost:8000/orders/' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer_id": 1,
  "total_amount": 99.99,
  "product_ids": [1]
}'
```

5. Get customer details (protected endpoint):

```bash
curl -X 'GET' \
  'http://localhost:8000/customers/1' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

## Authentication Notes

- Only customer creation (`POST /customers/`) and login (`POST /token`) endpoints are public
- All other endpoints require a valid JWT token in the Authorization header
- Tokens expire after 30 minutes
- Orders can only be created for the authenticated customer
- Replace `YOUR_ACCESS_TOKEN` with the token received from the login endpoint

## Database UML Scheme

```mermaid
classDiagram
    class Customer {
        +int id
        +string email
        +string hashed_password
        +string full_name
    }
  
    class Product {
        +int id
        +string name
        +string description
        +float price
    }
  
    class Order {
        +int id
        +int customer_id
        +datetime order_date
        +float total_amount
    }
  
    class OrderProducts {
        +int order_id
        +int product_id
        +int quantity
    }
  
    Customer "1" -- "*" Order
    Order "*" -- "*" Product
    OrderProducts -- Order
    OrderProducts -- Product
```

## Implementation Features

- FastAPI REST API with automatic OpenAPI documentation
- PostgreSQL database with SQLAlchemy ORM
- Pydantic models for request/response validation
- JWT authentication for secure endpoints
- Database migrations using Alembic
- Many-to-many relationship between orders and products
- CRUD operations for all entities
- Error handling and input validation

## Development

To run the application in development mode with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Security Notes

- The default SECRET_KEY in auth.py should be changed in production
- Database credentials should be stored in environment variables
- CORS settings should be configured based on your requirements
