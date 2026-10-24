import pandas as pd
from datetime import datetime

DATE_FORMATS = ['%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M', '%Y-%m-%d']

def chuan_hoa_diem(val, min_val, max_val):
    try:
        if pd.isna(val):
            return None
        score = int(val)
        if min_val <= score <= max_val:
            return score
        return None
    except (ValueError, TypeError):
        return None

def doc_ngay(raw):
    if pd.isna(raw):
        return None
    s = str(raw).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None
    