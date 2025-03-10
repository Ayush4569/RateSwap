import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_KEY = "3ac2f114561e233fb5aa9373da8981d4"
API_URL = f"https://v6.exchangeratesapi.io/latest?access_key={API_KEY}"

def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        data = response.json()
        if "rates" in data:
            return data["rates"]
        else:
            messagebox.showerror("Error", "Failed to fetch exchange rates.")
            return {}
    except Exception as e:
        messagebox.showerror("Error", f"Network error: {e}")
        return {}

exchange_rates = get_exchange_rates()

def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = combo_from_currency.get()
        to_currency = combo_to_currency.get()
        
        if from_currency == to_currency:
            messagebox.showwarning("Warning", "Source and target currencies cannot be the same.")
            return

        if from_currency in exchange_rates and to_currency in exchange_rates:
            rate = exchange_rates[to_currency] / exchange_rates[from_currency]
            result = amount * rate
            label_result.config(text=f"Converted Amount: {result:.2f} {to_currency}")
        else:
            messagebox.showerror("Error", "Conversion rate not available.")
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

window = tk.Tk()
window.title("Currency Converter")
window.geometry("450x400")
window.configure(bg="#f0f0f0")

title_label = tk.Label(window, text="Currency Converter", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

frame_amount = tk.Frame(window, bg="#f0f0f0")
frame_amount.pack(pady=5)
tk.Label(frame_amount, text="Amount:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
entry_amount = tk.Entry(frame_amount, width=20, font=("Arial", 12))
entry_amount.pack(side="left")

frame_currency = tk.Frame(window, bg="#f0f0f0")
frame_currency.pack(pady=5)

currencies = list(exchange_rates.keys())

tk.Label(frame_currency, text="From:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
combo_from_currency = ttk.Combobox(frame_currency, values=currencies, width=10, font=("Arial", 12))
combo_from_currency.set("USD")
combo_from_currency.pack(side="left", padx=5)

tk.Label(frame_currency, text="To:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
combo_to_currency = ttk.Combobox(frame_currency, values=currencies, width=10, font=("Arial", 12))
combo_to_currency.set("EUR")
combo_to_currency.pack(side="left", padx=5)

# Convert Button
button_convert = tk.Button(window, text="Convert", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=convert_currency)
button_convert.pack(pady=20, ipadx=10, ipady=5)

# Result Label
label_result = tk.Label(window, text="Converted Amount: ", font=("Arial", 12, "bold"), bg="#f0f0f0")
label_result.pack(pady=10)

# Run the Application
window.mainloop()
