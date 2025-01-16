'''( 1 ) Utility App - Vending Machine'''
# Princess Jamila Dinglasan

from tkinter import *

'''( 2 ) Menu Dictionary'''
menu = { # Shows the list of items the user can buy + the price & input code
    "Snacks": {
        "Sandwich": {"Turkey Sandwich": {"price": 5.00, "code": "01"}, "Chicken Sandwich": {"price": 4.50, "code": "02"}},
        "Pastries": {"Croissant": {"price": 2.50, "code": "11"}, "Donut": {"price": 2.00, "code": "12"}},
    },
    "Hot Drinks": {
        "Coffee": {
            "Americano": {"price": 2.50, "code": "21"},
            "Cappuccino": {"price": 3.00, "code": "22"},
            "Latte": {"price": 3.20, "code": "23"}
        },
        "Tea": {"Green Tea": {"price": 2.00, "code": "31"},
                "Chamomile Tea": {"price": 2.20, "code": "32"}},
    },
    "Cold Drinks": {
        "Frappe": {
            "Caramel Frappe": {"price": 3.00, "code": "41"}, 
            "Mocha Frappe": {"price": 3.00, "code": "42"},
            "Cookie Frappe": {"price": 3.00, "code": "43"}
        },
        "Juice": {"Apple Juice": {"price": 1.00, "code": "51"}, 
                  "Orange Juice": {"price": 1.50, "code": "52"}
        },
    },
}

'''( 3 ) Initialize User Data'''
cash = [0]  # Using list to make it mutable
shopping_cart = []  # Items in current order
purchase_history = []  # Track what people bought

'''( 4 ) Helper Functions'''
def clear_frame(frame): # To change display
    for widget in frame.winfo_children():
        widget.destroy()

def update_wallet(amount): # Amount of "money" user has
    current = float(money_display.get().replace('$', '') or '0')
    new_amount = current * 10 + amount
    if new_amount <= 1000:
        cash[0] = new_amount
        money_display.set(f"${new_amount:.2f}")
        oops_message.set("") # When input is wrong or unacceptable
    else:
        oops_message.set("Amount cannot exceed $1000.00")

def confirm_amount():
    if cash[0] == 0:
        oops_message.set("Please enter an amount")
    elif cash[0] > 1000:
        oops_message.set("Amount cannot exceed $1000.00")
    else:
        show_full_menu()
        create_numpad()  # Show numpad after money is entered

def empty_wallet():
    cash[0] = 0
    money_display.set("$0.00")
    oops_message.set("")  # Clear error message when resetting

def process_order():
    total = sum(price for _, price in shopping_cart)
    if cash[0] >= total:
        cash[0] -= total
        purchase_history.extend(shopping_cart)
        show_dispensing()
        shopping_cart.clear()
    else:
        oops_message.set("Not enough money :')")

def process_code_input(code):
    cart_total = sum(price for _, price in shopping_cart)
    
    for category in menu:
        for subcategory in menu[category]:
            for item, details in menu[category][subcategory].items():
                if details["code"] == code: # Check if adding this item would exceed available balance
                    if cart_total + details["price"] <= cash[0]:
                        add_to_cart(item, details["price"])
                        update_cart_display()
                        return True
                    else:
                        oops_message.set(f"Not enough balance! Need ${(cart_total + details['price'] - cash[0]):.2f} more")
                        return False
    oops_message.set(f"Invalid code: {code}")
    return False

'''( 5 ) GUI Display'''

