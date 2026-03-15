from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Tạo bảng trong database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống Quản lý Thư viện - Vibe Coding 2")

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