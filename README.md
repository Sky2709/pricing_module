# Django Pricing Module

A Django-based pricing module with REST API and admin logging.

---

## Features

- Manage pricing configurations via Django admin
- Custom admin actions and change logging
- REST API endpoint for price calculation
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
    Visit (http://127.0.0.1:8000/admin/) to access the admin panel.

---

## API Usage

- **Calculate Price Endpoint:**
    ```
    POST /pricing/api/calculate-price/
    ```
    - Example payload:
      ```json
      {
        "distance": 10,
        "duration": 30,
        "day_of_week": 2,
        "time": "14:00"
      }
      ```
    - Response:
      ```json
      {
        "total_price": 120.0
      }
      ```

---

## Running Tests

1. **Run all tests**
    ```bash
    ..\venv\Scripts\python.exe manage.py test
    ```

2. **Run tests for a specific app**
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
--
**For any issues, please open an issue on GitHub or contact the maintainer.**
