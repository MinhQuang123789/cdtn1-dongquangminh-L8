import hashlib
import hmac
import os


def lay_khoa_bi_mat() -> bytes:
    khoa = os.environ.get("PSEUDO_KEY", "")
    if len(khoa) < 32:
        raise ValueError("PSEUDO_KEY phai co it nhat 32 ky tu")
    return khoa.encode("utf-8")


def gia_danh(gia_tri: str | int | None) -> str | None:
    """Gia danh hoa gia tri dinh danh bang HMAC-SHA256."""
    if gia_tri is None or str(gia_tri).strip() == "":
        return None
    khoa = lay_khoa_bi_mat()
    return hmac.new(khoa, str(gia_tri).strip().encode("utf-8"), hashlib.sha256).hexdigest()