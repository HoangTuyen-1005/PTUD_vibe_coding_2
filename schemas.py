from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

# Base schema cho Độc giả
class DocGiaBase(BaseModel):
    ho_ten: str
    lop: Optional[str] = None
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None

# Schema khi tạo mới (Yêu cầu phải có mã độc giả)
class DocGiaCreate(DocGiaBase):
    ma_doc_gia: str

# Schema khi cập nhật (Có thể không cập nhật mã)
class DocGiaUpdate(DocGiaBase):
    pass

# Schema dùng để trả dữ liệu về (Response)
class DocGiaResponse(DocGiaBase):
    ma_doc_gia: str
    
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMAS CHO CHUYÊN NGÀNH ---
class ChuyenNganhBase(BaseModel):
    ten_chuyen_nganh: str
    mo_ta: Optional[str] = None

class ChuyenNganhCreate(ChuyenNganhBase):
    ma_chuyen_nganh: str

class ChuyenNganhResponse(ChuyenNganhBase):
    ma_chuyen_nganh: str
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMAS CHO ĐẦU SÁCH ---
class DauSachBase(BaseModel):
    ten_dau_sach: str
    nha_xuat_ban: Optional[str] = None
    so_trang: Optional[int] = None
    kich_thuoc: Optional[str] = None
    tac_gia: Optional[str] = None
    ma_chuyen_nganh: str # Khóa ngoại liên kết với Chuyên ngành

class DauSachCreate(DauSachBase):
    ma_dau_sach: str
    so_luong_sach: int = 0

class DauSachUpdate(DauSachBase):
    pass

class DauSachResponse(DauSachBase):
    ma_dau_sach: str
    so_luong_sach: int
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMAS CHO BẢN SAO SÁCH ---
class BanSaoSachBase(BaseModel):
    ma_dau_sach: str
    tinh_trang: str = "Sẵn sàng"
    ngay_nhap: date

class BanSaoSachCreate(BanSaoSachBase):
    ma_sach: str

class BanSaoSachResponse(BanSaoSachBase):
    ma_sach: str
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMAS CHO PHIẾU MƯỢN ---
class PhieuMuonBase(BaseModel):
    ma_sach: str
    ma_doc_gia: str
    ma_thu_thu: str # Bắt buộc phải có mã thủ thư trực quầy

class PhieuMuonCreate(PhieuMuonBase):
    pass

class PhieuMuonResponse(PhieuMuonBase):
    ma_phieu: int
    ngay_muon: date
    tinh_trang: str
    
    model_config = ConfigDict(from_attributes=True)