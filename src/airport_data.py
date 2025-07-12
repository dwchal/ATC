from airport import Airport

def create_airports():
    airports = {}

    # Rochester International Airport (KRST)
    rst = Airport("Rochester International", "KRST", 43.9083, -92.5000)
    # Runway 13/31
    rst.add_runway("13/31", [-1.2, 0.5], [1.2, -0.5], 150)
    # Runway 3/21
    rst.add_runway("3/21", [-0.8, -1.0], [0.8, 1.0], 150)
    # Taxiways (simplified)
    rst.add_taxiway([[-1.2, 0.5], [-0.5, 0.0], [0.8, 1.0]])
    rst.add_taxiway([[1.2, -0.5], [0.5, 0.0], [-0.8, -1.0]])
    airports['KRST'] = rst

    # Minneapolis-St. Paul International Airport (KMSP)
    msp = Airport("Minneapolis-St. Paul International", "KMSP", 44.8820, -93.2218)
    # Runway 12R/30L
    msp.add_runway("12R/30L", [-1.5, 0.7], [1.5, -0.7], 200)
    # Runway 12L/30R
    msp.add_runway("12L/30R", [-1.2, 1.2], [1.2, -1.2], 150)
    # Runway 4/22
    msp.add_runway("4/22", [-1.0, -1.5], [1.0, 1.5], 150)
    # Runway 17/35
    msp.add_runway("17/35", [0.2, -1.8], [-0.2, 1.8], 150)
    # Taxiways (simplified)
    msp.add_taxiway([[-1.5, 0.7], [0.0, 0.0], [1.0, 1.5]])
    msp.add_taxiway([[1.5, -0.7], [0.0, 0.0], [-1.2, 1.2]])
    msp.add_taxiway([[-1.0, -1.5], [0.0, 0.0], [0.2, -1.8]])
    msp.add_taxiway([[1.2, -1.2], [0.0, 0.0], [-0.2, 1.8]])
    airports['KMSP'] = msp

    # Chicago O'Hare International Airport (KORD)
    ord = Airport("Chicago O'Hare International", "KORD", 41.9776, -87.9047)
    # Runway 10L/28R
    ord.add_runway("10L/28R", [-2.0, 0.3], [2.0, -0.3], 150)
    # Runway 9R/27L
    ord.add_runway("9R/27L", [-1.8, 1.0], [1.8, 0.4], 150)
    # Runway 10C/28C
    ord.add_runway("10C/28C", [-1.7, -0.5], [1.7, -1.1], 200)
    # Runway 9C/27C
    ord.add_runway("9C/27C", [-1.8, 0.8], [1.8, 0.2], 200)
    # Runway 4R/22L
    ord.add_runway("4R/22L", [-0.5, -1.5], [0.5, 1.5], 150)
    # Runway 4L/22R
    ord.add_runway("4L/22R", [-1.2, -0.8], [1.2, 0.8], 150)
    # Runway 9L/27R
    ord.add_runway("9L/27R", [-1.2, 1.5], [1.2, 0.9], 150)
    # Runway 10R/28L
    ord.add_runway("10R/28L", [-1.2, -1.2], [1.2, -1.8], 150)
    # Taxiways (simplified)
    ord.add_taxiway([[-2.0, 0.3], [0.0, 0.0], [1.8, 0.4]])
    ord.add_taxiway([[-1.8, 1.0], [0.0, 0.0], [-1.7, -0.5]])
    ord.add_taxiway([[1.7, -1.1], [0.0, 0.0], [-0.5, -1.5]])
    ord.add_taxiway([[0.5, 1.5], [0.0, 0.0], [-1.2, -0.8]])
    airports['KORD'] = ord

    return airports
