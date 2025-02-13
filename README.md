# LINCRIDE TEST
# Django Ride Fare API

This is a Django REST API for calculating ride fares based on dynamic pricing factors such as distance, traffic level, demand level, and time of day.

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <project_directory>
   ```

2. Create a Python virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Copy the environment variables file:
   ```sh
   cp .env.example .env
   ```

5. Apply migrations:
   ```sh
   python manage.py migrate
   ```

6. Start the Django development server:
   ```sh
   python manage.py runserver
   ```

## How to Run Tests

Run the following command to execute the test suite:
```sh
python manage.py test
```

## API Endpoint

**Swagger URL**

```
GET /api/schema/swagger-ui/
```

**Calculate Fare**
```
GET /api/calculate-fare/?distance=<value>&traffic_level=<value>&demand_level=<value>
```

### Sample Request
```
GET /api/calculate-fare/?distance=10&traffic_level=high&demand_level=peak
```

### Sample Response
```json
{
  "base_fare": 2.5,
  "distance_fare": 10.0,
  "traffic_multiplier": 1.5,
  "demand_multiplier": 1.8,
  "total_fare": 34.5
}
```