def update_cart_display():
    if hasattr(update_cart_display, 'cart_frame'):
        update_cart_display.cart_frame.destroy()

    cart_frame = Frame(right_frame, bg="#dbb293")
    cart_frame.pack(fill=X, pady=10, padx=10)
    update_cart_display.cart_frame = cart_frame
    
    Label(
        cart_frame,
        text="Current Order:",
        font=("consolas", 12, "bold"),
        bg="#dbb293",
        fg="#4a2410",
    ).pack(pady=(5,0))
    
    total = 0
    for item, price in shopping_cart:
        item_frame = Frame(cart_frame, bg="#dbb293")
        item_frame.pack(fill=X)
        
        Label(
            item_frame,
            text=f"• {item}",
            font=("consolas", 10),
            bg="#dbb293",
            fg="#4a2410",
        ).pack(side=LEFT)
        
        Label(
            item_frame,
            text=f"${price:.2f}",
            font=("consolas", 10),
            bg="#dbb293",
            fg="#4a2410",
        ).pack(side=RIGHT)
        
        total += price
    
    if shopping_cart:
        Label(
            cart_frame,
            text=f"Total: ${total:.2f}",
            font=("consolas", 12, "bold"),
            bg="#dbb293",
            fg="#4a2410",
        ).pack(pady=5)

'''( 6 & 7 ) Creating The Numpad 1 & 2'''

