import pandas as pd

# Fungsi membership segitiga
def triangle(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    else:
        return 0.0

# Membaca data restoran.xlsx
def read_data(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df

# Fuzzification untuk kualitas servis
def fuzzify_service(service_value):
    low = triangle(service_value, 0, 30, 50)
    medium = triangle(service_value, 30, 50, 70)
    high = triangle(service_value, 50, 70, 100)

    return {
        "low": low,
        "medium": medium,
        "high": high
    }

# Fuzzification untuk harga
def fuzzify_price(price_value):
    cheap = triangle(price_value, 25000, 30000, 35000)
    moderate = triangle(price_value, 30000, 37500, 45000)
    expensive = triangle(price_value, 40000, 47500, 55000)

    return {
        "cheap": cheap,
        "moderate": moderate,
        "expensive": expensive
    }

# Inferensi - menggunakan aturan fuzzy
def inferencing(service_fuzzy, price_fuzzy):
    # Aturan fuzzy: output adalah tingkat rekomendasi
    rules = {
        "highly_recommended": [],
        "recommended": [],
        "not_recommended": []
    }

    # Definisikan semua aturan
    # Misal: High Service & Cheap Price -> Highly Recommended
    rules["highly_recommended"].append(min(service_fuzzy["high"], price_fuzzy["cheap"]))
    rules["recommended"].append(min(service_fuzzy["high"], price_fuzzy["moderate"]))
    rules["recommended"].append(min(service_fuzzy["high"], price_fuzzy["expensive"]))
    rules["recommended"].append(min(service_fuzzy["medium"], price_fuzzy["cheap"]))
    rules["recommended"].append(min(service_fuzzy["medium"], price_fuzzy["moderate"]))
    rules["not_recommended"].append(min(service_fuzzy["medium"], price_fuzzy["expensive"]))
    rules["recommended"].append(min(service_fuzzy["low"], price_fuzzy["cheap"]))
    rules["not_recommended"].append(min(service_fuzzy["low"], price_fuzzy["moderate"]))
    rules["not_recommended"].append(min(service_fuzzy["low"], price_fuzzy["expensive"]))

    # Ambil nilai maksimum untuk setiap output
    return {
        "highly_recommended": max(rules["highly_recommended"]),
        "recommended": max(rules["recommended"]),
        "not_recommended": max(rules["not_recommended"])
    }

# Defuzzification - mencari skor dari hasil inferensi
def defuzzification(output_membership):
    # Skor untuk tiap output
    skor = {
        "highly_recommended": 90,
        "recommended": 70,
        "not_recommended": 50
    }

    numerator = (output_membership["highly_recommended"] * skor["highly_recommended"] +
                 output_membership["recommended"] * skor["recommended"] +
                 output_membership["not_recommended"] * skor["not_recommended"])

    denominator = (output_membership["highly_recommended"] +
                   output_membership["recommended"] +
                   output_membership["not_recommended"])

    if denominator == 0:
        return 0
    else:
        return numerator / denominator

# Menyimpan hasil ke peringkat.xlsx
def save_result(df_result, output_path):
    df_result.to_excel(output_path, index=False)

def main():
    # 1. Read data
    df = read_data('restoran.xlsx')
    print("Kolom-kolom di file:", df.columns.tolist())

    results = []

    # 2. Fuzzification, Inferencing, Defuzzification untuk setiap restoran
    for idx, row in df.iterrows():
        service_value = row['Pelayanan']
        price_value = row['harga']

        service_fuzzy = fuzzify_service(service_value)
        price_fuzzy = fuzzify_price(price_value)

        output_membership = inferencing(service_fuzzy, price_fuzzy)
        score = defuzzification(output_membership)

        results.append({
            "Id": row['id Pelanggan'],
            "Kualitas Servis": service_value,
            "Harga": price_value,
            "Skor": score
        })

    # 3. Sort dan pilih 5 restoran terbaik
    df_result = pd.DataFrame(results)
    df_result = df_result.sort_values(by="Skor", ascending=False).head(5)

    # 4. Save ke Excel
    save_result(df_result, 'peringkat.xlsx')
    print("Berhasil disimpan ke peringkat.xlsx!")

if __name__ == "__main__":
    main()
