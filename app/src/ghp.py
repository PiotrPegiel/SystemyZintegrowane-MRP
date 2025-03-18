def calculate_ghp(product, num_periods):
    """
    Funkcja oblicza plan produkcji i stan magazynowy na podstawie zapotrzebowania.
    """
    for i in range(num_periods):
        if i >= product.lead_time:
            # Jeżeli minął czas realizacji, rozpocznij produkcję
            planned_production = max(0, product.demand[i] - product.stock)
            product.production_plan.append(planned_production)
        else:
            # W okresach przed czasem realizacji nie możemy produkować
            product.production_plan.append(0)

    # Obliczanie stanu magazynowego na podstawie planowanej produkcji
    product.update_stock()