import pandas as pd
import os

def run_pipeline():
    # Đường dẫn tới file csv (lấy từ thư mục gốc của project)
    file_path = 'data/sample/survey_sample.csv'
    
    print(f"Đang đọc dữ liệu từ: {file_path}")
    
    if not os.path.exists(file_path):
        print("Không tìm thấy file dữ liệu!")
        return

    # Đọc dữ liệu bằng pandas
    df = pd.read_csv(file_path)
    
    # In ra số dòng, số cột
    print(f"Số dòng: {df.shape[0]}")
    print(f"Số cột: {df.shape[1]}")
    
    # In ra tỉ lệ ô trống của từng cột
    print("\nTỉ lệ ô trống từng cột (%):")
    missing_ratio = (df.isnull().sum() / len(df)) * 100
    print(missing_ratio)

if __name__ == "__main__":
    run_pipeline()