def create_numpad():
    clear_frame(right_frame)
    
    # Balance display
    balance_frame = Frame(right_frame, bg="#dbb293")
    balance_frame.pack(fill=X, pady=5, padx=10)
    
    Label(
        balance_frame,
        text="Current Balance:",
        font=("consolas", 12, "bold"),
        bg="#dbb293",
        fg="#4a2410",
    ).pack(side=LEFT, pady=5)
    
    Label(
        balance_frame,
        textvariable=money_display,
        font=("consolas", 12, "bold"),
        bg="#dbb293",
        fg="#4a2410",
    ).pack(side=RIGHT, pady=5)
    
    code_var = StringVar()
    code_var.set("")
    
    display_frame = Frame(right_frame, bg="#dbb293")
    display_frame.pack(fill=X, pady=5, padx=10)
    
    Label(
        display_frame,
        text="Enter Item Code:",
        font=("consolas", 14, "bold"),
        bg="#dbb293",
        fg="#4a2410",
    ).pack(pady=5)
    
    code_display = Entry(
        display_frame,
        textvariable=code_var,
        font=("consolas", 20),
        justify="center",
        width=8
    )

    code_display.pack(pady=5)
    numpad_frame = Frame(right_frame, bg="#dbb293")
    numpad_frame.pack(pady=10, padx=10)
    
    buttons = [
        '7', '8', '9',
        '4', '5', '6',
        '1', '2', '3',
        'C', '0', 'E'
    ]
    
    row = 0
    col = 0

    def button_click(value):
        current = code_var.get()
        if value == 'C':  # Clear
            code_var.set("")
            oops_message.set("")  # Clear error message
        elif value == 'E':  # Enter
            if len(current) == 2:
                process_code_input(current)
                code_var.set("")  # Clear after processing
            else:
                oops_message.set("Please enter a 2-digit code!")
        elif len(current) < 2:  # Only allow 2 digits (maximum code)
            code_var.set(current + value)
    
    for button in buttons:
        btn_color = "#4CAF50" if button in ['E'] else "#b3704f" if button in ['C'] else "#85493a"
        btn = Button(
            numpad_frame,
            text=button,
            font=("consolas", 16, "bold"),
            width=5,
            height=2,
            bg=btn_color,
            fg="white",
            activebackground="#6b3b2e",
            activeforeground="white",
            command=lambda b=button: button_click(b)
        )
        btn.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 2:
            col = 0
            row += 1
    
    # Add finish shopping button
    finish_frame = Frame(right_frame, bg="#dbb293")
    finish_frame.pack(fill=X, pady=10, padx=10)
    
    Button(
        finish_frame,
        text="Finish & Get Change",
        font=("consolas", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        command=show_dispensing,
    ).pack(fill=X, pady=5)
    
    # Add initial empty order display
    update_cart_display()

def show_full_menu():
    clear_frame(left_frame)
    
    # Title
    title_frame = Frame(left_frame, bg="#dbb293")
    title_frame.pack(fill=X, pady=(10, 20))
    
    Label(
        title_frame,
        text="Princess' Cafe",
        font=("fixedsys", 30, "bold"),
        bg="#dbb293",
        fg="#85493a",
    ).pack()
    
    Label(
        title_frame,
        text="━━━━ Menu ━━━━",
        font=("fixedsys", 20),
        bg="#dbb293",
        fg="#85493a",
    ).pack()

    # Create scrollable menu
    menu_frame = Frame(left_frame, bg="#dbb293")
    menu_frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(menu_frame, bg="#dbb293", highlightthickness=0)
    scrollbar = Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#dbb293")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Display menu items
    for category in menu:
        # Category header
        category_frame = Frame(scrollable_frame, bg="#b3704f", relief=RAISED, borderwidth=2)
        category_frame.pack(fill=X, padx=5, pady=(15, 5))
        
        Label(
            category_frame,
            text=category,
            font=("fixedsys", 18, "bold"),
            bg="#b3704f",
            fg="white",
            pady=5,
        ).pack()

        for subcategory, items in menu[category].items():
            # Subcategory header
            subcategory_frame = Frame(scrollable_frame, bg="#dbb293")
            subcategory_frame.pack(fill=X, pady=(10, 5))
            
            Label(
                subcategory_frame,
                text=f"• {subcategory} •",
                font=("consolas", 14, "bold"),
                bg="#dbb293",
                fg="#4a2410",
            ).pack()

            # Items with prices
            items_frame = Frame(scrollable_frame, bg="#dbb293")
            items_frame.pack(fill=X, padx=20, pady=5)
            
            for item, details in items.items():
                create_menu_item_frame(items_frame, item, details)

    # Pack scrollbar and canvas
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

def create_menu_item_frame(parent, item, details):
    frame = Frame(parent, bg="#e8c2a5", relief=RAISED, borderwidth=1)
    frame.pack(fill=X, padx=10, pady=2)
    
    code_label = Label(
        frame,
        text=f"[{details['code']}]",
        font=("consolas", 12, "bold"),
        bg="#e8c2a5",
        fg="#4a2410",
        anchor="w",
    )
    code_label.pack(side=LEFT, padx=5)
    
    Label(
        frame,
        text=item,
        font=("consolas", 12),
        bg="#e8c2a5",
        fg="#4a2410",
        anchor="w",
    ).pack(side=LEFT, padx=5)
    
    Label(
        frame,
        text=f"${details['price']:.2f}",
        font=("consolas", 12, "bold"),
        bg="#e8c2a5",
        fg="#85493a",
        anchor="e",
    ).pack(side=RIGHT, padx=10)

def show_dispensing():
    if not shopping_cart:
        oops_message.set("Please select items first!")
        return
        
    clear_frame(left_frame)
    clear_frame(right_frame)
    
    '''( 8 ) "Cash" Calculation System'''
    total_spent = sum(price for _, price in shopping_cart)
    change = cash[0] - total_spent
    
    # Display items being dispensed
    Label(
        left_frame,
        text=" Whirring Noises ",
        font=("fixedsys", 20),
        bg="#dbb293",
        fg="#85493a",
    ).pack(pady=5)
    
    Label(
        left_frame,
        text="Dispensing Items...",
        font=("fixedsys", 24, "bold"),
        bg="#dbb293",
        fg="#85493a",
    ).pack(pady=5)
    
    for item, price in shopping_cart:
        Label(
            left_frame,
            text=f" {item} ",
            font=("consolas", 14),
            bg="#dbb293",
            fg="#4a2410",
        ).pack(pady=2)
    
    Label(
        left_frame,
        text=" Ka-Ching! ",
        font=("fixedsys", 20),
        bg="#dbb293",
        fg="#85493a",
    ).pack(pady=10)
    
    if change > 0:
        Label(
            left_frame,
            text="Dispensing Change:",
            font=("consolas", 16, "bold"),
            bg="#dbb293",
            fg="#4a2410",
        ).pack(pady=5)
        
        # Break down change into bills and coins
        bills = int(change)
        coins = round((change - bills) * 100)
        
        if bills > 0:
            Label(
                left_frame,
                text=f" {bills} {'bill' if bills == 1 else 'bills'} ",
                font=("consolas", 14),
                bg="#dbb293",
                fg="#2e7d32",
            ).pack()
        
        if coins > 0:
            Label(
                left_frame,
                text=f" {coins} {'cent' if coins == 1 else 'cents'} ",
                font=("consolas", 14),
                bg="#dbb293",
                fg="#2e7d32",
            ).pack()
            
        Label(
            left_frame,
            text=f"Total Change: ${change:.2f}",
            font=("consolas", 16, "bold"),
            bg="#dbb293",
            fg="#2e7d32",
        ).pack(pady=10)
    
    '''( 9 ) New Order Loop'''
    Button(
        left_frame,
        text="Start New Order",
        font=("consolas", 14, "bold"),
        bg="#4CAF50",
        fg="white",
        command=lambda: [
            shopping_cart.clear(),  # Clear the current order
            cash.__setitem__(0, 0),  # Reset money
            money_display.set("$0.00"),  # Reset display
            show_full_menu(),  # Show menu first
            show_money_input_panel()  # Then show money input
        ]
    ).pack(pady=20)

def add_to_cart(item, price):
    cart_total = sum(p for _, p in shopping_cart)
    if cart_total + price <= cash[0]:
        shopping_cart.append((item, price))
        update_cart_display()
    else:
        oops_message.set(f"Not enough balance! Need ${(cart_total + price - cash[0]):.2f} more")

def show_money_input_panel():
    clear_frame(right_frame)
    
    Label(
        right_frame,
        text="Enter Money",
        font=("fixedsys", 24, "bold"),
        bg="#e8c2a5",
        fg="#85493a",
    ).pack(pady=20)

    Label(
        right_frame,
        textvariable=money_display,
        font=("fixedsys", 30, "bold"),
        bg="#e8c2a5",
        fg="#2e7d32",
    ).pack(pady=10)

    keypad = Frame(right_frame, bg="#e8c2a5")
    keypad.pack(pady=20)

    for i in range(1, 10):
        Button(
            keypad,
            text=str(i),
            font=("consolas", 20, "bold"),
            bg="#b3704f",
            fg="#ffffff",
            activebackground="#91451f",
            activeforeground="#ffffff",
            width=4,
            command=lambda n=i: update_wallet(n),
        ).grid(row=(i-1)//3, column=(i-1)%3, pady=5, padx=5)

    Button(
        keypad,
        text="0",
        font=("consolas", 20, "bold"),
        bg="#b3704f",
        fg="#ffffff",
        activebackground="#91451f",
        activeforeground="#ffffff",
        width=4,
        command=lambda: update_wallet(0),
    ).grid(row=3, column=1, pady=5, padx=5)

    # Control buttons frame
    control_frame = Frame(right_frame, bg="#e8c2a5")
    control_frame.pack(pady=20)

    Button(
        control_frame,
        text="Confirm",
        font=("consolas", 16),
        bg="#4CAF50",
        fg="#ffffff",
        activebackground="#388E3C",
        activeforeground="#ffffff",
        width=10,
        command=confirm_amount,
    ).pack(side=LEFT, padx=5)

    Button(
        control_frame,
        text="Reset",
        font=("consolas", 16),
        bg="#f44336",
        fg="#ffffff",
        activebackground="#d32f2f",
        activeforeground="#ffffff",
        width=10,
        command=empty_wallet,
    ).pack(side=LEFT, padx=5)

    Label(
        right_frame,
        textvariable=oops_message,
        font=("consolas", 14),
        bg="#e8c2a5",
        fg="red",
    ).pack(pady=10)

'''( 10 ) Full GUI Window Setup'''
app = Tk()
app.title("Utility App - Princess Jamila Dinglasan (CC Yr 1)")
app.geometry("1000x750")
app.config(background="#dbb293")

left_frame = Frame(app, bg="#dbb293", width=600)
left_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)
left_frame.pack_propagate(False)

right_frame = Frame(app, bg="#e8c2a5", width=400)
right_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)
right_frame.pack_propagate(False)

money_display = StringVar()
money_display.set("$0.00")
oops_message = StringVar()

show_full_menu()
show_money_input_panel()

# Loop to keep window open
app.mainloop()