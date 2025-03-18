import tkinter as tk
from tkinter import messagebox
from app.mrp_algorithm import calculate_mrp
from app.data_models import Product

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MRP & GHP Planner")

        # Zmienna na dane wejściowe
        self.product = None
        self.num_periods = 0
        self.demand_entries = []
        
        self.create_widgets()

    def create_widgets(self):
        # Wprowadzenie liczby jednostek czasu
        self.label_time = tk.Label(self.root, text="Liczba jednostek czasu:")
        self.label_time.grid(row=0, column=0)
        self.entry_time = tk.Entry(self.root)
        self.entry_time.grid(row=0, column=1)
        
        # Wprowadzenie danych zapotrzebowania
        self.label_demand = tk.Label(self.root, text="Wprowadź zapotrzebowanie (oddzielone przecinkami):")
        self.label_demand.grid(row=1, column=0)
        self.entry_demand = tk.Entry(self.root)
        self.entry_demand.grid(row=1, column=1)

        # Wprowadzenie początkowego stanu magazynowego
        self.label_stock = tk.Label(self.root, text="Początkowy stan magazynowy:")
        self.label_stock.grid(row=2, column=0)
        self.entry_stock = tk.Entry(self.root)
        self.entry_stock.grid(row=2, column=1)

        # Wprowadzenie czasu realizacji produkcji
        self.label_lead_time = tk.Label(self.root, text="Czas realizacji produkcji:")
        self.label_lead_time.grid(row=3, column=0)
        self.entry_lead_time = tk.Entry(self.root)
        self.entry_lead_time.grid(row=3, column=1)

        # Przycisk do obliczeń
        self.calculate_button = tk.Button(self.root, text="Oblicz", command=self.calculate)
        self.calculate_button.grid(row=4, columnspan=2)

        # Tabela do wyświetlania wyników
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=5, columnspan=2)

    def calculate(self):
        # Pobieranie danych wejściowych
        try:
            self.num_periods = int(self.entry_time.get())
            demand_str = self.entry_demand.get()
            demand_list = [int(x) for x in demand_str.split(',')]
            stock = int(self.entry_stock.get())
            lead_time = int(self.entry_lead_time.get())

            # Tworzenie produktu
            self.product = Product("Produkt", lead_time, stock)
            for d in demand_list:
                self.product.add_demand(d)

            # Obliczanie MRP
            calculate_mrp(self.product, self.num_periods)

            # Wyświetlanie wyników
            self.display_results()

        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    def display_results(self):
        # Usuwanie poprzednich wyników
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Nagłówki tabeli
        tk.Label(self.table_frame, text="Okres").grid(row=0, column=0)
        tk.Label(self.table_frame, text="Zapotrzebowanie").grid(row=0, column=1)
        tk.Label(self.table_frame, text="Planowana Produkcja").grid(row=0, column=2)
        tk.Label(self.table_frame, text="Stan Magazynowy").grid(row=0, column=3)

        # Wiersze danych
        for i in range(self.num_periods):
            tk.Label(self.table_frame, text=f"Okres {i+1}").grid(row=i+1, column=0)
            tk.Label(self.table_frame, text=self.product.demand[i]).grid(row=i+1, column=1)
            tk.Label(self.table_frame, text=self.product.production_plan[i]).grid(row=i+1, column=2)
            tk.Label(self.table_frame, text=self.product.forecast[i]).grid(row=i+1, column=3)