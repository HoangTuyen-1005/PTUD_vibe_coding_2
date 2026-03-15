import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';
import './App.css'; 

function Dashboard() {
  const [sachMuonNhieu, setSachMuonNhieu] = useState([]);
  const [docGiaChuaTra, setDocGiaChuaTra] = useState([]);
  const navigate = useNavigate();

  // useEffect sẽ chạy hàm fetchData ngay khi màn hình này hiện lên
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Gọi 2 API báo cáo cùng lúc
      const [resSach, resDocGia] = await Promise.all([
        api.get('/api/baocao/sach-muon-nhieu'),
        api.get('/api/baocao/docgia-chua-tra')
      ]);
      
      setSachMuonNhieu(resSach.data);
      setDocGiaChuaTra(resDocGia.data);
    } catch (error) {
      console.error("Lỗi khi tải dữ liệu:", error);
      // Nếu token hết hạn hoặc lỗi 401, tự động văng ra trang đăng nhập
      if (error.response && error.response.status === 401) {
        handleLogout();
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="dashboard-container" style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>📊 Trang Tổng Quan Thư Viện</h2>
        <button onClick={handleLogout} style={{ backgroundColor: '#ff4d4f', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>
          Đăng xuất
        </button>
      </div>

      <hr style={{ margin: '20px 0' }} />

      <div className="report-section">
        <h3>🔥 Top 5 Đầu Sách Mượn Nhiều Nhất</h3>
        <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', marginBottom: '30px' }}>
          <thead>
            <tr style={{ backgroundColor: '#f4f4f4' }}>
              <th>Tên Đầu Sách</th>
              <th>Số Lượt Mượn</th>
            </tr>
          </thead>
          <tbody>
            {sachMuonNhieu.length > 0 ? (
              sachMuonNhieu.map((sach, index) => (
                <tr key={index}>
                  <td>{sach.ten_dau_sach}</td>
                  <td>{sach.so_luot_muon} lượt</td>
                </tr>
              ))
            ) : (
              <tr><td colSpan="2" style={{ textAlign: 'center' }}>Chưa có dữ liệu mượn sách.</td></tr>
            )}
          </tbody>
        </table>

        <h3>⚠️ Danh Sách Độc Giả Chưa Trả Sách</h3>
        <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ backgroundColor: '#f4f4f4' }}>
              <th>Mã Độc Giả</th>
              <th>Họ Tên</th>
              <th>Lớp</th>
              <th>Mã Sách Đang Mượn</th>
              <th>Ngày Mượn</th>
            </tr>
          </thead>
          <tbody>
            {docGiaChuaTra.length > 0 ? (
              docGiaChuaTra.map((docgia, index) => (
                <tr key={index}>
                  <td>{docgia.ma_doc_gia}</td>
                  <td>{docgia.ho_ten}</td>
                  <td>{docgia.lop}</td>
                  <td>{docgia.ma_sach_dang_muon}</td>
                  <td>{docgia.ngay_muon}</td>
                </tr>
              ))
            ) : (
              <tr><td colSpan="5" style={{ textAlign: 'center' }}>Tuyệt vời! Không có độc giả nào trễ hạn trả sách.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;