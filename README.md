# Multi-Vendor E-Commerce Application for Skincare Products
#project folders are in Master Branch

## Project Overview
This is a multi-vendor e-commerce application designed to facilitate the sale of skincare products. The platform is built using the Python Django framework and PostgreSQL as the database. The application features three primary user roles:

1. **Customers** - Can browse products, manage their cart, checkout, and make payments.
2. **Vendors** - Can manage their products, handle orders, and manage subcategories.
3. **Admin** - Oversees the platform, manages users, approves vendors, and manages categories.

---

## Project Structure
The repository contains the following main folders:

### 1. **lushaura**
   - The core app that integrates all components of the project.
   - Handles configurations, settings, and primary functionality.

### 2. **user_management**
   - Manages authentication and user-related operations.
   - Features include user login, registration, and admin functionalities.

### 3. **customer**
   - Focuses on customer-specific features such as:
     - Shopping and browsing products.
     - Cart management.
     - Profile management.
     - Checkout and payment processes.

### 4. **vendor**
   - Handles vendor-related functionality, including:
     - Adding and managing products.
     - Managing orders.
     - Subcategory management.

---

## Key Features

### Customers
- Browse products and add to cart.
- Manage user profile.
- Checkout and pay for orders.
- View order history.

### Vendors
- Add and edit product details.
- Manage orders received from customers.
- Organize products into subcategories.

### Admin
- Approve vendor registrations.
- Manage product categories and subcategories.
- Oversee platform operations to ensure smooth functionality.

---

## Technical Details
- **Framework:** Python Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Django ORM for database management

---

## Folder Structure

```
project_root/
|
|-- lushaura/                # Main application directory
|-- customer/                # Customer-related app
|-- user_management/         # Authentication and user management
|-- vendor/                  # Vendor-related app
|-- templates/               # HTML templates
|-- static/                  # Static files (CSS, JavaScript, images)
|-- db.sqlite3               # Development database (replace with PostgreSQL in production)
|-- manage.py                # Django project management file
```

---

## How to Run the Project

### Prerequisites
- Python 3.x
- PostgreSQL
- Django (latest version)
- Virtual environment (optional but recommended)

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:
   ```bash
   cd your-repository
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database and update the `settings.py` file with the database credentials.

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`.

---


---



---

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

---



