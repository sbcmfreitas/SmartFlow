# SmartFlow API

SmartFlow is a REST API focused on managing device transactions, built with FastAPI and SQLite.

## Features

- **Authentication**: JWT Bearer Token.
- **Transactions**: Start, Finish, and Search transactions.
- **Time Tracking**: Calculates intervals between start and finish.
- **Admin UI**: SQLite-Web interface for database management.
- **Robustness**: Validation for duplicate transactions, timezone-naive datetime handling, and comprehensive logging.

---

## 🚀 How to Run

### Option 1: Docker / CasaOS (Recommended)

This project includes a `docker-compose.yml` file, making it ready for deployment on CasaOS or any Docker environment.

#### **For CasaOS:**

1. **Access the Terminal** of your CasaOS/Server.
2. **Clone this repository** or copy the files to a folder (e.g., `/DATA/AppData/smartflow`).
3. **Navigate to the folder**:
   ```bash
   cd /DATA/AppData/smartflow
   ```
4. **Run the application**:

   ```bash
   docker-compose up -d --build
   ```

   _Note: Using `--build` is crucial to create the custom image defined in `Dockerfile`._

5. **Import into CasaOS Dashboard (Optional)**:
   - You can add a "Custom App" in CasaOS UI.
   - Set the `Web UI` port to `8080` (Admin) or `8000` (API Docs).

#### **Ports:**

- **API & Docs**: `http://<server-ip>:8000`
- **Database Admin**: `http://<server-ip>:8080`

### Option 2: Local Development (Python)

**Prerequisites**: Python 3.10+ and Poetry.

1. **Install Dependencies**:
   ```bash
   poetry install
   ```
2. **Run the API**:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
3. **Access**:
   - Docs: http://127.0.0.1:8000/docs
   - Admin: Not available in this mode (unless you run `sqlite_web` manually).

---

## 🔑 Authentication

The system automatically creates a default user on first startup.

- **Username**: `admin`
- **Password**: `admin`

**How to Login:**
Use the `/login` endpoint to get a Bearer Token.

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin"
```

---

## 📡 API Usage

### 1. Start Transaction

POST `/transaction/start`

```json
{
  "device_id": "device_01",
  "entity_id": "entity_01"
}
```

### 2. Finish Transaction

POST `/transaction/finish?transaction_id=UUID`

```json
{}
```

_Returns 400 if transaction is already finished._

### 3. Search Transactions

GET `/transaction/search`
_Returns list of transactions with start_time, end_time, and calculated interval._
