# 💎 Microservices Jewelry eCommerce Platform

<div align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-green.svg" alt="Status">
  <img src="https://img.shields.io/badge/Architecture-Microservices-orange.svg" alt="Architecture">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

## 📖 Giới thiệu

**Microservices Jewelry eCommerce** là một nền tảng thương mại điện tử chuyên về trang sức được xây dựng theo kiến trúc microservices hiện đại. Hệ thống cung cấp trải nghiệm mua sắm toàn diện với các tính năng quản lý sản phẩm, giỏ hàng, đơn hàng, thanh toán và chatbot AI.

### ✨ Tính năng chính

- 🏪 **Catalog Service**: Quản lý sản phẩm, danh mục, bộ sưu tập với hệ thống cache Redis
- 👤 **Account Service**: Xác thực người dùng, OAuth2 Google, quản lý tài khoản
- 🛒 **Cart & Order Service**: Giỏ hàng, đặt hàng, thanh toán MoMo
- 🤖 **Chatbot Service**: Tư vấn sản phẩm với Google Gemini AI
- 📱 **Delivery Service**: Ứng dụng mobile cho shipper (React Native Expo)
- 🔧 **Manager Service**: Quản lý backend cho admin
- 🌐 **API Gateway**: Điều phối và bảo mật API
- 🎨 **Micro Frontend**: Module Federation với Vite

### 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
├─────────────────────────────────────────────────────────────┤
│  Container App  │  Account UI  │  Catalog UI  │  Cart UI    │
│  (Module Fed)   │  (React)     │  (React)     │  (React)    │
├─────────────────────────────────────────────────────────────┤
│                     API Gateway                             │
├─────────────────────────────────────────────────────────────┤
│                   Microservices Layer                       │
├─────────────────┬───────────────┬───────────────┬───────────┤
│  Account        │  Catalog      │  Cart/Order   │  Chatbot  │
│  Service        │  Service      │  Service      │  Service  │
│  (Spring Boot)  │  (Spring Boot)│  (Node.js)    │  (Python) │
├─────────────────┴───────────────┴───────────────┴───────────┤
│                     Data Layer                              │
├─────────────────────────────────────────────────────────────┤
│     PostgreSQL Database     │      Redis Cache              │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Công nghệ sử dụng

### Backend
- **Spring Boot** (Java 17) - Account, Catalog, Manager Services
- **Node.js** (Express) - Cart/Order Service, API Gateway
- **Python** (Flask) - Chatbot Service
- **PostgreSQL** - Database chính
- **Redis** - Cache và session
- **Docker** - Container hóa

### Frontend
- **React 18** - User Interface
- **Vite** - Build tool và Module Federation
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Native Expo** - Mobile app cho delivery

### DevOps & Infrastructure
- **Docker Compose** - Container orchestration
- **Jenkins** - CI/CD Pipeline
- **Terraform** - Infrastructure as Code
- **Google Cloud Platform** - Cloud hosting
- **Nginx** - Reverse proxy (trong production)

### External APIs
- **Google OAuth2** - Đăng nhập xã hội
- **Google Gemini AI** - Chatbot intelligence
- **MoMo Payment** - Thanh toán điện tử
- **Gmail SMTP** - Email service

## 📦 Cấu trúc dự án

```
Microservices_Jewelry_eCommerce/
├── Backend/
│   └── Workspace/
│       ├── API_Gateway/           # API Gateway (Node.js)
│       ├── Service_Account/       # User management (Spring Boot)
│       ├── Service_Cart_Order/    # Shopping cart & orders (Node.js)
│       ├── Service_Catalog/       # Product catalog (Spring Boot)
│       ├── Service_Chatbot/       # AI Chatbot (Python)
│       └── Service_Manager/       # Admin management (Spring Boot)
├── Frontend/
│   └── Workspace/
│       ├── Container/             # Main container app (Vite + Module Federation)
│       ├── Service_Account/       # Account microfrontend
│       ├── Service_Catalog/       # Catalog microfrontend
│       ├── Service_Cart_Order/    # Cart & Order microfrontend
│       ├── Service_Manager/       # Admin panel microfrontend
│       └── Service_Delivery/      # Delivery mobile app (Expo)
├── Terraform/                     # Infrastructure as Code
├── Utility/
│   └── PNJ_Scraper/              # Data scraping utility
├── docker-compose.yml            # Main compose file
├── docker-compose.backend.yml    # Backend services
├── docker-compose.frontend.yml   # Frontend services
├── docker-compose.jenkins.yml    # CI/CD setup
└── Jenkinsfile                   # CI/CD pipeline
```

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống

