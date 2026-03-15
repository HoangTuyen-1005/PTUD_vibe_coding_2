# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class NhanVien(Base):
    __tablename__ = "nhan_vien"
    ma_nhan_vien = Column(String, primary_key=True, index=True)
    ho_ten = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    vai_tro = Column(String, nullable=False) # 'Admin' hoặc 'ThuThu'

class DocGia(Base):
    __tablename__ = "doc_gia"
    ma_doc_gia = Column(String, primary_key=True, index=True)
    ho_ten = Column(String, nullable=False)
    lop = Column(String)
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String)

class ChuyenNganh(Base):
    __tablename__ = "chuyen_nganh"
    ma_chuyen_nganh = Column(String, primary_key=True, index=True)
    ten_chuyen_nganh = Column(String, nullable=False)
    mo_ta = Column(String)

class DauSach(Base):
    __tablename__ = "dau_sach"
    ma_dau_sach = Column(String, primary_key=True, index=True)
    ten_dau_sach = Column(String, nullable=False)
    nha_xuat_ban = Column(String)
    so_trang = Column(Integer)
    kich_thuoc = Column(String)
    tac_gia = Column(String)
    so_luong_sach = Column(Integer, default=0)
    ma_chuyen_nganh = Column(String, ForeignKey("chuyen_nganh.ma_chuyen_nganh"))
    
    chuyen_nganh = relationship("ChuyenNganh")

class BanSaoSach(Base):
    __tablename__ = "ban_sao_sach"
    ma_sach = Column(String, primary_key=True, index=True)
    ma_dau_sach = Column(String, ForeignKey("dau_sach.ma_dau_sach"))
    tinh_trang = Column(String, default="Sẵn sàng")
    ngay_nhap = Column(Date)
    
    dau_sach = relationship("DauSach")

class PhieuMuon(Base):
    __tablename__ = "phieu_muon"
    ma_phieu = Column(Integer, primary_key=True, autoincrement=True)
    ma_sach = Column(String, ForeignKey("ban_sao_sach.ma_sach"))
    ma_doc_gia = Column(String, ForeignKey("doc_gia.ma_doc_gia"))
    ma_thu_thu = Column(String, ForeignKey("nhan_vien.ma_nhan_vien"))
    ngay_muon = Column(Date)
    tinh_trang = Column(String, default="Đang mượn") # 'Đang mượn' hoặc 'Đã trả'