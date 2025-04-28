from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        omega_list = list(map(float, request.form.getlist("omega")))
        tvi_list = list(map(float, request.form.getlist("tvi")))

        Z_av = float(request.form["Z_av"])
        Z_pl = float(request.form["Z_pl"])

        omega_oc = sum(omega_list)
        t_v_oc = sum(omega_list[i] * tvi_list[i] for i in range(len(omega_list))) / omega_oc

        k_a_oc = (omega_oc * t_v_oc) / 8760
        k_n_oc = (1.2 * 1.43) / 8760 

        omega_dc = omega_oc * (3.6e-4 + 58.9e-4)
        omega_dc_sek = 3.69e-4 + 0.00295

        M_W_nea = 0.01 * 0.4 * 45_000 * 5.12e-5 * 6451  

        M_W_nep = 4e-3 * 5.12e-5 * 6451 * 8760 

        M_Z = Z_av * M_W_nea + Z_pl * M_W_nep

        results = {
            "omega_oc": round(omega_oc, 4),
            "t_v_oc": round(t_v_oc, 2),
            "k_a_oc": round(k_a_oc, 6),
            "k_n_oc": round(k_n_oc, 6),
            "omega_dc": f"{omega_dc:.4e}",
            "omega_dc_sek": f"{omega_dc_sek:.4e}",
            "M_W_nea": round(M_W_nea, 2),
            "M_W_nep": round(M_W_nep, 2),
            "M_Z": round(M_Z, 2),
        }
        return render_template("index.html", results=results)

    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(debug=True)
