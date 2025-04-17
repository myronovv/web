from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    example = None

    if request.method == "POST":
        example = request.form.get("example")

        if example == "7.1":
            P = float(request.form.get("power")) * 1000 
            U = float(request.form.get("voltage")) * 1000 
            cos_phi = float(request.form.get("cos_phi"))
            I = P / (U * cos_phi)
            result = {"info": "Розрахований струм", "I": round(I, 2)}

        elif example == "7.2":
            U = float(request.form.get("voltage")) * 1000
            Z = float(request.form.get("impedance"))
            Ikz = U / (1.73 * Z)
            result = {"info": "Струм КЗ", "Ikz": round(Ikz, 2)}

        elif example == "7.4":
            U = float(request.form.get("voltage")) * 1000
            Z = float(request.form.get("impedance"))
            regime = request.form.get("regime")

            k_regime = {
                "normal": 1.0,
                "minimal": 0.9,
                "emergency": 0.75
            }

            coeff = k_regime.get(regime, 1.0)
            Ikz = coeff * U / (1.73 * Z)
            result = {"info": f"Струм КЗ ({regime})", "Ikz": round(Ikz, 2)}

    return render_template("index.html", result=result, example=example)

if __name__ == "__main__":
    app.run(debug=True)
