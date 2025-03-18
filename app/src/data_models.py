class Product:
    def __init__(self, name, lead_time, initial_stock):
        self.name = name
        self.lead_time = lead_time  # Czas realizacji
        self.stock = initial_stock  # Początkowy stan magazynowy
        self.demand = []  # Lista zapotrzebowania
        self.production_plan = []  # Planowana produkcja
        self.forecast = []  # Przewidywane zapotrzebowanie

    def add_demand(self, demand):
        self.demand.append(demand)

    def update_stock(self):
        # Oblicz stan magazynowy na podstawie planowanej produkcji
        for i in range(len(self.forecast)):
            planned_production = self.production_plan[i] if i < len(self.production_plan) else 0
            self.stock += planned_production - self.demand[i]
            self.forecast.append(self.stock)