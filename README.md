# Test task FastAPI + RetailCRM API

- Clone the Repository

<pre> git clone https://github.com/nika-doroshkevich/Test_task_RetailCRM_API.git </pre>

- Create .env with RETAILCRM_API_URL and RETAILCRM_API_KEY. Example:

<pre> RETAILCRM_API_URL=https://your.retailcrm.ru/api/v5 </pre>
<pre> RETAILCRM_API_KEY=Oooooaaaaaffffkkkkkkkkkk </pre>

- Build and Run Container

<pre> docker-compose up --build -d </pre>

- Explore the API

<pre> http://localhost:8000/docs </pre>

## Description:

- api -> api_v1 -> customers:
  Retrieve a list of customers from RetailCRM based on optional filters.
  Create a new customer in RetailCRM.
- api -> api_v1 -> orders:
  Retrieve all orders associated with a specific customer.
  Create a new order in RetailCRM.
  Create a payment for an order in RetailCRM.
- filters -> customers:
  Model used to filter customers based on various optional fields.
- funcs -> customers:
  Retrieves a list of customers from RetailCRM using the provided filters.
  Creates a new customer in RetailCRM.
- funcs -> orders:
  Retrieves a list of orders for a specific customer by customer ID.
  Creates a new order in the RetailCRM system.
  Creates a new payment associated with an order in the RetailCRM system.
- schemas -> customers:
  Pydantic models for customers.
- schemas -> orders:
  Pydantic models for customers.
