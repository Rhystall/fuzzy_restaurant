import pandas as pd

# Membaca data restoran.xlsx
def read_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Fuzzification untuk kualitas servis
def fuzzify_service(service_value):
    # Placeholder - nanti diisi fungsi keanggotaan
    return {
        "low": 0.0,
        "medium": 0.0,
        "high": 0.0
    }

# Fuzzification untuk harga
def fuzzify_price(price_value):
    # Placeholder - nanti diisi fungsi keanggotaan
    return {
        "cheap": 0.0,
        "moderate": 0.0,
        "expensive": 0.0
    }

# Inferensi - menggunakan aturan fuzzy
def inferencing(service_fuzzy, price_fuzzy):
    # Placeholder - nanti dibuat aturan inferensinya
    return {
        "not_recommended": 0.0,
        "recommended": 0.0,
        "highly_recommended": 0.0
    }

# Defuzzification - mencari skor dari hasil inferensi
def defuzzification(output_membership):
    # Placeholder - gunakan metode Centroid (rata-rata)
    return 0.0

# Menyimpan hasil ke peringkat.xlsx
def save_result(df_result, output_path):
    df_result.to_excel(output_path, index=False)

def main():
    # 1. Read data
    df = read_data('restoran.xlsx')

    results = []

    # 2. Fuzzification, Inferencing, Defuzzification untuk setiap restoran
    for idx, row in df.iterrows():
        service_value = row['Kualitas Servis']
        price_value = row['Harga']

        service_fuzzy = fuzzify_service(service_value)
        price_fuzzy = fuzzify_price(price_value)

        output_membership = inferencing(service_fuzzy, price_fuzzy)
        score = defuzzification(output_membership)

        results.append({
            "Id": idx + 1,
            "Kualitas Servis": service_value,
            "Harga": price_value,
            "Skor": score
        })

    # 3. Sort dan pilih 5 restoran terbaik
    df_result = pd.DataFrame(results)
    df_result = df_result.sort_values(by="Skor", ascending=False).head(5)

    # 4. Save ke Excel
    save_result(df_result, 'peringkat.xlsx')

if __name__ == "__main__":
    main()
