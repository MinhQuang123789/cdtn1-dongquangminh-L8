import csv

file_path = "data/sample/warranty_sample.csv"

rows = []
with open(file_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for r in reader:
        rows.append(r)

header = rows[0]
data_rows = rows[1:]

print("=" * 50)
print("   KẾT QUẢ SMOKE TEST - TRACK DATA ANALYTICS")
print("=" * 50)
print(f"-> Số dòng dữ liệu (không tính tiêu đề): {len(data_rows)}")
print(f"-> Số cột dữ liệu: {len(header)}")
print(f"-> Các trường dữ liệu: {', '.join(header)}")
print("\n5 bản ghi đầu tiên:")
for r in data_rows[:5]:
    print(r)
print("=" * 50)