- **Docker** & **Docker Compose**
- **Node.js** >= 18.x
- **Java** >= 17
- **Python** >= 3.9
- **Terraform** >= 1.0
- **Git** với submodules

### 🔧 Cài đặt local development

#### 1. Clone repository với submodules

```bash
git clone --recurse-submodules https://github.com/Zennisch/Microservices_Jewelry_eCommerce.git
cd Microservices_Jewelry_eCommerce
```

#### 2. Cấu hình environment variables

```bash
# Copy template và điền thông tin
cp .env.template .env

# Cấu hình các thông số sau trong file .env:
# - Database credentials
# - Google OAuth2 (Client ID & Secret)
# - Google Gemini API Key
# - Email SMTP settings
# - MoMo payment credentials (nếu có)
```

#### 3. Khởi chạy hệ thống

```bash
# Khởi động tất cả services
docker-compose up -d

# Hoặc khởi động từng layer riêng biệt:
# Backend only
docker-compose -f docker-compose.backend.yml up -d

# Frontend only  
docker-compose -f docker-compose.frontend.yml up -d
```

#### 4. Kiểm tra services

- **Frontend Container**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Account Service**: http://localhost:8001
- **Manager Service**: http://localhost:8003
- **Catalog Service**: http://localhost:8005
- **Cart/Order Service**: http://localhost:8006
- **Chatbot Service**: http://localhost:5000
- **PostgreSQL**: localhost:6543
- **Redis**: localhost:6379

### ☁️ Triển khai production trên Google Cloud

#### Yêu cầu GCP Services

Đảm bảo các services sau đã được enable trên Google Cloud Project:
- **Compute Engine API** - Tạo và quản lý VM instances
- **Google Identity Services** - OAuth2 authentication
- **IAM Service Account Credentials API** - Quản lý service accounts
- **Generative Language API** - Google Gemini AI cho chatbot

#### 1. Chuẩn bị GCP environment

```bash
# Copy Service Account JSON file vào root directory
cp path/to/your-service-account.json gcp_key.json

# Cấu hình Terraform variables
cd Terraform
cp terraform.tfvars.template terraform.tfvars

# Điền thông tin GCP trong terraform.tfvars:
# gcp_project = "your-project-id"
# gcp_region = "us-central1"  # hoặc region phù hợp
# ssh_public_key = "username:ssh-rsa AAAAB3NzaC1yc2E... username@hostname"
```

#### 2. Tạo infrastructure

```bash
# Khởi tạo Terraform
terraform init

# Tạo VM instance và firewall rules
terraform apply -auto-approve

# Lấy external IP của VM instance từ output hoặc GCP Console
```

#### 3. Cài đặt môi trường trên VM instance

```bash
# SSH vào VM instance
ssh -i path/to/private-key username@<VM_EXTERNAL_IP>

# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt Git
sudo apt install git -y

# Cấu hình Git (thay thế bằng thông tin của bạn)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Cài đặt Docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Cấu hình Docker permissions
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Cài đặt Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Kiểm tra cài đặt
docker --version
docker-compose --version
git --version

# Clone repository với submodules
git clone --recurse-submodules https://github.com/Zennisch/Microservices_Jewelry_eCommerce.git
cd Microservices_Jewelry_eCommerce
```

#### 4. Chuẩn bị môi trường production

```bash
# Tạo file .env từ template (trên VM)
cp .env.template .env

# Chỉnh sửa file .env với thông tin production
nano .env

# Cập nhật các biến môi trường sau:
# VITE_BACKEND_HOST=<VM_EXTERNAL_IP>
# VITE_FRONTEND_HOST=<VM_EXTERNAL_IP>
# ACCOUNT_SPRING_MAIL_USERNAME=your-email@gmail.com
# ACCOUNT_SPRING_MAIL_PASSWORD=your-app-password
# ACCOUNT_SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_GOOGLE_CLIENT_ID=your-client-id
# ACCOUNT_SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_GOOGLE_CLIENT_SECRET=your-client-secret
# GEMINI_API_KEY=your-gemini-api-key
```

#### 5. Setup CI/CD với Jenkins

