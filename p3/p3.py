from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_profit(Pc, sigma1, sigma2, price):
    if sigma2 >= sigma1:
        return None, "Покращене σ повинно бути менше за початкове."
    
    delta_m1 = 0.2  # 20% до покращення
    delta_m2 = 0.68 # 68% після покращення

    W1 = Pc * 24 * delta_m1
    P1 = W1 * price * 1000
    W2 = Pc * 24 * (1 - delta_m1)
    S1 = W2 * price * 1000
    profit1 = P1 - S1

    W3 = Pc * 24 * delta_m2
    P2 = W3 * price * 1000
    W4 = Pc * 24 * (1 - delta_m2)
    S2 = W4 * price * 1000
    profit2 = P2 - S2

    return {
        "W1": W1, "P1": P1, "W2": W2, "S1": S1, "profit1": profit1,
        "W3": W3, "P2": P2, "W4": W4, "S2": S2, "profit2": profit2
    }, None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            Pc = float(request.form['Pc'])
            sigma1 = float(request.form['sigma1'])
            sigma2 = float(request.form['sigma2'])
            price = float(request.form['price'])
            
            result, error = calculate_profit(Pc, sigma1, sigma2, price)
        except ValueError:
            error = 'Помилка у введених даних!'
    
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)