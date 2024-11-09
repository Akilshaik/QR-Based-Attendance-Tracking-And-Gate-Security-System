# GateVise

## Overview

This repository contains a web application developed using Flask for managing and tracking user entry and exit times through QR code scanning. The application is designed to handle multiple roles such as Admin, Security Guard, and Users, providing different levels of access and functionality.

## Features

- **User Registration and Authentication:**
  - Users can register with personal details and generate a unique QR code for their profile.
  - Secure login using hashed passwords.

- **Admin Panel:**
  - Admin can manage users, security guards, and visitors.
  - Admin panel implemented using Flask-Admin for easy management.

- **QR Code Generation and Scanning:**
  - Generate unique QR codes for registered users.
  - Two cameras are set up for scanning QR codes for entry and exit.
  - Scanned QR codes log entry and exit times automatically.

- **Role-Based Access:**
  - Separate login pages for Admin, Security Guards, and Users.
  - Different dashboards and functionalities based on the role.

- **Visitor Management:**
  - Form for visitor registration capturing basic details and entry time.

## Technology Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Admin, MySQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Libraries:** OpenCV, Pyzbar, Qrcode, Bcrypt

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Akilshaik/GateVise.git
    cd qr-code-entry-exit-system
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    - Ensure MySQL is installed and running.
    - Create a database named `db` and update the database URI in the code if necessary.

5. **Run the application:**
    ```bash
    flask run
    ```

## Usage

1. **Register as a User:**
   - Navigate to the registration page and fill out the form to create a new user account.
   - A unique QR code is generated for the user upon registration.

2. **Admin and Security Guard Registration:**
   - Admin can register and manage security guards through the admin panel.
   - Security guards can log in and access the security dashboard.

3. **Scanning QR Codes:**
   - Use the provided camera setup to scan QR codes for users entering and exiting.
   - The application logs the entry and exit times automatically.

4. **Visitor Management:**
   - Visitors can register their details and log their entry times using the visitor registration form.

## Contributing

We welcome contributions from the community. If you have suggestions, bug reports, or improvements, please open an issue or submit a pull request. Make sure to follow the contribution guidelines.



## Contact

For any questions or suggestions, feel free to contact me at akilshaikh4161@gmail.com .
