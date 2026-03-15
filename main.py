from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import auth
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from sqlalchemy import func, desc

import models
import schemas
from database import engine, get_db

# Tạo bảng trong database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống Quản lý Thư viện - Vibe Coding 2")

# --- BẮT ĐẦU ĐOẠN CẤU HÌNH CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi nguồn (Frontend) gọi tới
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép mọi phương thức GET, POST, PUT, DELETE
    allow_headers=["*"],
)
# --- KẾT THÚC ĐOẠN CẤU HÌNH CORS ---

@app.post("/api/docgia/", response_model=schemas.DocGiaResponse, tags=["Quản lý Độc giả"])
def tao_the_thu_vien(docgia: schemas.DocGiaCreate, db: Session = Depends(get_db)):
    # Kiểm tra xem mã độc giả đã tồn tại chưa
    db_docgia = db.query(models.DocGia).filter(models.DocGia.ma_doc_gia == docgia.ma_doc_gia).first()
    if db_docgia:
        raise HTTPException(status_code=400, detail="Mã độc giả đã tồn tại trong hệ thống")
    
    # Tạo mới
    new_docgia = models.DocGia(**docgia.model_dump())
    db.add(new_docgia)
    db.commit()
    db.refresh(new_docgia)
    return new_docgia

@app.get("/api/docgia/", response_model=List[schemas.DocGiaResponse], tags=["Quản lý Độc giả"])
def lay_danh_sach_doc_gia(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.DocGia).offset(skip).limit(limit).all()

@app.put("/api/docgia/{ma_doc_gia}", response_model=schemas.DocGiaResponse, tags=["Quản lý Độc giả"])
def sua_thong_tin_the(ma_doc_gia: str, docgia_update: schemas.DocGiaUpdate, db: Session = Depends(get_db)):
    db_docgia = db.query(models.DocGia).filter(models.DocGia.ma_doc_gia == ma_doc_gia).first()
    if not db_docgia:
        raise HTTPException(status_code=404, detail="Không tìm thấy thẻ thư viện")
    
    # Cập nhật thông tin
    update_data = docgia_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_docgia, key, value)
        
    db.commit()
    db.refresh(db_docgia)
    return db_docgia

@app.delete("/api/docgia/{ma_doc_gia}", tags=["Quản lý Độc giả"])
def xoa_the_thu_vien(ma_doc_gia: str, db: Session = Depends(get_db)):
    db_docgia = db.query(models.DocGia).filter(models.DocGia.ma_doc_gia == ma_doc_gia).first()
    if not db_docgia:
        raise HTTPException(status_code=404, detail="Không tìm thấy thẻ thư viện")
    
    db.delete(db_docgia)
    db.commit()
    return {"message": f"Đã xóa thành công thẻ thư viện {ma_doc_gia}"}

# ==========================================
# API QUẢN LÝ CHUYÊN NGÀNH
# ==========================================
@app.post("/api/chuyennganh/", response_model=schemas.ChuyenNganhResponse, tags=["Quản lý Sách"])
def them_chuyen_nganh(chuyennganh: schemas.ChuyenNganhCreate, db: Session = Depends(get_db)):
    db_cn = db.query(models.ChuyenNganh).filter(models.ChuyenNganh.ma_chuyen_nganh == chuyennganh.ma_chuyen_nganh).first()
    if db_cn:
        raise HTTPException(status_code=400, detail="Mã chuyên ngành đã tồn tại")
    
    new_cn = models.ChuyenNganh(**chuyennganh.model_dump())
    db.add(new_cn)
    db.commit()
    db.refresh(new_cn)
    return new_cn

@app.get("/api/chuyennganh/", response_model=List[schemas.ChuyenNganhResponse], tags=["Quản lý Sách"])
def lay_danh_sach_chuyen_nganh(db: Session = Depends(get_db)):
    return db.query(models.ChuyenNganh).all()

# ==========================================
# API QUẢN LÝ ĐẦU SÁCH VÀ BẢN SAO SÁCH
# ==========================================
@app.post("/api/dausach/", response_model=schemas.DauSachResponse, tags=["Quản lý Sách"])
def them_dau_sach(dausach: schemas.DauSachCreate, db: Session = Depends(get_db)):
    # Kiểm tra chuyên ngành có tồn tại không
    db_cn = db.query(models.ChuyenNganh).filter(models.ChuyenNganh.ma_chuyen_nganh == dausach.ma_chuyen_nganh).first()
    if not db_cn:
        raise HTTPException(status_code=404, detail="Không tìm thấy Mã chuyên ngành này")
        
    db_ds = db.query(models.DauSach).filter(models.DauSach.ma_dau_sach == dausach.ma_dau_sach).first()
    if db_ds:
        raise HTTPException(status_code=400, detail="Mã đầu sách đã tồn tại")
    
    new_ds = models.DauSach(**dausach.model_dump())
    db.add(new_ds)
    db.commit()
    db.refresh(new_ds)
    return new_ds

