from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_emission_coal(bi):
    qri = 20.47 
    ar = 25.20  
    avin = 0.80 
    qc = 32.68  
    q4 = 1.5  
    eta_zu = 0.985  
    gvin = 1.5  
    
    k_tv = ((ar * avin * (1 - gvin / 100)) / (100 - q4)) * (qc / qri)
    k_tv = k_tv * (1 - eta_zu)
    emission = k_tv * bi * qri / 1_000_000  
    return round(k_tv * 1000, 2), round(emission, 2)  

def calculate_emission_oil(bi):
    qri = 40.40  
    ar = 0.15  
    avin = 1.00 
    qc = 32.68  
    q4 = 0  
    eta_zu = 0.985  
    gvin = 0  
    
    k_tv = ((ar * avin * (1 - gvin / 100)) / (100 - q4)) * (qc / qri)
    k_tv = k_tv * (1 - eta_zu)
    emission = k_tv * bi * qri / 1_000_000  
    return round(k_tv * 1000, 2), round(emission, 2)  

def calculate_emission_gas(bi):
    qri = 33.08  
    k_tv = 0  
    emission = k_tv * bi * qri / 1_000_000
    return round(k_tv * 1000, 2), round(emission, 2)  

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            bi_coal = float(request.form['bi_coal'])
            bi_oil = float(request.form['bi_oil'])
            bi_gas = float(request.form['bi_gas'])
            
            k_tv_coal, emission_coal = calculate_emission_coal(bi_coal)
            k_tv_oil, emission_oil = calculate_emission_oil(bi_oil)
            k_tv_gas, emission_gas = calculate_emission_gas(bi_gas)
            
            result = f"""
            1. Для заданого енергоблоку і відповідним умовам роботи:
            1.1. Показник емісії твердих частинок при спалюванні вугілля становитиме: {k_tv_coal} г/ГДж;
            1.2. Валовий викид при спалюванні вугілля становитиме: {emission_coal} т.;
            1.3. Показник емісії твердих частинок при спалюванні мазуту становитиме: {k_tv_oil} г/ГДж;
            1.4. Валовий викид при спалюванні мазуту становитиме: {emission_oil} т.;
            1.5. Показник емісії твердих частинок при спалюванні природного газу становитиме: {k_tv_gas} г/ГДж;
            1.6. Валовий викид при спалюванні природного газу становитиме: {emission_gas} т.
            """
        except ValueError:
            result = 'Помилка у введених даних'
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
