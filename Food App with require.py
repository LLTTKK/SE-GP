#Generate me a python windows app ,is food ordering system and tracking system with below function 
#1.Login page , sign up page (include customer page , restaurant's staff and owner page, deleiver food page, customer service staff page)
#2.discount page (store different user's own discount or restaurant's shared discount and allow restaurant's staff or owner edit and send discount to user)
#3.Restaurant (allow user scroll to see different restaurant and the app can auto )
#4.menu page (can scroll to see different food after user select a restaurant , allower restaurant's staff and owner edit menu)

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import bcrypt
import datetime
import json
import os

class FoodOrderingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Food Ordering System")
        self.root.geometry("800x600")
        
        # Initialize data files
        self.init_data_files()
        
        # Initialize shopping cart
        self.cart = []
        
        # Initialize current user info
        self.current_user_id = None
        self.current_user_role = None
        self.current_user_restaurant_id = None
        
        # Start with login page
        self.show_login_page()
        
    def init_data_files(self):
        # Initialize user data file
        if not os.path.exists('users.txt'):
            with open('users.txt', 'w') as f:
                json.dump([], f)
                
        # Initialize restaurant data file  
        if not os.path.exists('restaurants.txt'):
            default_restaurants = [
                {"id": 1, "name": "Pizza Palace", "description": "Best pizza in town", "address": "123 Pizza St"},
                {"id": 2, "name": "Burger King", "description": "Flame grilled burgers", "address": "456 Burger Ave"},
                {"id": 3, "name": "Sushi Express", "description": "Fresh sushi daily", "address": "789 Sushi Rd"}
            ]
            with open('restaurants.txt', 'w') as f:
                json.dump(default_restaurants, f)
                
        # Initialize menu items file
        if not os.path.exists('menu_items.txt'):
            with open('menu_items.txt', 'w') as f:
                json.dump([], f)
                
        # Initialize discounts file
        if not os.path.exists('discounts.txt'):
            with open('discounts.txt', 'w') as f:
                json.dump([], f)

        # Initialize orders file
        if not os.path.exists('orders.txt'):
            with open('orders.txt', 'w') as f:
                json.dump([], f)

    def show_login_page(self):
        self.clear_window()
        
        # Login frame
        login_frame = ttk.Frame(self.root)
        login_frame.pack(pady=50)
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, pady=5)
        username_entry = ttk.Entry(login_frame)
        username_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=5)
        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        ttk.Button(login_frame, text="Login", 
                  command=lambda: self.login(username_entry.get(), password_entry.get())
                  ).grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(login_frame, text="Sign Up", 
                  command=self.show_signup_page
                  ).grid(row=3, column=0, columnspan=2)

    def show_signup_page(self):
        self.clear_window()
        
        signup_frame = ttk.Frame(self.root)
        signup_frame.pack(pady=50)
        
        ttk.Label(signup_frame, text="Username:").grid(row=0, column=0, pady=5)
        username_entry = ttk.Entry(signup_frame)
        username_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(signup_frame, text="Password:").grid(row=1, column=0, pady=5)
        password_entry = ttk.Entry(signup_frame, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(signup_frame, text="Email:").grid(row=2, column=0, pady=5)
        email_entry = ttk.Entry(signup_frame)
        email_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(signup_frame, text="Role:").grid(row=3, column=0, pady=5)
        role_var = tk.StringVar()
        roles = ['Customer', 'Restaurant Staff', 'Restaurant Owner', 'Delivery Staff', 'Customer Service']
        role_dropdown = ttk.Combobox(signup_frame, textvariable=role_var, values=roles)
        role_dropdown.grid(row=3, column=1, pady=5)

        # Add restaurant fields that show only for restaurant roles
        restaurant_frame = ttk.Frame(signup_frame)
        restaurant_frame.grid(row=4, column=0, columnspan=2, pady=5)
        restaurant_frame.grid_remove()

        ttk.Label(restaurant_frame, text="Restaurant Name:").grid(row=0, column=0, pady=5)
        restaurant_name_entry = ttk.Entry(restaurant_frame)
        restaurant_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(restaurant_frame, text="Restaurant Description:").grid(row=1, column=0, pady=5)
        restaurant_desc_entry = ttk.Entry(restaurant_frame)
        restaurant_desc_entry.grid(row=1, column=1, pady=5)

        def on_role_change(*args):
            if role_var.get() in ['Restaurant Staff', 'Restaurant Owner']:
                restaurant_frame.grid()
            else:
                restaurant_frame.grid_remove()

        role_var.trace('w', on_role_change)
        
        def validate_and_signup():
            email = email_entry.get()
            role = role_var.get()
            
            # Check if customer email is valid HKMU email
            if role == 'Customer' and not email.endswith('@live.hkmu.edu.hk'):
                messagebox.showerror("Error", "You are not HKMU student, only HKMU student are allow to use the app")
                return
                
            self.signup(username_entry.get(),
                       password_entry.get(),
                       email,
                       role,
                       restaurant_name_entry.get(),
                       restaurant_desc_entry.get())
        
        ttk.Button(signup_frame, text="Sign Up",
                  command=validate_and_signup
                  ).grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(signup_frame, text="Back to Login",
                  command=self.show_login_page
                  ).grid(row=6, column=0, columnspan=2)

    def show_delivery_orders(self):
        self.clear_window()
        
        orders_frame = ttk.Frame(self.root)
        orders_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(orders_frame, text="Available Orders for Delivery", font=('Helvetica', 16, 'bold')).pack()
        
        # Add sign out button
        ttk.Button(orders_frame, text="Sign Out", command=self.sign_out).pack(anchor="ne")
        
        try:
            with open('orders.txt', 'r') as f:
                all_orders = json.load(f)
                available_orders = [order for order in all_orders if order['status'] == 'delivering' and not order.get('delivery_staff_id')]
                my_deliveries = [order for order in all_orders if order.get('delivery_staff_id') == self.current_user_id and order['status'] == 'out_for_delivery']
        except:
            available_orders = []
            my_deliveries = []
            
        # Show available orders
        if available_orders:
            ttk.Label(orders_frame, text="\nAvailable Orders:", font=('Helvetica', 12, 'bold')).pack(anchor="w")
            for order in available_orders:
                order_frame = ttk.Frame(orders_frame, relief="solid", borderwidth=1)
                order_frame.pack(fill=tk.X, pady=10, padx=5)
                
                # Get restaurant info
                with open('restaurants.txt', 'r') as f:
                    restaurants = json.load(f)
                restaurant = next((r for r in restaurants if r['id'] == order['items'][0]['restaurant_id']), None)
                
                # Get customer info
                with open('users.txt', 'r') as f:
                    users = json.load(f)
                customer = next((u for u in users if u['id'] == order['user_id']), None)
                
                # Check if restaurant has an address
                restaurant_address = restaurant.get('address', 'Address not available')
                
                order_info = f"Order #{order['id']} - {order['date']}\n"
                order_info += f"Restaurant: {restaurant['name']} ({restaurant_address})\n"
                order_info += f"Customer: {customer['username']}\n"
                order_info += f"Total: ${order['total']:.2f}"
                
                ttk.Label(order_frame, text=order_info).pack(side=tk.LEFT, padx=5)
                
                button_frame = ttk.Frame(order_frame)
                button_frame.pack(side=tk.RIGHT, padx=5)
                
                ttk.Button(button_frame, text="View Details",
                          command=lambda o=order: self.show_order_details(o)).pack(side=tk.LEFT, padx=2)
                          
                ttk.Button(button_frame, text="Accept",
                          command=lambda o=order: self.accept_delivery(o['id'])).pack(side=tk.LEFT, padx=2)
                          
                ttk.Button(button_frame, text="Decline",
                          command=lambda o=order: self.decline_delivery(o['id'])).pack(side=tk.LEFT, padx=2)
        
        # Show my deliveries
        if my_deliveries:
            ttk.Label(orders_frame, text="\nMy Current Deliveries:", font=('Helvetica', 12, 'bold')).pack(anchor="w", pady=(20,10))
            for order in my_deliveries:
                order_frame = ttk.Frame(orders_frame, relief="solid", borderwidth=1)
                order_frame.pack(fill=tk.X, pady=10, padx=5)
                
                # Get restaurant and customer info
                with open('restaurants.txt', 'r') as f:
                    restaurants = json.load(f)
                restaurant = next((r for r in restaurants if r['id'] == order['items'][0]['restaurant_id']), None)
                
                with open('users.txt', 'r') as f:
                    users = json.load(f)
                customer = next((u for u in users if u['id'] == order['user_id']), None)
                
                order_info = f"Order #{order['id']} - {order['date']}\n"
                order_info += f"Restaurant: {restaurant['name']}\n"
                order_info += f"Customer: {customer['username']}\n"
                order_info += f"Total: ${order['total']:.2f}"
                
                ttk.Label(order_frame, text=order_info).pack(side=tk.LEFT, padx=5)
                
                ttk.Button(order_frame, text="Mark as Delivered",
                          command=lambda o=order: self.mark_as_delivered(o['id'])).pack(side=tk.RIGHT, padx=5)
                
        if not available_orders and not my_deliveries:
            ttk.Label(orders_frame, text="No orders available for delivery yet").pack(pady=20)

    def mark_as_delivered(self, order_id):
        try:
            with open('orders.txt', 'r') as f:
                orders = json.load(f)
                
            for order in orders:
                if order['id'] == order_id:
                    order['status'] = 'Finished'
                    break
                    
            with open('orders.txt', 'w') as f:
                json.dump(orders, f)
                
            messagebox.showinfo("Success", "Order marked as delivered!")
            self.show_delivery_orders()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update order status: {e}")

    def show_order_details(self, order):
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Order #{order['id']} Details")
        details_window.geometry("400x400")
        
        # Get restaurant info
        with open('restaurants.txt', 'r') as f:
            restaurants = json.load(f)
        restaurant = next((r for r in restaurants if r['id'] == order['items'][0]['restaurant_id']), None)
        
        # Get customer info
        with open('users.txt', 'r') as f:
            users = json.load(f)
        customer = next((u for u in users if u['id'] == order['user_id']), None)
        
        details_frame = ttk.Frame(details_window, padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(details_frame, text="Order Items:", font=('Helvetica', 12, 'bold')).pack(anchor="w")
        for item in order['items']:
            ttk.Label(details_frame, text=f"- {item['name']} (${item['price']:.2f})").pack(anchor="w")
            
        ttk.Label(details_frame, text=f"\nTotal: ${order['total']:.2f}", font=('Helvetica', 12, 'bold')).pack(anchor="w")
        
        ttk.Label(details_frame, text="\nRestaurant Details:", font=('Helvetica', 12, 'bold')).pack(anchor="w")
        ttk.Label(details_frame, text=f"Name: {restaurant['name']}").pack(anchor="w")
        ttk.Label(details_frame, text=f"Address: {restaurant['address']}").pack(anchor="w")
        
        ttk.Label(details_frame, text="\nCustomer Details:", font=('Helvetica', 12, 'bold')).pack(anchor="w")
        ttk.Label(details_frame, text=f"Name: {customer['username']}").pack(anchor="w")
        ttk.Label(details_frame, text=f"Email: {customer['email']}").pack(anchor="w")

    def accept_delivery(self, order_id):
        try:
            with open('orders.txt', 'r') as f:
                orders = json.load(f)
                
            for order in orders:
                if order['id'] == order_id:
                    order['delivery_staff_id'] = self.current_user_id
                    order['status'] = 'out_for_delivery'
                    break
                    
            with open('orders.txt', 'w') as f:
                json.dump(orders, f)
                
            messagebox.showinfo("Success", "Order accepted for delivery!")
            self.show_delivery_orders()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to accept order: {e}")

    def decline_delivery(self, order_id):
        try:
            with open('orders.txt', 'r') as f:
                orders = json.load(f)
                
            for order in orders:
                if order['id'] == order_id:
                    order['declined_by'] = self.current_user_id
                    break
                    
            with open('orders.txt', 'w') as f:
                json.dump(orders, f)
                
            messagebox.showinfo("Success", "Order declined!")
            self.show_delivery_orders()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decline order: {e}")

    def show_restaurant_list(self):
        self.clear_window()
        
        # Restaurant list frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add sign out and view cart buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(anchor="ne", padx=10, pady=5)
        
        if self.current_user_role == 'Customer':
            ttk.Button(button_frame, text="View Cart", command=self.show_cart).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="My Orders", command=self.show_orders).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sign Out", command=self.sign_out).pack(side=tk.LEFT)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get restaurants from file
        with open('restaurants.txt', 'r') as f:
            restaurants = json.load(f)
        
        for restaurant in restaurants:
            restaurant_frame = ttk.Frame(scrollable_frame)
            restaurant_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(restaurant_frame, text=restaurant['name']).pack(side=tk.LEFT)
            ttk.Label(restaurant_frame, text=restaurant['description']).pack(side=tk.LEFT, padx=10)
            
            # Only show View Menu button for customers
            # Restaurant staff/owners can only view their own restaurant's menu
            if self.current_user_role == 'Customer':
                ttk.Button(restaurant_frame, text="View Menu",
                          command=lambda r_id=restaurant['id']: self.show_menu(r_id)
                          ).pack(side=tk.RIGHT)
            elif self.current_user_role in ['Restaurant Staff', 'Restaurant Owner'] and restaurant['id'] == self.current_user_restaurant_id:
                ttk.Button(restaurant_frame, text="View Menu",
                          command=lambda r_id=restaurant['id']: self.show_menu(r_id)
                          ).pack(side=tk.RIGHT)
                ttk.Button(restaurant_frame, text="Add Food",
                          command=lambda r_id=restaurant['id']: self.show_add_food_page(r_id)
                          ).pack(side=tk.RIGHT, padx=5)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def show_add_food_page(self, restaurant_id):
        add_food_window = tk.Toplevel(self.root)
        add_food_window.title("Add New Food Item")
        add_food_window.geometry("400x300")
        
        add_food_frame = ttk.Frame(add_food_window, padding=20)
        add_food_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(add_food_frame, text="Add New Food Item", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        ttk.Label(add_food_frame, text="Food Name:").pack(pady=5)
        name_entry = ttk.Entry(add_food_frame)
        name_entry.pack(pady=5)
        
        ttk.Label(add_food_frame, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(add_food_frame)
        price_entry.pack(pady=5)
        
        ttk.Label(add_food_frame, text="Description:").pack(pady=5)
        desc_entry = ttk.Entry(add_food_frame)
        desc_entry.pack(pady=5)
        
        def add_food():
            try:
                with open('menu_items.txt', 'r') as f:
                    menu_items = json.load(f)
                
                new_item = {
                    'id': len(menu_items) + 1,
                    'restaurant_id': restaurant_id,
                    'name': name_entry.get(),
                    'price': float(price_entry.get()),
                    'description': desc_entry.get()
                }
                
                menu_items.append(new_item)
                
                with open('menu_items.txt', 'w') as f:
                    json.dump(menu_items, f)
                    
                messagebox.showinfo("Success", "Food item added successfully!")
                add_food_window.destroy()
                self.show_menu(restaurant_id)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add food item: {e}")
        
        ttk.Button(add_food_frame, text="Add Food", command=add_food).pack(pady=20)

    def show_menu(self, restaurant_id):
        self.clear_window()
        
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add buttons
        button_frame = ttk.Frame(menu_frame)
        button_frame.pack(anchor="ne", padx=10, pady=5)
        
        if self.current_user_role == 'Customer':
            ttk.Button(button_frame, text="View Cart", command=self.show_cart).pack(side=tk.LEFT, padx=5)
        elif self.current_user_role in ['Restaurant Staff', 'Restaurant Owner']:
            ttk.Button(button_frame, text="Add Food", 
                      command=lambda: self.show_add_food_page(restaurant_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sign Out", command=self.sign_out).pack(side=tk.LEFT)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(menu_frame)
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get menu items from file
        with open('menu_items.txt', 'r') as f:
            all_menu_items = json.load(f)
            menu_items = [item for item in all_menu_items if item['restaurant_id'] == restaurant_id]
        
        # Add Food button at the top for restaurant staff/owners
        if self.current_user_role in ['Restaurant Staff', 'Restaurant Owner'] and restaurant_id == self.current_user_restaurant_id:
            add_food_frame = ttk.Frame(scrollable_frame)
            add_food_frame.pack(fill=tk.X, padx=10, pady=5)
            ttk.Button(add_food_frame, text="Add New Food Item",
                      command=lambda: self.show_add_food_page(restaurant_id)).pack()
        
        for item in menu_items:
            item_frame = ttk.Frame(scrollable_frame)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(item_frame, text=f"{item['name']} - ${item['price']}").pack(side=tk.LEFT)
            ttk.Label(item_frame, text=item['description']).pack(side=tk.LEFT, padx=10)
            
            # Only show Add to Cart button for customers
            if self.current_user_role == 'Customer':
                ttk.Button(item_frame, text="Add to Cart",
                          command=lambda i=item: self.add_to_cart(i)).pack(side=tk.RIGHT)
            elif self.current_user_role in ['Restaurant Staff', 'Restaurant Owner'] and restaurant_id == self.current_user_restaurant_id:
                ttk.Button(item_frame, text="Edit",
                          command=lambda i=item: self.edit_menu_item(i)).pack(side=tk.RIGHT)
                ttk.Button(item_frame, text="Delete",
                          command=lambda i=item: self.delete_menu_item(i)).pack(side=tk.RIGHT)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Button(self.root, text="Back to Restaurants",
                  command=self.show_restaurant_list).pack(pady=10)

    def edit_menu_item(self, item):
        # Create a new window for editing
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Menu Item")
        edit_window.geometry("400x300")
        
        # Create entry fields
        ttk.Label(edit_window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, item['name'])
        name_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(edit_window)
        price_entry.insert(0, str(item['price']))
        price_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Description:").pack(pady=5)
        desc_entry = ttk.Entry(edit_window)
        desc_entry.insert(0, item['description'])
        desc_entry.pack(pady=5)
        
        def save_changes():
            try:
                # Read current menu items
                with open('menu_items.txt', 'r') as f:
                    menu_items = json.load(f)
                
                # Find and update the item
                for i in range(len(menu_items)):
                    if menu_items[i]['id'] == item['id']:
                        menu_items[i]['name'] = name_entry.get()
                        menu_items[i]['price'] = float(price_entry.get())
                        menu_items[i]['description'] = desc_entry.get()
                        break
                
                # Save updated menu items
                with open('menu_items.txt', 'w') as f:
                    json.dump(menu_items, f)
                
                messagebox.showinfo("Success", "Menu item updated successfully!")
                edit_window.destroy()
                self.show_menu(self.current_user_restaurant_id)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update menu item: {e}")
        
        ttk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)

    def delete_menu_item(self, item):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this menu item?"):
            try:
                # Read current menu items
                with open('menu_items.txt', 'r') as f:
                    menu_items = json.load(f)
                
                # Remove the item
                menu_items = [i for i in menu_items if i['id'] != item['id']]
                
                # Save updated menu items
                with open('menu_items.txt', 'w') as f:
                    json.dump(menu_items, f)
                
                messagebox.showinfo("Success", "Menu item deleted successfully!")
                self.show_menu(self.current_user_restaurant_id)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete menu item: {e}")

    def add_to_cart(self, item):
        if self.current_user_role == 'Customer':
            self.cart.append(item)
            messagebox.showinfo("Success", f"{item['name']} added to cart!")
        else:
            messagebox.showerror("Error", "Only customers can add items to cart")

    def show_cart(self):
        self.clear_window()
        
        cart_frame = ttk.Frame(self.root)
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(cart_frame, text="Shopping Cart", font=('Helvetica', 16, 'bold')).pack()
        
        total = 0
        if self.cart:
            for item in self.cart:
                item_frame = ttk.Frame(cart_frame)
                item_frame.pack(fill=tk.X, pady=5)
                
                ttk.Label(item_frame, text=item['name']).pack(side=tk.LEFT)
                ttk.Label(item_frame, text=f"${item['price']}").pack(side=tk.RIGHT)
                total += item['price']
            
            ttk.Label(cart_frame, text=f"Total: ${total:.2f}", font=('Helvetica', 12, 'bold')).pack(pady=10)
            ttk.Button(cart_frame, text="Proceed to Checkout", 
                      command=lambda: self.show_payment_page(total)).pack(pady=5)
        else:
            ttk.Label(cart_frame, text="Your cart is empty").pack(pady=20)
        
        ttk.Button(cart_frame, text="Back to Restaurants",
                  command=self.show_restaurant_list).pack(pady=5)

    def show_payment_page(self, total):
                with open('menu_items.txt', 'r') as f:
                    menu_items = json.load(f)
                
                # Remove the item
                menu_items = [i for i in menu_items if i['id'] != item['id']]
                
                # Save updated menu items
                with open('menu_items.txt', 'w') as f:
                    json.dump(menu_items, f)
                
                messagebox.showinfo("Success", "Menu item deleted successfully!")
                self.show_menu(self.current_user_restaurant_id);
                
            #except Exception as e:
                #messagebox.showerror("Error", f"Failed to delete menu item: {e}")

    def add_to_cart(self, item):
        if self.current_user_role == 'Customer':
            self.cart.append(item)
            messagebox.showinfo("Success", f"{item['name']} added to cart!")
        else:
            messagebox.showerror("Error", "Only customers can add items to cart")

    def show_cart(self):
        self.clear_window()
        
        cart_frame = ttk.Frame(self.root)
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(cart_frame, text="Shopping Cart", font=('Helvetica', 16, 'bold')).pack()
        
        total = 0
        if self.cart:
            for item in self.cart:
                item_frame = ttk.Frame(cart_frame)
                item_frame.pack(fill=tk.X, pady=5)
                
                ttk.Label(item_frame, text=item['name']).pack(side=tk.LEFT)
                ttk.Label(item_frame, text=f"${item['price']}").pack(side=tk.RIGHT)
                total += item['price']
            
            ttk.Label(cart_frame, text=f"Total: ${total:.2f}", font=('Helvetica', 12, 'bold')).pack(pady=10)
            ttk.Button(cart_frame, text="Proceed to Checkout", 
                      command=lambda: self.show_payment_page(total)).pack(pady=5)
        else:
            ttk.Label(cart_frame, text="Your cart is empty").pack(pady=20)
        
        ttk.Button(cart_frame, text="Back to Restaurants",
                  command=self.show_restaurant_list).pack(pady=5)

    def show_payment_page(self, total):
        self.clear_window()
        
        payment_frame = ttk.Frame(self.root)
        payment_frame.pack(pady=50)
        
        ttk.Label(payment_frame, text="Select Payment Method", 
                 font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        ttk.Label(payment_frame, text=f"Total Amount: ${total:.2f}",
                 font=('Helvetica', 12)).pack(pady=10)
        
        # Add delivery address field
        ttk.Label(payment_frame, text="Delivery Address:").pack(pady=5)
        delivery_address_entry = ttk.Entry(payment_frame)
        delivery_address_entry.pack(pady=5)

        payment_var = tk.StringVar()
        payment_methods = ['Credit Card', 'PayPal', 'Apple Pay', 'Google Pay']
        
        for method in payment_methods:
            ttk.Radiobutton(payment_frame, text=method, 
                          variable=payment_var, value=method).pack(pady=5)
        
        def process_payment():
            if not payment_var.get():
                messagebox.showerror("Error", "Please select a payment method")
                return
            
            # Create new order
            try:
                with open('orders.txt', 'r') as f:
                    orders = json.load(f)
            except:
                orders = []
                
            new_order = {
                'id': len(orders) + 1,
                'user_id': self.current_user_id,
                'items': self.cart,
                'total': total,
                'payment_method': payment_var.get(),
                'status': 'delivering',
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'delivery_address': delivery_address_entry.get()  # Attach delivery address
            }
            
            orders.append(new_order)
            
            with open('orders.txt', 'w') as f:
                json.dump(orders, f)
                
            messagebox.showinfo("Success", 
                              f"Payment processed successfully using {payment_var.get()}")
            self.cart = []  # Clear cart after successful payment
            self.show_restaurant_list()
        
        ttk.Button(payment_frame, text="Pay Now",
                  command=process_payment).pack(pady=20)
        
        ttk.Button(payment_frame, text="Back to Cart",
                  command=self.show_cart).pack()

    def show_orders(self):
        self.clear_window()
        
        orders_frame = ttk.Frame(self.root)
        orders_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        


        button_frame = ttk.Frame(orders_frame)
        button_frame.pack(anchor="ne", padx=10, pady=5)

        ttk.Button(button_frame, text="Back to Restaurants",
                  command=self.show_restaurant_list).pack(side=tk.LEFT,padx=5)
        ttk.Button(button_frame, text="Clear Finished Orders",
                  command=self.clear_finished_orders).pack(side=tk.LEFT,padx=5) 
        ttk.Button(button_frame, text="Sign Out",
                  command=self.sign_out).pack(side=tk.LEFT)


        ttk.Label(orders_frame, text="My Orders", font=('Helvetica', 16, 'bold')).pack()
        
        try:
            with open('orders.txt', 'r') as f:
                all_orders = json.load(f)
                user_orders = [order for order in all_orders if order['user_id'] == self.current_user_id]
        except:
            user_orders = []
            
        if user_orders:
            for order in user_orders:
                order_frame = ttk.Frame(orders_frame)
                order_frame.pack(fill=tk.X, pady=10)
                
                order_info = f"Order #{order['id']} - {order['date']}\n"
                order_info += f"Status: {order['status']}\n"
                order_info += f"Total: ${order['total']:.2f}"
                
                ttk.Label(order_frame, text=order_info).pack(side=tk.LEFT)
                
                if order['status'] == 'delivering':
                    ttk.Button(order_frame, text="Mark as Finished",
                             command=lambda o=order: self.update_order_status(o['id'])).pack(side=tk.RIGHT)
        else:
            ttk.Label(orders_frame, text="No orders found").pack(pady=20)
            
        ttk.Button(orders_frame, text="Back to Restaurants",
                  command=self.show_restaurant_list).pack(pady=10)

    def clear_finished_orders(self):
        try:
            with open('orders.txt', 'r') as f:
                orders = json.load(f)

            updated_orders = [
                order for order in orders
                if order['user_id'] != self.current_user_id or 
                order['status'] != 'Finished'
            ]

            with open('orders.txt', 'w') as f:
                json.dump(updated_orders, f)

            messagebox.showinfo("Success", "Finished orders cleared successfully!")
            self.show_orders()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear finished orders: {e}")
            self.show_orders()
    def update_order_status(self, order_id):
        try:
            with open('orders.txt', 'r') as f:
                orders = json.load(f)
                
            for order in orders:
                if order['id'] == order_id:
                    order['status'] = 'Finished'
                    break
                    
            with open('orders.txt', 'w') as f:
                json.dump(orders, f)
                
            messagebox.showinfo("Success", "Order marked as finished!")
            self.show_orders()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update order status: {e}")

    def show_edit_menu_page(self):
        self.clear_window()
        
        edit_menu_frame = ttk.Frame(self.root)
        edit_menu_frame.pack(pady=50)
        
        # Add sign out button
        ttk.Button(edit_menu_frame, text="Sign Out", command=self.sign_out).grid(row=0, column=2, padx=10, pady=5)
        
        ttk.Label(edit_menu_frame, text="Menu Item Name:").grid(row=0, column=0, pady=5)
        menu_item_name_entry = ttk.Entry(edit_menu_frame)
        menu_item_name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(edit_menu_frame, text="Price:").grid(row=1, column=0, pady=5)
        price_entry = ttk.Entry(edit_menu_frame)
        price_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(edit_menu_frame, text="Description:").grid(row=2, column=0, pady=5)
        description_entry = ttk.Entry(edit_menu_frame)
        description_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(edit_menu_frame, text="Add Menu Item",
                  command=lambda: self.add_menu_item(menu_item_name_entry.get(), 
                                                    price_entry.get(),
                                                    description_entry.get())
                  ).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(edit_menu_frame, text="View Menu",
                  command=lambda: self.show_menu(self.current_user_restaurant_id)).grid(row=4, column=0, columnspan=2)

    def add_menu_item(self, name, price, description):
        try:
            with open('menu_items.txt', 'r') as f:
                menu_items = json.load(f)
            
            new_item = {
                'id': len(menu_items) + 1,
                'restaurant_id': self.current_user_restaurant_id,
                'name': name,
                'price': float(price),
                'description': description
            }
            
            menu_items.append(new_item)
            
            with open('menu_items.txt', 'w') as f:
                json.dump(menu_items, f)
                
            messagebox.showinfo("Success", "Menu item added successfully!")
            self.show_menu(self.current_user_restaurant_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add menu item: {e}")

    def login(self, username, password):
        with open('users.txt', 'r') as f:
            users = json.load(f)
            
        user = next((u for u in users if u['username'] == username), None)
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            self.current_user_id = user['id']
            self.current_user_role = user['role']
            self.current_user_restaurant_id = user.get('restaurant_id')
            
            if self.current_user_role == 'Customer':
                self.show_restaurant_list()
            elif self.current_user_role in ['Restaurant Staff', 'Restaurant Owner']:
                self.show_edit_menu_page()
            elif self.current_user_role == 'Delivery Staff':
                self.show_delivery_orders()
            elif self.current_user_role == 'Customer Service':
                self.show_customer_service_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup(self, username, password, email, role, restaurant_name=None, restaurant_description=None):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        with open('users.txt', 'r') as f:
            users = json.load(f)
            
        if any(u['username'] == username for u in users):
            messagebox.showerror("Error", "Username already exists")
            return

        # Create new restaurant if role is restaurant staff or owner
        restaurant_id = None
        if role in ['Restaurant Staff', 'Restaurant Owner']:
            if not restaurant_name or not restaurant_description:
                messagebox.showerror("Error", "Restaurant details are required")
                return

            with open('restaurants.txt', 'r') as f:
                restaurants = json.load(f)

            new_restaurant = {
                'id': len(restaurants) + 1,
                'name': restaurant_name,
                'description': restaurant_description,
                'address': 'Test Restaurant address'  # Default address
            }
            restaurants.append(new_restaurant)
            restaurant_id = new_restaurant['id']

            with open('restaurants.txt', 'w') as f:
                json.dump(restaurants, f)
            
        new_user = {
            'id': len(users) + 1,
            'username': username,
            'password': hashed_password,
            'email': email,
            'role': role,
            'restaurant_id': restaurant_id,
            'address': 'Test Restaurant address'
        }
        
        
        users.append(new_user)
        
        with open('users.txt', 'w') as f:
            json.dump(users, f)
            
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_page()

    def sign_out(self):
        self.current_user_id = None
        self.current_user_role = None
        self.current_user_restaurant_id = None
        self.cart = []  # Clear cart on sign out
        messagebox.showinfo("Success", "Signed out successfully!")
        self.show_login_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_customer_service_page(self):
        self.clear_window()
        
        service_frame = ttk.Frame(self.root)
        service_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(service_frame, text="Customer Service", font=('Helvetica', 16, 'bold')).pack()
        
        # Add sign out button
        ttk.Button(service_frame, text="Sign Out", command=self.sign_out).pack(anchor="ne")
        
        # Add tabs for orders, accounts, and chat
        tab_control = ttk.Notebook(service_frame)
        orders_tab = ttk.Frame(tab_control)
        accounts_tab = ttk.Frame(tab_control)
        chat_tab = ttk.Frame(tab_control)
        tab_control.add(orders_tab, text="Orders")
        tab_control.add(accounts_tab, text="Accounts")
        tab_control.add(chat_tab, text="Chat")
        tab_control.pack(expand=1, fill="both")
        
        # Orders tab
        ttk.Label(orders_tab, text="All Orders", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        try:
            with open('orders.txt', 'r') as f:
                all_orders = json.load(f)
        except:
            all_orders = []
        
        for order in all_orders:
            order_frame = ttk.Frame(orders_tab, relief="solid", borderwidth=1)
            order_frame.pack(fill=tk.X, pady=5, padx=5)
            
            order_info = f"Order #{order['id']} - {order['date']}\n"
            order_info += f"Status: {order['status']}\n"
            order_info += f"Total: ${order['total']:.2f}"
            
            ttk.Label(order_frame, text=order_info).pack(side=tk.LEFT, padx=5)
            ttk.Button(order_frame, text="View Details",
                      command=lambda o=order: self.show_order_details(o)).pack(side=tk.RIGHT, padx=5)
        
        # Accounts tab
        ttk.Label(accounts_tab, text="All Accounts", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(accounts_tab)
        scrollbar = ttk.Scrollbar(accounts_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        try:
            with open('users.txt', 'r') as f:
                all_users = json.load(f)
        except:
            all_users = []
        
        for user in all_users:
            if user['role'] == 'Customer Service':
                continue  # Skip customer service accounts
            
            user_frame = ttk.Frame(scrollable_frame, relief="solid", borderwidth=1)
            user_frame.pack(fill=tk.X, pady=5, padx=5)
            
            user_info = f"Username: {user['username']}\n"
            user_info += f"Email: {user['email']}\n"
            user_info += f"Role: {user['role']}"
            
            ttk.Label(user_frame, text=user_info).pack(side=tk.LEFT, padx=5)
            
            button_frame = ttk.Frame(user_frame)
            button_frame.pack(side=tk.RIGHT, padx=5)
            
            ttk.Button(button_frame, text="Edit",
                      command=lambda u=user: self.edit_user_account(u)).pack(side=tk.LEFT, padx=2)
            ttk.Button(button_frame, text="Delete",
                      command=lambda u=user: self.delete_user_account(u)).pack(side=tk.LEFT, padx=2)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Chat tab
        ttk.Label(chat_tab, text="Chat with Users", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        chat_frame = ttk.Frame(chat_tab)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(chat_frame, text="Select User:").pack(anchor="w")
        user_var = tk.StringVar()
        user_dropdown = ttk.Combobox(chat_frame, textvariable=user_var)
        user_dropdown.pack(fill=tk.X, pady=5)
        
        try:
            with open('users.txt', 'r') as f:
                all_users = json.load(f)
            user_dropdown['values'] = [user['username'] for user in all_users if user['role'] != 'Customer Service']
        except:
            user_dropdown['values'] = []
        
        chat_text = tk.Text(chat_frame, state='disabled', wrap='word')
        chat_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        message_entry = ttk.Entry(chat_frame)
        message_entry.pack(fill=tk.X, pady=5)
        
        def send_message():
            user = user_var.get()
            message = message_entry.get()
            if user and message:
                chat_text.config(state='normal')
                chat_text.insert(tk.END, f"To {user}: {message}\n")
                chat_text.config(state='disabled')
                message_entry.delete(0, tk.END)
        
        ttk.Button(chat_frame, text="Send", command=send_message).pack(pady=5)
    
    def edit_user_account(self, user):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit User Account")
        edit_window.geometry("400x300")
        
        ttk.Label(edit_window, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(edit_window)
        username_entry.insert(0, user['username'])
        username_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(edit_window)
        email_entry.insert(0, user['email'])
        email_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Role:").pack(pady=5)
        role_var = tk.StringVar()
        roles = ['Customer', 'Restaurant Staff', 'Restaurant Owner', 'Delivery Staff']
        role_dropdown = ttk.Combobox(edit_window, textvariable=role_var, values=roles)
        role_dropdown.set(user['role'])
        role_dropdown.pack(pady=5)
        
        def save_changes():
            try:
                with open('users.txt', 'r') as f:
                    users = json.load(f)
                
                for u in users:
                    if u['id'] == user['id']:
                        u['username'] = username_entry.get()
                        u['email'] = email_entry.get()
                        u['role'] = role_var.get()
                        break
                
                with open('users.txt', 'w') as f:
                    json.dump(users, f)
                
                messagebox.showinfo("Success", "User account updated successfully!")
                edit_window.destroy()
                self.show_customer_service_page()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update user account: {e}")
        
        ttk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)
    
    def delete_user_account(self, user):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user account?"):
            try:
                with open('users.txt', 'r') as f:
                    users = json.load(f)
                
                users = [u for u in users if u['id'] != user['id']]
                
                with open('users.txt', 'w') as f:
                    json.dump(users, f)
                
                messagebox.showinfo("Success", "User account deleted successfully!")
                self.show_customer_service_page()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user account: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FoodOrderingSystem()
    app.run()
