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