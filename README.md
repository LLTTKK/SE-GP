# HKMU Food Ordering System

A Python-based desktop application for food ordering and delivery management, specifically designed for HKMU students and restaurants.(You Need to SignUp all the account then use)

## Features

### 1. User Authentication & Roles
- **Login and Sign-up System**
  - Multiple user roles:
    - Customers (HKMU students only)
    - Restaurant Staff
    - Restaurant Owners
    - Delivery Staff
    - Customer Service Staff
  - Email verification system
  - HKMU email domain validation (@live.hkmu.edu.hk)

### 2. Restaurant Management
- Scrollable restaurant listing
- Restaurant profile management
- Menu management for restaurant staff/owners
  - Add new menu items
  - Edit existing items
  - Delete menu items
- Restaurant details including name, description, and address

### 3. Order Management
- Shopping cart functionality
- Multiple payment methods:
  - Credit Card
  - PayPal
  - Apple Pay
  - Google Pay
- Order tracking system
- Delivery status updates
- Order history for customers

### 4. Delivery System
- Order acceptance/rejection by delivery staff
- Real-time delivery status updates
- Delivery address management
- Order completion confirmation

### 5. Customer Service
- Live chat support
- User account management
- Order monitoring and management
- Customer support ticket system

## Technical Requirements

### Prerequisites
- Python 3.x
- Required Python packages:
  ```bash
  pip install tkinter
  pip install pillow
  pip install bcrypt
  ```

### Data Storage
The application uses JSON files for data storage:
- `users.txt`: User account information
- `restaurants.txt`: Restaurant details
- `menu_items.txt`: Menu items for all restaurants
- `orders.txt`: Order information
- `discounts.txt`: Discount information

## Installation

1. Clone the repository:
2. Install required packages:

## Usage

### For Customers
1. Sign up with HKMU email (@live.hkmu.edu.hk)
2. Browse restaurants
3. Add items to cart
4. Place orders
5. Track delivery status

### For Restaurant Staff/Owners
1. Register restaurant
2. Manage menu items
3. View orders
4. Update restaurant information

### For Delivery Staff
1. View available orders
2. Accept/decline deliveries
3. Update delivery status
4. Mark orders as delivered

### For Customer Service
1. Monitor all orders
2. Manage user accounts
3. Handle customer inquiries
4. Access system-wide information

## Security Features
- Password hashing using bcrypt
- Email verification system
- Role-based access control
- Session management

## File Structure

project/
│
├── Food App with require.py
├── users.txt
├── restaurants.txt
├── menu_items.txt
├── orders.txt
└── discounts.txt
