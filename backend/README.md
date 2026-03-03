# 🚗 Car Rental App — Backend API Documentation

> **For Frontend Developers** — Everything you need to know to connect your frontend to this Flask backend.

---

## 🌐 Base URL

```
http://127.0.0.1:5000
```

> Flask runs on port **5000** by default when started with `python app.py`.  
> All API routes are prefixed with `/api`.

---

## 🔐 Authentication

This API uses **JWT (JSON Web Tokens)**.

- After login, you receive an `access_token`.
- For **protected routes**, include it in every request header:

```
Authorization: Bearer <your_access_token>
```

> ⚠️ Currently implemented protected routes use `@jwt_required()` — always send the token for any route that needs user identity.

---

## 📡 API Endpoints

### 🔑 Auth Routes — `/api/auth`

---

#### `POST /api/auth/register`

Register a new user.

**Request Body (JSON):**
```json
{
  "name": "Anas",
  "email": "anas@example.com",
  "password": "yourpassword"
}
```

**Success Response — `201 Created`:**
```json
{
  "message": "User registered successfully"
}
```

**Error Response — `400 Bad Request`:**
```json
{
  "message": "Email already exists"
}
```

---

#### `POST /api/auth/login`

Login and receive a JWT token.

**Request Body (JSON):**
```json
{
  "email": "anas@example.com",
  "password": "yourpassword"
}
```

**Success Response — `200 OK`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "user_id": 1,
  "role": "renter"
}
```

> 🔑 Save the `access_token` and `user_id` — you'll need them for all protected requests.

**Error Response — `401 Unauthorized`:**
```json
{
  "message": "Invalid credentials"
}
```

---

### 🛡️ Protected Test Route

> ⚠️ This route is for testing JWT auth only.

#### `GET /api/test/protected` *(requires JWT)*

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response — `200 OK`:**
```json
{
  "message": "Access granted",
  "user_id": 1
}
```

---

## 🗂️ Data Models (What the database stores)

### 👤 User
| Field        | Type    | Notes                          |
|--------------|---------|--------------------------------|
| `user_id`    | Integer | Primary key (auto)             |
| `name`       | String  |                                |
| `email`      | String  | Unique                         |
| `password_hash` | String | Stored hashed, never sent back |
| `role`       | String  | `"renter"` (default) or `"owner"` |
| `created_at` | DateTime |                               |

---

### 🚘 Car
| Field           | Type    | Notes                         |
|-----------------|---------|-------------------------------|
| `car_id`        | Integer | Primary key (auto)            |
| `owner_id`      | Integer | FK → User                     |
| `brand`         | String  | e.g. Toyota                   |
| `model`         | String  | e.g. Corolla                  |
| `city`          | String  |                               |
| `price_per_day` | Decimal | e.g. 1500.00                  |
| `is_available`  | Boolean | `true` or `false`             |
| `created_at`    | DateTime |                              |

---

### 📋 Booking
| Field          | Type    | Notes                                      |
|----------------|---------|--------------------------------------------|
| `booking_id`   | Integer | Primary key (auto)                         |
| `car_id`       | Integer | FK → Car                                   |
| `owner_id`     | Integer | FK → User (car owner)                      |
| `customer_id`  | Integer | FK → User (person renting)                 |
| `start_date`   | Date    | Format: `YYYY-MM-DD`                       |
| `end_date`     | Date    | Format: `YYYY-MM-DD`                       |
| `total_amount` | Decimal | Calculated total                           |
| `status`       | String  | `"pending"`, `"confirmed"`, `"cancelled"`  |
| `created_at`   | DateTime |                                           |

---

### 💳 Payment
| Field            | Type    | Notes                                     |
|------------------|---------|-------------------------------------------|
| `payment_id`     | Integer | Primary key (auto)                        |
| `booking_id`     | Integer | FK → Booking                              |
| `amount`         | Decimal |                                           |
| `payment_mode`   | String  | `"UPI"`, `"COD"`, etc.                    |
| `payment_status` | String  | `"pending"`, `"completed"`, `"failed"`    |
| `payment_date`   | DateTime |                                          |

---

## 🚀 How to Run the Backend

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure PostgreSQL is running and .env is configured

# 3. Start the server
python app.py
```

Server starts at: **`http://127.0.0.1:5000`**

---

## 📝 Quick Fetch Example (JavaScript)

### Register
```js
const res = await fetch("http://127.0.0.1:5000/api/auth/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Anas",
    email: "anas@example.com",
    password: "mypassword"
  })
});
const data = await res.json();
console.log(data); // { message: "User registered successfully" }
```

### Login
```js
const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "anas@example.com",
    password: "mypassword"
  })
});
const data = await res.json();
const token = data.access_token; // Save this!
```

### Authenticated Request
```js
const res = await fetch("http://127.0.0.1:5000/api/test/protected", {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${token}`
  }
});
const data = await res.json();
console.log(data); // { message: "Access granted", user_id: 1 }
```

---

## ⚙️ CORS

**CORS is enabled** for all origins (`flask-cors`), so you can freely make requests from your frontend running on any port (e.g., `localhost:3000`, `localhost:5173`, etc.) without any CORS errors.

---

## 📌 Notes for Frontend Dev

- All request bodies must be **JSON** — always set `Content-Type: application/json`.
- All dates should be in **`YYYY-MM-DD`** format.
- The `role` field returned on login (`"renter"` or `"owner"`) can be used to conditionally show UI elements.
- More routes (Cars, Bookings, Payments CRUD) are **coming soon** — check back as the backend evolves.
