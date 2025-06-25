# Django Pricing Module

A Django-based pricing module with REST API, JWT authentication, and admin logging.

---

## Features

- Manage pricing configurations via Django admin
- Custom admin actions and detailed change logging
- REST API endpoint for price calculation
- JWT authentication for secure API access
- Unit tests for core functionality

---

## Project Structure

```
pricing-module/
├── pricing_project/
│   ├── pricing/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   ├── pricing_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── db.sqlite3
├── venv/
├── requirements.txt
└── README.md
```

---

## Installation & Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/Sky2709/pricing_module.git
    cd pricing-module
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```bash
    cd pricing_project
    ..\venv\Scripts\python.exe manage.py migrate
    ```

5. **Create a superuser (for admin access)**
    ```bash
    ..\venv\Scripts\python.exe manage.py createsuperuser
    ```

6. **Run the development server**
    ```bash
    ..\venv\Scripts\python.exe manage.py runserver
    ```

7. **Access the admin panel**
    - Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Creating a Pricing Configuration

1. **Login to Django Admin**
    - Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with your superuser credentials.

2. **Add a PricingConfig**
    - In the sidebar, click on **Pricing Configs**.
    - Click **Add Pricing Config**.

3. **Fill in the fields:**
    - **Name:** e.g., `Weekday Pricing`
    - **Is active:** Check this box to enable the config.
    - **Days of week:** Select days (e.g., 1 for Monday, 2 for Tuesday, etc.).
    - **Base distance:** e.g., `3`
    - **Base price:** e.g., `80`
    - **Additional distance price:** e.g., `30`
    - **Time multipliers:**  
      Example (as JSON):
      ```json
      [
        {"threshold": 60, "multiplier": 1.0},
        {"threshold": 120, "multiplier": 1.25},
        {"threshold": 180, "multiplier": 2.2}
      ]
      ```
    - **Free waiting minutes:** e.g., `3`
    - **Waiting charge per interval:** e.g., `5`
    - **Waiting charge interval:** e.g., `3`

4. **Save**
    - Click **Save**. Your new config will be active and available for API calculations.

---

## API Usage

### **JWT Authentication**

1. **Obtain a JWT Token**

    Send a POST request to `/api/token/` with your Django username and password:
    ```json
    {
      "username": "your_admin_username",
      "password": "your_admin_password"
    }
    ```
    **Response:**
    ```json
    {
      "refresh": "your-refresh-token",
      "access": "your-access-token"
    }
    ```

2. **Use the Token in API Requests**

    Add this header to your API requests:
    ```
    Authorization: Bearer your-access-token
    ```

---

### **Calculate Price Endpoint**

- **URL:** `POST /pricing/api/calculate-price/`
- **Headers:**  
  - `Content-Type: application/json`
  - `Authorization: Bearer <your-access-token>`
- **Example payload:**
    ```json
    {
      "distance": 10,
      "total_ride_time": 30,
      "waiting_time": 5,
      "day_of_week": 2
    }
    ```
- **Example response:**
    ```json
    {
      "total_price": 120.0,
      "breakdown": {
        "distance_price": 90.0,
        "time_price": 30.0,
        "waiting_charge": 0.0
      },
      "config_used": "Weekday Pricing"
    }
    ```

---

## Running Tests

- **Run all tests**
    ```bash
    ..\venv\Scripts\python.exe manage.py test
    ```

- **Run tests for a specific app**
    ```bash
    ..\venv\Scripts\python.exe manage.py test pricing
    ```

---

## Checking Project Health

- **Check for configuration issues**
    ```bash
    ..\venv\Scripts\python.exe manage.py check
    ```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

---

## License

MIT License

---

## Support

For any issues, please open an issue on GitHub or contact