@app.post("/api/bansaosach/", response_model=schemas.BanSaoSachResponse, tags=["Quản lý Sách"])
def nhap_ban_sao_sach(bansaosach: schemas.BanSaoSachCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra đầu sách có tồn tại không
    db_ds = db.query(models.DauSach).filter(models.DauSach.ma_dau_sach == bansaosach.ma_dau_sach).first()
    if not db_ds:
        raise HTTPException(status_code=404, detail="Không tìm thấy Đầu sách này để thêm bản sao")
        
    # 2. Kiểm tra mã bản sao sách đã tồn tại chưa
    db_bss = db.query(models.BanSaoSach).filter(models.BanSaoSach.ma_sach == bansaosach.ma_sach).first()
    if db_bss:
        raise HTTPException(status_code=400, detail="Mã cuốn sách này đã tồn tại")

    # 3. Thêm bản sao sách mới
    new_bss = models.BanSaoSach(**bansaosach.model_dump())
    db.add(new_bss)
    
    # 4. Tự động cập nhật số lượng sách trong bảng DauSach
    db_ds.so_luong_sach += 1
    
    db.commit()
    db.refresh(new_bss)
    return new_bss

# ==========================================
# API QUẢN LÝ MƯỢN / TRẢ SÁCH
# ==========================================
@app.post("/api/phieumuon/", response_model=schemas.PhieuMuonResponse, tags=["Quản lý Mượn Trả"])
def tao_phieu_muon(phieumuon: schemas.PhieuMuonCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra mã độc giả có hợp lệ không
    doc_gia = db.query(models.DocGia).filter(models.DocGia.ma_doc_gia == phieumuon.ma_doc_gia).first()
    if not doc_gia:
        raise HTTPException(status_code=404, detail="Không tìm thấy thẻ độc giả này")
    
    # 2. RÀNG BUỘC: Mỗi độc giả chỉ được mượn 1 cuốn sách cùng lúc
    phieu_dang_muon = db.query(models.PhieuMuon).filter(
        models.PhieuMuon.ma_doc_gia == phieumuon.ma_doc_gia,
        models.PhieuMuon.tinh_trang == "Đang mượn"
    ).first()
    if phieu_dang_muon:
        raise HTTPException(status_code=400, detail="Độc giả này đang mượn 1 cuốn sách chưa trả. Phải trả sách cũ trước khi mượn mới.")

    # 3. Kiểm tra mã cuốn sách có tồn tại và đang rảnh không
    ban_sao_sach = db.query(models.BanSaoSach).filter(models.BanSaoSach.ma_sach == phieumuon.ma_sach).first()
    if not ban_sao_sach:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã cuốn sách này")
    if ban_sao_sach.tinh_trang != "Sẵn sàng":
        raise HTTPException(status_code=400, detail="Cuốn sách này hiện không có sẵn (đã được mượn hoặc hỏng)")
    
    # 4. Tạo phiếu mượn mới
    new_phieu = models.PhieuMuon(
        ma_sach=phieumuon.ma_sach,
        ma_doc_gia=phieumuon.ma_doc_gia,
        ma_thu_thu=phieumuon.ma_thu_thu,
        ngay_muon=date.today(),
        tinh_trang="Đang mượn"
    )
    db.add(new_phieu)
    
    # 5. Đổi trạng thái của cuốn sách thành 'Đang mượn'
    ban_sao_sach.tinh_trang = "Đang mượn"
    
    db.commit()
    db.refresh(new_phieu)
    return new_phieu

@app.put("/api/phieumuon/{ma_phieu}/trasach", response_model=schemas.PhieuMuonResponse, tags=["Quản lý Mượn Trả"])
def tra_sach(ma_phieu: int, db: Session = Depends(get_db)):
    # 1. Lấy thông tin phiếu mượn
    phieu_muon = db.query(models.PhieuMuon).filter(models.PhieuMuon.ma_phieu == ma_phieu).first()
    if not phieu_muon:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu mượn này")
    if phieu_muon.tinh_trang == "Đã trả":
        raise HTTPException(status_code=400, detail="Phiếu mượn này đã được hoàn tất trả sách trước đó")

    # 2. Tìm cuốn sách để cập nhật lại trạng thái
    ban_sao_sach = db.query(models.BanSaoSach).filter(models.BanSaoSach.ma_sach == phieu_muon.ma_sach).first()
    
    # 3. Thực hiện trả sách: Đổi trạng thái phiếu và trạng thái sách
    phieu_muon.tinh_trang = "Đã trả"
    if ban_sao_sach:
        ban_sao_sach.tinh_trang = "Sẵn sàng"
        
    db.commit()
    db.refresh(phieu_muon)
    return phieu_muon

# ==========================================
# API BÁO CÁO THỐNG KÊ
# ==========================================
@app.get("/api/baocao/sach-muon-nhieu", tags=["Báo cáo Thống kê"])
def bao_cao_sach_muon_nhieu_nhat(limit: int = 5, db: Session = Depends(get_db)):
    # Báo cáo 1: Thông tin các đầu sách cho mượn nhiều nhất
    # Logic: Join PhieuMuon -> BanSaoSach -> DauSach, sau đó đếm (count) và sắp xếp giảm dần (desc)
    result = db.query(
        models.DauSach.ten_dau_sach,
        func.count(models.PhieuMuon.ma_phieu).label("so_luot_muon")
    ).join(
        models.BanSaoSach, models.BanSaoSach.ma_sach == models.PhieuMuon.ma_sach
    ).join(
        models.DauSach, models.DauSach.ma_dau_sach == models.BanSaoSach.ma_dau_sach
    ).group_by(
        models.DauSach.ma_dau_sach
    ).order_by(
        desc("so_luot_muon")
    ).limit(limit).all()
    
    # Chuyển đổi kết quả thành list dạng JSON
    return [{"ten_dau_sach": row.ten_dau_sach, "so_luot_muon": row.so_luot_muon} for row in result]

@app.get("/api/baocao/docgia-chua-tra", tags=["Báo cáo Thống kê"])
def bao_cao_doc_gia_chua_tra(db: Session = Depends(get_db)):
    # Báo cáo 2: Thông tin về các độc giả chưa trả sách
    # Logic: Tìm các phiếu mượn có tình trạng "Đang mượn" và join lấy thông tin người mượn
    result = db.query(
        models.DocGia.ma_doc_gia,
        models.DocGia.ho_ten,
        models.DocGia.lop,
        models.PhieuMuon.ma_sach,
        models.PhieuMuon.ngay_muon
    ).join(
        models.PhieuMuon, models.PhieuMuon.ma_doc_gia == models.DocGia.ma_doc_gia
    ).filter(
        models.PhieuMuon.tinh_trang == "Đang mượn"
    ).all()
    
    return [
        {
            "ma_doc_gia": row.ma_doc_gia, 
            "ho_ten": row.ho_ten, 
            "lop": row.lop,
            "ma_sach_dang_muon": row.ma_sach,
            "ngay_muon": row.ngay_muon
        } for row in result
    ]

# ==========================================
# API QUẢN TRỊ VIÊN & XÁC THỰC
# ==========================================
@app.post("/api/nhanvien/", response_model=schemas.NhanVienResponse, tags=["Quản lý Hệ thống"])
def tao_tai_khoan_nhan_vien(nhanvien: schemas.NhanVienCreate, db: Session = Depends(get_db)):
    # Nghiệp vụ: Quản trị viên cập nhật thông tin thủ thư vào hệ thống, tạo tài khoản và cấp quyền 
    db_nv = db.query(models.NhanVien).filter(models.NhanVien.ma_nhan_vien == nhanvien.ma_nhan_vien).first()
    if db_nv:
        raise HTTPException(status_code=400, detail="Mã nhân viên đã tồn tại")
        
    db_user = db.query(models.NhanVien).filter(models.NhanVien.username == nhanvien.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username này đã được sử dụng")

    # Băm mật khẩu trước khi lưu vào database
    hashed_pwd = auth.get_password_hash(nhanvien.password)
    
    new_nv = models.NhanVien(
        ma_nhan_vien=nhanvien.ma_nhan_vien,
        ho_ten=nhanvien.ho_ten,
        username=nhanvien.username,
        password_hash=hashed_pwd,
        vai_tro=nhanvien.vai_tro
    )
    db.add(new_nv)
    db.commit()
    db.refresh(new_nv)
    return new_nv

@app.post("/api/login", response_model=schemas.Token, tags=["Xác thực"])
def dang_nhap(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Tìm user trong database
    user = db.query(models.NhanVien).filter(models.NhanVien.username == form_data.username).first()
    
    # Kiểm tra user có tồn tại và mật khẩu có khớp không
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Sai username hoặc password")

    # Tạo token chứa thông tin username và vai trò (Admin/ThuThu)
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.vai_tro})
    return {"access_token": access_token, "token_type": "bearer"}