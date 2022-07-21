# Currency Converter 

## Introduction
This is a currency converter build using the FASTAPI framework. It consists simple API that converts from one currency to another,
get historical rates of currencies. This project supports JWT Authorization and makes use of fixer.io for getting the exchange rates.

# How to use
1. Clone the repository
2. Ensure docker is installed on your machine and run the command `docker-compose up -d --build `, which sets up the API and the database
3. Visit the browser and navigate to `http://localhost:8002/docs` to view the docs and see the lists of endpoints you have access to.


# Endpoints
- /v1/login/token - Logs a registered user in and returns a valid token
- /v1/user/signup - Creates a new user
- /v1/converter/symbols -  Gets all the available currency symbols
- /v1/converter/rates - Get all the latest currency rates
- /v1/converter/historical-rates - Get all the historical rates of a currency within a specified timeframe

N.B: All the converter routes required authentication. If using the swagger UI, you can authenticate with a registered user
email and password, then you'd be able to access the protected routes.

# Testing
To run the test, ensure the container has been built and then run `docker-compose exec web pytest`