```bash
# Khởi động Jenkins server (chạy trên VM hoặc local machine)
docker-compose -f docker-compose.jenkins.yml up -d

# Đợi Jenkins khởi động (khoảng 2-3 phút)
docker logs -f jenkins-blueocean

# Lấy admin password
docker exec jenkins-blueocean cat /var/jenkins_home/secrets/initialAdminPassword
```

#### 6. Cấu hình Jenkins Pipeline

1. **Truy cập Jenkins UI**: http://localhost:8080 (nếu chạy local) hoặc http://<VM_IP>:8080
2. **Cài đặt plugins**: Chọn "Install suggested plugins"
3. **Tạo admin user**: Điền thông tin admin user
4. **Thêm credentials**:
   - Vào "Manage Jenkins" → "Credentials" → "(global)" → "Add Credentials"
   - Tạo các credentials sau:
     ```
     Kind: Secret file
     ID: JEC_ENV_FILE
     File: Upload file .env
     
     Kind: Secret file
     ID: JEC_GCP_FILE
     File: Upload file gcp_key.json
     
     Kind: Secret file
     ID: JEC_SSH_FILE
     File: Upload SSH private key (id_ed25519 hoặc id_rsa)
     ```

5. **Tạo Pipeline**:
   - Dashboard → "New Item"
   - Tên: "Microservices_Jewelry_eCommerce"
   - Chọn "Pipeline" → "OK"
   - Trong "Pipeline" section:
     - Definition: "Pipeline script from SCM"
     - SCM: "Git"
     - Repository URL: `https://github.com/Zennisch/Microservices_Jewelry_eCommerce`
     - Branches: `*/master`
     - Additional Behaviours → "Advanced sub-modules behaviours" → "Recursively update submodules"
     - Script Path: `Jenkinsfile`
   - Save configuration

#### 7. Chạy deployment pipeline

```bash
# Trong Jenkins UI:
# 1. Vào pipeline "Microservices_Jewelry_eCommerce"
# 2. Click "Build Now"
# 3. Theo dõi build progress trong "Pipeline Overview" hoặc "Console Output"

# Kiểm tra logs realtime (nếu cần)
docker logs -f jenkins-blueocean
```

#### 8. Kiểm tra deployment

Sau khi pipeline hoàn thành thành công:

```bash
# Trên VM instance, kiểm tra containers đang chạy
docker ps

# Kiểm tra logs của các services
docker-compose logs -f

# Test các endpoints
curl http://<VM_EXTERNAL_IP>:8000/health  # API Gateway health check
curl http://<VM_EXTERNAL_IP>:3000         # Frontend application
```

**Truy cập ứng dụng**: http://`<VM_EXTERNAL_IP>`:3000

#### 9. Troubleshooting thường gặp

```bash
# Nếu Docker permission denied
sudo chmod 666 /var/run/docker.sock

# Nếu ports bị conflict
sudo netstat -tulpn | grep :8080  # Kiểm tra port usage

# Nếu out of disk space
docker system prune -af  # Dọn dẹp containers và images cũ

# Restart all services
docker-compose restart

# Xem logs chi tiết của service cụ thể
docker-compose logs -f service-name
```

#### 10. Optional: Import dữ liệu sản phẩm

```bash
# Mở firewall cho database port (chỉ từ IP của bạn)
gcloud compute firewall-rules create allow-postgres-6543 \
  --allow tcp:6543 \
  --source-ranges=<YOUR_IP_ADDRESS>/32 \
  --target-tags=allow-6543 \
  --description="Allow access to PostgreSQL for data import"

# Chạy scraper để import dữ liệu từ PNJ
cd Utility/PNJ_Scraper
python3 -m pip install -r requirements.txt
python3 src/PNJScraper.py

# Nhập thông tin khi được hỏi:
# - Item type: nhan, day-chuyen, lac, etc.
# - Start page: 1
# - End page: 5 (hoặc số trang muốn scrape)
```

### 📱 Setup Delivery Mobile App

```bash
cd Frontend/Workspace/Service_Delivery/service-delivery-expo/my-expo-app

# Cài đặt dependencies
npm install

# Chạy development server
npx expo start

# Build cho production
npx expo build:android  # hoặc build:ios
```

## 🔑 API Documentation

### Authentication Endpoints

```http
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/logout
GET  /api/v1/auth/account
```

### Product Catalog Endpoints

