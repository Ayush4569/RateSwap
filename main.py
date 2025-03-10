import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Replace with your actual API key
API_KEY = "3ac2f114561e233fb5aa9373da8981d4"
API_URL = f"https://api.apilayer.com/exchangerates_data/latest?apikey={API_KEY}"

# Fetch exchange rates
def fetch_exchange_rates():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if response.status_code == 200:
            return data["rates"]
        else:
            messagebox.showerror("Error", f"API Error: {data.get('error', 'Unknown Error')}")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return None

# Convert currency
def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = combo_from_currency.get()
        to_currency = combo_to_currency.get()

        if from_currency == to_currency:
            messagebox.showinfo("Error", "Source and target currencies cannot be the same.")
            return
        
        rates = fetch_exchange_rates()
        if not rates:
            return
        
        from_rate = rates.get(from_currency)
        to_rate = rates.get(to_currency)

        if from_rate and to_rate:
            converted_amount = (amount / from_rate) * to_rate
            label_result.config(text=f"Converted Amount: {converted_amount:.2f} {to_currency}")
        else:
            messagebox.showinfo("Error", "Invalid currency selection.")
    
    except ValueError:
        messagebox.showinfo("Error", "Please enter a valid number.")

# Initialize Tkinter window
window = tk.Tk()
window.title("Exchangify - Currency Converter")
window.geometry("450x350")
window.resizable(False, False)
window.configure(bg="#f0f0f0")

# Fetch supported currencies
exchange_rates = fetch_exchange_rates()
currency_list = sorted(exchange_rates.keys()) if exchange_rates else ["USD", "EUR", "GBP", "INR", "AUD"]

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
style.configure("TCombobox", font=("Arial", 12))

# Title
label_title = ttk.Label(window, text="Currency Converter", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

# Amount Entry
frame_amount = ttk.Frame(window)
frame_amount.pack(pady=10)

ttk.Label(frame_amount, text="Enter Amount: ").pack(side="left", padx=5)
entry_amount = ttk.Entry(frame_amount, font=("Arial", 12), width=15)
entry_amount.pack(side="left")

# Dropdowns for currency selection
frame_currency = ttk.Frame(window)
frame_currency.pack(pady=10)

ttk.Label(frame_currency, text="From: ").pack(side="left", padx=5)
combo_from_currency = ttk.Combobox(frame_currency, values=currency_list, state="readonly", width=10)
combo_from_currency.set("USD")
combo_from_currency.pack(side="left")

ttk.Label(frame_currency, text="To: ").pack(side="left", padx=5)
combo_to_currency = ttk.Combobox(frame_currency, values=currency_list, state="readonly", width=10)
combo_to_currency.set("EUR")
combo_to_currency.pack(side="left")

# Convert Button
button_convert = ttk.Button(window, text="Convert", command=convert_currency)
button_convert.pack(pady=20)

# Result Label
label_result = ttk.Label(window, text="Converted Amount: ", font=("Arial", 14, "bold"))
label_result.pack(pady=10)

# Run Tkinter event loop
window.mainloop()
