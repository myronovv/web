from flask import Flask, render_template, request

app = Flask(__name__)

def calculator(hp, cp, sp, np, op, wp, ap):
    if wp + ap >= 100:
        return "Помилка у введених даних!"
    
    k_ps = round(100 / (100 - wp) , 2)
    k_pg = round(100 / (100 - wp - ap) , 2)
    
    hs = round(hp * k_ps, 2)
    cs = round(cp * k_ps, 2)
    ss = round(sp * k_ps, 2)
    ns = round(np * k_ps, 2)
    os = round(op * k_ps, 2)
    as_ = round(ap * k_ps, 2)
    
    hg = round(hp * k_pg, 2)
    cg = round(cp * k_pg, 2)
    sg = round(sp * k_pg, 2)
    ng = round(np * k_pg, 2)
    og = round(op * k_pg, 2)
    
    q_r = round(339 * cp + 1030 * hp - 108.8 * (op - sp) - 25 * wp, 3)
    q_r = q_r / 1000
    q_s = round((q_r + 0.025 * wp) * (100 / (100 - wp)), 2)
    q_g = round((q_r + 0.025 * wp) * (100 / (100 - wp - ap)), 2)
    
    return {
        "k_ps": k_ps,
        "k_pg": k_pg,
        "hs": hs, "cs": cs, "ss": ss, "ns": ns, "os": os, "as": as_,
        "hg": hg, "cg": cg, "sg": sg, "ng": ng, "og": og,
        "q_r": q_r, "q_s": q_s, "q_g": q_g
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            hp = float(request.form["hp"])
            cp = float(request.form["cp"])
            sp = float(request.form["sp"])
            np = float(request.form["np"])
            op = float(request.form["op"])
            wp = float(request.form["wp"])
            ap = float(request.form["ap"])
            
            result = calculator(hp, cp, sp, np, op, wp, ap)
        except ValueError:
            result = "Помилка у введених даних!"
    
    return render_template("index1.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
