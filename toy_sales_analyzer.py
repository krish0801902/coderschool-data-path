import csv
import matplotlib.pyplot as plt

def extract(file_name):
    sales=[]
    try:
        with open(file_name, 'r') as f:
            for row in csv.DictReader(f):
                try:
                    sales.append({'toy': row['toy'].strip(), 
                                  'category': row['category'].strip().lower(), 
                                  'price': float(row ['price']),
                                  'unit_sold': int(row['unit_sold'])
                                  })
                except (ValueError, KeyError):  
                    pass
        return sales

    except FileNotFoundError:
        return []
def transform(sales):
    cat_data = {}
    for item in sales:
        c = item['category']
        if c not in cat_data:
            cat_data[c] = {'units': 0, 'revenue': 0.0}
        cat_data [c]['units']+=item['units_sold']
        cat_data [c]['revenue']+=item['price'] * item['units_sold']
    category = list(cat_data.items())
    

