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

#### 1. Chuẩn bị GCP environment

```bash
# Cấu hình Terraform variables
cd Terraform
cp terraform.tfvars.template terraform.tfvars

# Điền thông tin GCP:
# - project_id
# - region
# - ssh_public_key
```

#### 2. Tạo infrastructure

```bash
# Khởi tạo Terraform
terraform init

# Tạo VM instance và firewall rules
terraform apply -auto-approve
```

#### 3. Setup CI/CD với Jenkins

```bash
# Khởi động Jenkins server
docker-compose -f docker-compose.jenkins.yml up -d

# Lấy admin password
docker exec jenkins-blueocean cat /var/jenkins_home/secrets/initialAdminPassword
```

#### 4. Cấu hình Jenkins Pipeline

1. Truy cập Jenkins UI: http://localhost:8080
2. Cài đặt plugins đề xuất
3. Tạo credentials:
   - **JEC_ENV_FILE**: Upload file `.env`
   - **JEC_GCP_FILE**: Upload file `gcp_key.json`
   - **JEC_SSH_FILE**: Upload SSH private key
4. Tạo pipeline từ SCM với repository URL
5. Chạy pipeline để deploy lên GCP

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
| [Tên thành viên 1] | Team Lead / Full-stack Developer | email1@example.com | [@username1](https://github.com/username1) |
| [Tên thành viên 2] | Backend Developer | email2@example.com | [@username2](https://github.com/username2) |
| [Tên thành viên 3] | Frontend Developer | email3@example.com | [@username3](https://github.com/username3) |
| [Tên thành viên 4] | DevOps Engineer | email4@example.com | [@username4](https://github.com/username4) |
| [Tên thành viên 5] | Mobile Developer | email5@example.com | [@username5](https://github.com/username5) |

## 📞 Liên hệ & Hỗ trợ

- **Repository**: [Microservices_Jewelry_eCommerce](https://github.com/Zennisch/Microservices_Jewelry_eCommerce)
- **Issues**: [GitHub Issues](https://github.com/Zennisch/Microservices_Jewelry_eCommerce/issues)
- **Wiki**: [Project Wiki](https://github.com/Zennisch/Microservices_Jewelry_eCommerce/wiki)

---

<div align="center">
  <p>⭐ Nếu dự án này hữu ích, hãy cho chúng tôi một star trên GitHub!</p>
  <p>Made with ❤️ by Jewelry eCommerce Team</p>
</div>