```http
GET    /api/v1/products
GET    /api/v1/products/{id}
GET    /api/v1/products/category/{categoryId}
GET    /api/v1/categories
GET    /api/v1/collections
```

### Cart & Order Endpoints

```http
GET    /api/v1/cart/{userId}
POST   /api/v1/cart/{userId}
PUT    /api/v1/cart-items/{cartItemId}
DELETE /api/v1/cart-items/{cartItemId}
POST   /api/v1/orders
GET    /api/v1/orders/user/{userId}
```

### Payment Endpoints

```http
POST /api/v1/payment
POST /api/v1/payment/verify
POST /api/v1/payment/confirmTransaction
```

## 🔒 Bảo mật

- **JWT Authentication** cho API access
- **OAuth2 với Google** cho đăng nhập xã hội
- **CORS** configuration cho cross-origin requests
- **Input validation** và **SQL injection** protection
- **Rate limiting** trên API Gateway
- **HTTPS** trong production environment

## 🧪 Testing

```bash
# Backend tests
cd Backend/Workspace/Service_Account/Service_Account_Backend
./gradlew test

cd Backend/Workspace/Service_Manager
./mvnw test

cd Backend/Workspace/Service_Cart_Order/Service_Cart_Order_Backend  
npm test

# Frontend tests
cd Frontend/Workspace/Container/container-vite
npm test

cd Frontend/Workspace/Service_Account/service-account-vite
npm test
```

## 📊 Monitoring & Logging

- **Docker logs** cho container monitoring
- **Application logs** trong `/app/logs`
- **Database query logging** 
- **Redis monitoring** với built-in commands
- **Jenkins build logs** cho CI/CD tracking

## 🛠️ Công cụ phát triển

### Data Scraping Tool

```bash
cd Utility/PNJ_Scraper
python src/PNJScraper.py

# Nhập loại sản phẩm (vd: nhan, day-chuyen, lac)
# Nhập page range để scrape data từ PNJ website
```

### Database Migration

```bash
# Auto migration khi khởi động services
# Schema được tạo tự động từ JPA entities (Spring Boot)
# hoặc Sequelize models (Node.js)
```

## 🤝 Đóng góp

### Team Development Workflow

1. **Fork** repository
2. Tạo **feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. Tạo **Pull Request**

### Code Standards

- **ESLint** + **Prettier** cho JavaScript/TypeScript
- **Checkstyle** cho Java code
- **Black** formatter cho Python
- **Conventional Commits** cho commit messages

## 📄 License

Dự án này được phân phối dưới giấy phép MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 👥 Thành viên dự án

| Tên thành viên | Vai trò | Email | GitHub |
|----------------|---------|-------|--------|
| [Nguyễn Thiên Phú] | Team Lead / Full-stack Developer / DevOps Engineer | zennisch@gmail.com | [@Thiên Phú](https://github.com/Zennisch) |
| [Vũ Quốc Huy] | Account & Admin Service Developer / DevOps Engineer | quochuyab2003@gmail.com | [@tuitenhyu](https://github.com/QuocHuyGIT103) |
| [Đinh Trần Phú Khang] | Cart & Order Service Developer / DevOps Engineer | dtphukhang210320033@gmail.com | [@DinhTranPhuKhang](https://github.com/khangdinh2103) |
| [Trần Quốc Khánh] | Manager Service Developer | tqkhanhsn@gmail.com | [@Khánh](https://github.com/Tq-Khanhs) |
| [Lê Đại Phát] | Product Service Developer / Fault-Tolerant Engineer | phatpro1208@gmail.com | [@Lê Đại Phát](https://github.com/ldp2003) |
| [Nguyễn Thanh Tuyền] | User Service Developer | nguyenthanhtuyen221103@gmail.com | [@Tuyền](https://github.com/ThanhTuyenz) |

## 📞 Liên hệ & Hỗ trợ

- **Repository**: [Microservices_Jewelry_eCommerce](https://github.com/Zennisch/Microservices_Jewelry_eCommerce)
- **Issues**: [GitHub Issues](https://github.com/Zennisch/Microservices_Jewelry_eCommerce/issues)
- **Wiki**: [Project Wiki](https://github.com/Zennisch/Microservices_Jewelry_eCommerce/wiki)

---

<div align="center">
  <p>⭐ Nếu dự án này hữu ích, hãy cho chúng tôi một star trên GitHub!</p>
  <p>Made with ❤️ by Jewelry eCommerce Team</p>
</div>