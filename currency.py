import tkinter as tk
from tkinter import messagebox

# Exchange rates dictionary (for example purposes)
exchange_rates = {
    'USD': {'EUR': 0.91, 'GBP': 0.75, 'INR': 82.00, 'AUD': 1.5},
    'EUR': {'USD': 1.1, 'GBP': 0.82, 'INR': 90.0, 'AUD': 1.65},
    'GBP': {'USD': 1.33, 'EUR': 1.22, 'INR': 109.0, 'AUD': 1.9},
    'INR': {'USD': 0.012, 'EUR': 0.011, 'GBP': 0.0092, 'AUD': 0.017},
    'AUD': {'USD': 0.67, 'EUR': 0.61, 'GBP': 0.53, 'INR': 58.0}
}

# Function to convert currency
def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = combo_from_currency.get()
        to_currency = combo_to_currency.get()
        
        if from_currency == to_currency:
            messagebox.showinfo("Error", "Source and target currencies cannot be the same.")
            return
        
        rate = exchange_rates[from_currency].get(to_currency)
        
        if rate:
            result = amount * rate
            label_result.config(text=f"Converted Amount: {result:.2f} {to_currency}")
        else:
            messagebox.showinfo("Error", "Conversion rate not available.")
        
    except ValueError:
        messagebox.showinfo("Error", "Please enter a valid number.")

# Setting up the main window
window = tk.Tk()
window.title("Exchangify - Currency Converter")
window.geometry("400x300")

# Label and input field for amount
label_amount = tk.Label(window, text="Enter Amount:")
label_amount.pack(pady=10)

entry_amount = tk.Entry(window, width=20)
entry_amount.pack(pady=5)

# Dropdown for selecting source currency
label_from_currency = tk.Label(window, text="From Currency:")
label_from_currency.pack(pady=5)

combo_from_currency = tk.StringVar()
combo_from_currency.set("USD")  # Default value
dropdown_from_currency = tk.OptionMenu(window, combo_from_currency, "USD", "EUR", "GBP", "INR", "AUD")
dropdown_from_currency.pack(pady=5)

# Dropdown for selecting target currency
label_to_currency = tk.Label(window, text="To Currency:")
label_to_currency.pack(pady=5)

combo_to_currency = tk.StringVar()
combo_to_currency.set("EUR")  # Default value
dropdown_to_currency = tk.OptionMenu(window, combo_to_currency, "USD", "EUR", "GBP", "INR", "AUD")
dropdown_to_currency.pack(pady=5)

# Convert button
button_convert = tk.Button(window, text="Convert", command=convert_currency)
button_convert.pack(pady=20)

# Label for displaying the result
label_result = tk.Label(window, text="Converted Amount: ")
label_result.pack(pady=5)

# Run the application
window.mainloop()
