mport csv
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
    n = len(category)
    for i in range (n):
        for j in range(0, n-i-1):
            if category [j][1]['units'] < category [j+1][1]['units']:
                category [j], category [j+1] = category [j+1], category [j]
    return category
                
def show_dashboard(category):
    cats = [c.title() for c, _ in category]
    units = [d['units'] for _, d in category]
    revenue = [d['revenue'] for _, d in category]          
    colors = ['#4ECDC4','#FF6B6B','#FFE66D','#A8E6CF','#FF8894']

    fig, (ax1, ax2) = plt.subplot(1,2,figsize = (14,6))
    ax1.bar(cats,units,color=colors[:len(cats)],edgecolor='white')
    ax1.set_title('units sold by category',fontsize=14, fontweight= 'bold')
    ax2.bar(cats,revenue,color=colors[:len(cats)],edgecolor='white')
    ax2.set_title('revenue by category',fontsize=14, fontweight= 'bold')
    for ax in (ax1,ax2):
        ax.tick_params(axis='x',rotation=30)
    fig.suptitle('toys store sales dashboard',fontsize=18,fontweight='bold')
    plt.tight_layout()
    plt.show()

def save_report(category):
    with open('save_report.csv','w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['rank','category','units','revenue'])
        for i , (c,d) in enumerate (category,1):
            w.writerow([i,c.title(),d['units'],f'${d['revenue']:.2f}'])
    print("report saved to sales_report.csv")



