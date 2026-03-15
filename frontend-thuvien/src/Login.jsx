import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';
import './App.css'; // Dùng tạm CSS mặc định của Vite

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    // FastAPI OAuth2 bắt buộc gửi dữ liệu dạng form-urlencoded
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await api.post('/api/login', formData);
      // Lưu token vào LocalStorage để dùng cho các API sau
      localStorage.setItem('token', response.data.access_token);
      alert('Đăng nhập thành công!');
      navigate('/dashboard'); // Chuyển hướng sang trang quản lý
    } catch (err) {
      setError('Sai username hoặc mật khẩu. Vui lòng thử lại!');
    }
  };

  return (
    <div className="login-container">
      <h2>Hệ Thống Quản Lý Thư Viện</h2>
      <form onSubmit={handleLogin} className="login-form">
        <div>
          <label>Tài khoản: </label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Mật khẩu: </label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        {error && <p style={{color: 'red'}}>{error}</p>}
        <button type="submit">Đăng Nhập</button>
      </form>
    </div>
  );
}

export default Login;