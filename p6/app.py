from flask import Flask, render_template_string, request

app = Flask(__name__)

# Початкові дані з таблиці 6.6
data = [
    {"name": "Шліфувальний верстат", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 4, "Pn": 20, "Kv": 0.15, "tg_phi": 1.33},
    {"name": "Свердлильний верстат", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 2, "Pn": 14, "Kv": 0.12, "tg_phi": 1.0},
    {"name": "Фугувальний верстат", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 4, "Pn": 42, "Kv": 0.15, "tg_phi": 1.33},
    {"name": "Циркулярна пила", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 1, "Pn": 36, "Kv": 0.3, "tg_phi": 1.52},
    {"name": "Прес", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 1, "Pn": 20, "Kv": 0.5, "tg_phi": 0.75},
    {"name": "Полірувальний верстат", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 1, "Pn": 40, "Kv": 0.2, "tg_phi": 1.0},
    {"name": "Фрезерний верстат", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 2, "Pn": 32, "Kv": 0.2, "tg_phi": 1.0},
    {"name": "Вентилятор", "eta": 0.92, "cos_phi": 0.9, "U": 0.38, "n": 1, "Pn": 20, "Kv": 0.65, "tg_phi": 0.75}
]

html_template = """
<!doctype html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Веб калькулятор електричних навантажень</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
    <h1 class="text-center mb-4">Розрахунок електричних навантажень</h1>
    <form method="post">
        <table class="table table-bordered">
            <thead class="table-dark">
                <tr>
                    <th>Найменування ЕП</th>
                    <th>ηн</th>
                    <th>cos φ</th>
                    <th>Uн (кВ)</th>
                    <th>n</th>
                    <th>Pn (кВт)</th>
                    <th>Kv</th>
                    <th>tg φ</th>
                </tr>
            </thead>
            <tbody>
               {% for ep in data %}
<tr>
    <td><input type="text" name="name{{ loop.index0 }}" class="form-control" value="{{ ep.name }}" required></td>
    <td><input type="number" step="0.01" name="eta{{ loop.index0 }}" class="form-control" value="{{ ep.eta }}" required></td>
    <td><input type="number" step="0.01" name="cos_phi{{ loop.index0 }}" class="form-control" value="{{ ep.cos_phi }}" required></td>
    <td><input type="number" step="0.01" name="U{{ loop.index0 }}" class="form-control" value="{{ ep.U }}" required></td>
    <td><input type="number" name="n{{ loop.index0 }}" class="form-control" value="{{ ep.n }}" required></td>
    <td><input type="number" name="Pn{{ loop.index0 }}" class="form-control" value="{{ ep.Pn }}" required></td>
    <td><input type="number" step="0.01" name="Kv{{ loop.index0 }}" class="form-control" value="{{ ep.Kv }}" required></td>
    <td><input type="number" step="0.01" name="tg_phi{{ loop.index0 }}" class="form-control" value="{{ ep.tg_phi }}" required></td>
</tr>
{% endfor %}

            </tbody>
        </table>
        <div class="text-center">
            <button type="submit" class="btn btn-success">Розрахувати</button>
        </div>
    </form>
    {% if results %}
    <h3 class="mt-5">Результати розрахунку:</h3>
    <table class="table table-striped">
        <thead class="table-secondary">
            <tr>
                <th>ЕП</th><th>Ip (A)</th>
            </tr>
        </thead>
        <tbody>
            {% for item in results %}
            <tr>
                <td>{{ item.name }}</td>
                <td>{{ item.Ip }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <ul class="list-group">
        <li class="list-group-item">Kв = <strong>{{ K_v }}</strong></li>
        <li class="list-group-item">nₑ = <strong>{{ n_e }}</strong></li>
        <li class="list-group-item">Kₚ = <strong>{{ K_p }}</strong></li>
        <li class="list-group-item">Pₚ = <strong>{{ P_p }} кВт</strong></li>
        <li class="list-group-item">Qₚ = <strong>{{ Q_p }} квар</strong></li>
        <li class="list-group-item">Sₚ = <strong>{{ S_p }} кВА</strong></li>
        <li class="list-group-item">Iₚ = <strong>{{ I_p }} А</strong></li>
    </ul>
    {% endif %}
</div>
</body>
</html>
"""

def calculate(data):
    results = []
    sum_Pn = 0
    sum_KvPn = 0
    sum_KvPn_tgphi = 0
    sum_Pn2 = 0

    for ep in data:
        Pn_total = ep['n'] * ep['Pn']
        Ip = round((Pn_total * 1000) / (ep['eta'] * ep['cos_phi'] * (3**0.5) * ep['U']), 1)
        results.append({"name": ep['name'], "Ip": Ip})

        sum_Pn += Pn_total
        sum_KvPn += Pn_total * ep['Kv']
        sum_KvPn_tgphi += Pn_total * ep['Kv'] * ep['tg_phi']
        sum_Pn2 += (Pn_total)**2

    K_v = round(sum_KvPn / sum_Pn, 4)
    n_e = round((sum_Pn ** 2) / sum_Pn2)
    K_p = 1.25
    P_p = round(K_p * sum_KvPn, 2)
    Q_p = round(sum_KvPn_tgphi, 2)
    S_p = round((P_p**2 + Q_p**2)**0.5, 2)
    I_p = round((P_p * 1000) / (0.38 * (3**0.5)), 2)

    return results, K_v, n_e, K_p, P_p, Q_p, S_p, I_p

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_data = []
        for i in range(len(data)):
            new_data.append({
                "name": request.form[f'name{i}'],
                "eta": float(request.form[f'eta{i}']),
                "cos_phi": float(request.form[f'cos_phi{i}']),
                "U": float(request.form[f'U{i}']),
                "n": int(request.form[f'n{i}']),
                "Pn": float(request.form[f'Pn{i}']),
                "Kv": float(request.form[f'Kv{i}']),
                "tg_phi": float(request.form[f'tg_phi{i}'])
            })

        results, K_v, n_e, K_p, P_p, Q_p, S_p, I_p = calculate(new_data)
        return render_template_string(html_template, data=new_data, results=results, K_v=K_v, n_e=n_e, K_p=K_p, P_p=P_p, Q_p=Q_p, S_p=S_p, I_p=I_p)
    return render_template_string(html_template, data=data, results=None)

if __name__ == "__main__":
    app.run(debug=True)
