import pytest
from src.transform.rules import chuan_hoa_diem

# LOẠI 1 - Luồng đúng: Điểm hợp lệ trong khoảng cho phép
@pytest.mark.parametrize('tho, mong_doi', [
    (5, 5),
    ('4', 4),
    (8, 8)  # Ví dụ điểm NPS (từ 0-10)
])
def test_TR01_chuan_hoa_diem_luong_dung(tho, mong_doi):
    assert chuan_hoa_diem(tho, 0, 10) == mong_doi

# LOẠI 2 - Giá trị biên: Kiểm tra giới hạn 1 và 5 của thang đo CSAT
@pytest.mark.parametrize('tho, mong_doi', [
    (1, 1),      # Biên dưới
    (5, 5),      # Biên trên
    (0, None),   # Dưới biên (Không hợp lệ)
    (6, None)    # Trên biên (Không hợp lệ)
])
def test_TR02_chuan_hoa_diem_bien(tho, mong_doi):
    assert chuan_hoa_diem(tho, 1, 5) == mong_doi

# LOẠI 3 - Dữ liệu sai: Rỗng hoặc chữ rác thì trả về None, KHÔNG sập hệ thống
@pytest.mark.parametrize('tho', [None, '', 'abc', '10/10/2026'])
def test_TR03_du_lieu_rac(tho):
    assert chuan_hoa_diem(tho, 1, 5) is None