# Dash Django Template

**Dash Django Template** is a repository created to provide a skeleton for building Dash applications that utilize Django's powerful Object Relational Mapper (ORM) for database management. This template aims to combine the rapid development and flexibility of Dash with the robust, scalable, and well-structured capabilities of Django.

## Why this template?

After experimenting extensively with both Dash and Django, it became evident that Django is an excellent choice for creating robust and scalable web applications. However, for smaller-scale projects that need to be developed quickly, Dash stands out with its ease of use, callback management, and the ability to design layouts entirely in Python. 

By integrating Django's ORM with Dash's simplicity, this template allows developers to:
- Quickly create dynamic and visually appealing Dash applications.
- Leverage Django's ORM for scalable, maintainable database schema design and management.
- Lay the foundation for projects that can grow over time without sacrificing maintainability.

## Features
- **Dash for front-end layouts and interactivity.**
- **Django ORM for database communication and schema design.**
- **Ready-to-use skeleton for efficient development.**

## Getting Started

### Prerequisites

- Python 3.8+ (preferably the latest version)
- pip (Python package manager)

### Setting up the Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dash-django-template.git
   cd dash-django-template
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Database Selection 
Database is configurable throught the django settings module (django_db/settings.py)
. Default database is sqlite.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # or os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

``` 

Here is an example of configuration for a local MySQL server.
```
# MYSQL Server (local host)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',  # Use the database host (e.g., IP or hostname)
        'PORT': '3306',       # MySQL default port
    }
} 
```


#### Running the migrations (first time and when django models are changed) and the application

1. Apply the initial migrations for Django:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Run the development server:
   ```bash
   python manage.py runserver
   ```

3. Run one of the examples: 
    ```bash
    python dash_app_download_edit.py
    ```

3. Open the application in your browser at `http://127.0.0.1:8000`.



## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
Thank you Chat-GPT.

