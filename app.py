import pandas as pd
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    search_data = {
        "type": request.args.get("type"),
        "location": request.args.get("location"),
        "price_min": request.args.get("price_min"),
        "price_max": request.args.get("price_max"),
        "size_min": request.args.get("size_min"),
        "bedrooms_min": request.args.get("bedrooms_min"),
        "pet_friendly": request.args.get("pet_friendly")
    }

    import pandas as pd

    # โหลดข้อมูล Excel
    df = pd.read_excel("sonic_real_data.xlsx")

    # เริ่มกรองข้อมูล
    results = df.copy()

    if search_data["type"]:
        results = results[results["ชนิด"] == search_data["type"]]

    if search_data["location"]:
        results = results[results["โลเคชั่น"].str.lower().str.contains(search_data["location"].lower())]

    if search_data["price_min"]:
        results = results[results["ราคา"] >= int(search_data["price_min"])]

    if search_data["price_max"]:
        results = results[results["ราคา"] <= int(search_data["price_max"])]

    if search_data["size_min"]:
        results = results[results["ขนาด"] >= float(search_data["size_min"])]

    if search_data["bedrooms_min"]:
        if search_data["bedrooms_min"].lower() == "studio":
            results = results[results["ห้องนอน"].astype(str).str.lower() == "studio"]
        else:
            results = results[results["ห้องนอน"] == int(search_data["bedrooms_min"])]

    if search_data["pet_friendly"]:
        expected = "ได้" if search_data["pet_friendly"] == "yes" else "ไม่ได้"
        results = results[results["เลี้ยงสัตว์"] == expected]

    # ส่งข้อมูลที่กรองแล้วไปแสดงผล
    return render_template("results.html", rooms=results.to_dict(orient="records"))

@app.route('/all')
def show_all():
    df = pd.read_excel("sonic_real_data.xlsx")
    return render_template("results.html", rooms=df.to_dict(orient="records"))



if __name__ == '__main__':
    app.run(debug=True)
