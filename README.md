# 🌟 Game NFT API

Dự án **Game NFT API** cung cấp backend cho nền tảng website game blockchain. Dự án được xây dựng với **Django**, **Django REST Framework**, và tích hợp ví **Solana** để xác thực người dùng. Hệ thống đảm bảo khả năng mở rộng, bảo mật và dễ dàng triển khai với Railway.

---

## 🚀 Tính năng nổi bật

- 🔐 Xác thực người dùng bằng JWT và API Key
- 🎮 Kết nối và xác thực người dùng qua ví Solana
- 🖼️ Quản lý ảnh/media, lưu trữ trên Amazon S3
- 📊 Hệ thống phân loại nội dung (tagging)
- 🌍 Nhận diện thiết bị người dùng truy cập
- 🎨 Tích hợp CKEditor 5 trong Admin
- 🌐 Hỗ trợ CORS để tích hợp frontend (React, Vue, v.v.)
- ⚙️ Đầy đủ cấu hình cho Railway, dễ deploy

---

## 🧰 Công nghệ sử dụng

- **Django 4+**
- **Django REST Framework**
- **JWT** (`djangorestframework-simplejwt`)
- **Solana SDK** (`solana`, `pynacl`, `cryptography`)
- **Amazon S3** (`boto3`, `django-storages`)
- **PostgreSQL** (qua `psycopg2-binary`)
- `django-cors-headers`, `django-taggit`, `gunicorn`, `whitenoise`, v.v.

---

## 🖥️ Cài đặt local

### 1. Clone dự án

```bash
git clone https://github.com/KaiO277/da_game_bc.git
cd backend_api/
```

2. Tạo virtual environment và cài packages
```bash
python -m venv env
source env/bin/activate  # Trên Windows: env\Scripts\activate
pip install -r requirements.txt
```

3. Tạo file .env
Tạo file .env ở thư mục gốc:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:5173
```

4. Chạy migrate và khởi động server
```bash
python manage.py migrate
python manage.py runserver
```


☁️ Triển khai lên Railway
🚀 Cấu hình cần thiết
✅ Procfile
```bash
web: python manage.py migrate && gunicorn backend_api.wsgi --bind 0.0.0.0:$PORT
```


✅ Theo dõi log
Sử dụng Railway CLI (tùy chọn):

```bash
railway logs
```
🔐 Xác thực người dùng
JWT: Token-based Auth (login, refresh, verify)

API Key: Cho dịch vụ nội bộ

Solana Auth: Xác thực ví người dùng bằng chữ ký số

🔗 Tích hợp ví Solana
Người dùng đăng nhập bằng public key ví

Server xác thực chữ ký và tạo tài khoản

Giao tiếp qua solana, pynacl, cryptography
