# ParkoBuddy - Parking Management System

A Flask-based web application for managing parking spaces across different regions in Delhi. ParkoBuddy helps users find available parking spots and allows parking space owners to manage their inventory efficiently.

## Features

- **User Authentication**: Secure signup and login system with unique user IDs sent via email
- **Parking Search**: Browse available parking spaces by region:
  - Central Delhi
  - Old Delhi
  - South Delhi
- **Real-time Availability**: Check total spaces, occupied spaces, and vacant spots
- **Parking Management**: Owners can:
  - Add new parking locations
  - Remove existing parking spaces
  - View detailed information about their parking lots
- **Email Notifications**: Automated email system for sending unique user IDs
- **Multi-region Support**: Manage parking data across different Delhi regions

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML/CSS (Templates)
- **Email Service**: Office 365 SMTP

## Project Structure

```
parkobuddy-Flask/
├── app.py              # Main Flask application with all routes
├── templates/          # HTML templates for UI
│   ├── index.html     # Home page
│   ├── login.html     # Login page
│   ├── signup.html    # User registration
│   ├── user.html      # User dashboard
│   ├── data.html      # Parking data display
│   ├── data2.html     # User's parking lots
│   ├── add-new.html   # Add new parking location
│   ├── remove.html    # Remove parking location
│   ├── success.html   # Operation success page
│   └── success1.html  # Deletion success page
├── static/            # Static files (CSS, JavaScript)
└── requirements.txt   # Python dependencies
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jainrochak05/parkobuddy-Flask.git
   cd parkobuddy-Flask
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Required packages:
   - Flask
   - mysql-connector-python

3. **Configure Database**:
   Update the MySQL connection details in `app.py`:
   ```python
   mydb = mysql.connector.connect(
     host="your_host",
     port="3306",
     user="your_user",
     password="your_password",
     database="your_database"
   )
   ```

4. **Configure Email Service**:
   Update the email credentials in `app.py`:
   ```python
   server.login('your_email@outlook.com', 'your_password')
   ```

5. **Create Database Tables**:
   Create the following tables in your MySQL database:
   - `users`: Store user information (u_id, username, password)
   - `centd`: Central Delhi parking data
   - `od`: Old Delhi parking data
   - `sd`: South Delhi parking data
   
   Each parking table should have columns: Location, total, inuse, own_id, p_id

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```
   The app will run at `http://0.0.0.0:5000`

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:5000`

3. **User Operations**:
   - **Signup**: Create a new account and receive a unique ID via email
   - **Login**: Use your username, password, and unique ID to log in
   - **Browse Parking**: Search for available parking in different regions
   - **Manage Parking**: Add or remove parking spaces (for owners)

## API Routes

- `GET/POST /` - Home page and parking search
- `GET/POST /signup` - User registration
- `GET/POST /login` - User login
- `GET/POST /user` - User dashboard and owner parking management
- `GET/POST /new` - Add new parking location
- `GET/POST /remove` - Remove parking location

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  u_id INT PRIMARY KEY,
  username VARCHAR(255),
  password VARCHAR(255)
);
```

### Parking Tables (centd, od, sd)
```sql
CREATE TABLE centd (
  Location VARCHAR(255),
  total INT,
  inuse INT,
  own_id INT,
  p_id INT PRIMARY KEY
);
```


**For production use, please**:
2. Implement proper SQL parameterization
3. Add input validation and sanitization
4. Use a secure secrets management system
5. Implement proper error handling
6. Add CSRF protection
7. Use password hashing (bcrypt/argon2)

## Future Enhancements

- [ ] Real-time parking space updates
- [ ] Payment integration
- [ ] Mobile app support
- [ ] Map integration (Google Maps API)
- [ ] User ratings and reviews
- [ ] Reservation system
- [ ] Analytics dashboard
- [ ] Multi-city support
- [ ] OCR for license plate recognition
- [ ] SMS notifications

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Author

**Rochak Jain** - [GitHub Profile](https://github.com/jainrochak05)

## Contact

For queries or suggestions, feel free to reach out!!!

---

**Note**: This is an educational project. For production deployment, ensure proper security measures are implemented.
