# 🚗 Car Rental App — Backend API Documentation

> **For Frontend Developers** — Everything you need to connect your frontend to this Flask backend.

---

## 🌐 Base URL

```
http://127.0.0.1:5000
```

> Flask runs on port **5000**. All API routes are prefixed with `/api`.

---

## 🔐 Authentication

This API uses **JWT (JSON Web Tokens)**.

- After login, you receive an `access_token`.
- For **protected routes**, include it in every request header:

```
Authorization: Bearer <your_access_token>
```

> ⚠️ Always send the token for any route marked with 🔒.

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
  "password": "yourpassword",
  "role": "renter"
}
```

> `role` must be `"renter"` or `"owner"`. Defaults to `"renter"` if omitted.

**Success — `201 Created`:**
```json
{ "message": "User registered successfully" }
```

**Error — `400 Bad Request`:**
```json
{ "message": "Email already exists" }
```
```json
{ "message": "Invalid role" }
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

**Success — `200 OK`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "user_id": 1,
  "role": "renter"
}
```

> 🔑 Save the `access_token` and `user_id` — you'll need them for all protected requests.

**Error — `401 Unauthorized`:**
```json
{ "message": "Invalid credentials" }
```

---

### 🚘 Cars Routes — `/api/cars`

---

#### `GET /api/cars/` — Get All Cars

Returns a list of all available cars. No auth required.

**Success — `200 OK`:**
```json
[
  {
    "id": 1,
    "brand": "Toyota",
    "model": "Corolla",
    "price_per_day": 1500.00,
    "owner_id": 2,
    "is_available": true,
    "city": "Delhi"
  }
]
```

---

#### `GET /api/cars/<car_id>` — Get Single Car

**Success — `200 OK`:**
```json
{
  "id": 1,
  "brand": "Toyota",
  "model": "Corolla",
  "price_per_day": 1500.00,
  "owner_id": 2,
  "is_available": true,
  "city": "Delhi"
}
```

**Error — `404 Not Found`:**
```json
{ "message": "car not found" }
```

---

#### 🔒 `POST /api/cars/` — Add a Car

*Requires JWT. Only users with `role: "owner"` can add cars.*

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (JSON):**
```json
{
  "brand": "Toyota",
  "model": "Corolla",
  "price_per_day": 1500.00,
  "city": "Delhi"
}
```

**Success — `201 Created`:**
```json
{ "message": "car added successufully" }
```

**Error — `403 Forbidden`:**
```json
{ "message": "only owners can add cars" }
```

**Error — `400 Bad Request`:**
```json
{
  "error": "Missing required fields",
  "missing": ["city"]
}
```

---

#### 🔒 `PUT /api/cars/<car_id>` — Update a Car

*Requires JWT. Only the car's owner can update it.*

**Request Body (JSON) — all fields optional:**
```json
{
  "brand": "Honda",
  "model": "Civic",
  "price_per_day": 1800.00,
  "city": "Mumbai",
  "is_available": false
}
```

**Success — `200 OK`:**
```json
{ "message": "car updated successfullu" }
```

**Error — `403 Forbidden`:**
```json
{ "message": "Not Authorized" }
```

---

#### 🔒 `DELETE /api/cars/<car_id>` — Delete a Car

*Requires JWT. Only the car's owner can delete it.*

**Success — `200 OK`:**
```json
{ "message": "car deleted successfully" }
```

**Error — `403 Forbidden`:**
```json
{ "message": "Not authorized" }
```

---

### 🛡️ Test Route — `/api/test`

> For testing JWT auth only.

#### `GET /api/test/protected` 🔒

**Success — `200 OK`:**
```json
{ "message": "Access granted", "user_id": 1 }
```

---

## 🗂️ Data Models

### 👤 User
| Field           | Type     | Notes                              |
|-----------------|----------|------------------------------------|
| `user_id`       | Integer  | Primary key (auto)                 |
| `name`          | String   |                                    |
| `email`         | String   | Unique                             |
| `password_hash` | String   | Stored hashed, never returned      |
| `role`          | String   | `"renter"` (default) or `"owner"` |
| `created_at`    | DateTime |                                    |

### 🚘 Car
| Field           | Type     | Notes                     |
|-----------------|----------|---------------------------|
| `car_id`        | Integer  | Primary key (auto)        |
| `owner_id`      | Integer  | FK → User                 |
| `brand`         | String   | e.g. Toyota               |
| `model`         | String   | e.g. Corolla              |
| `city`          | String   |                           |
| `price_per_day` | Decimal  | e.g. 1500.00              |
| `is_available`  | Boolean  | `true` by default         |
| `created_at`    | DateTime |                           |

### 📋 Booking
| Field          | Type     | Notes                                     |
|----------------|----------|-------------------------------------------|
| `booking_id`   | Integer  | Primary key (auto)                        |
| `car_id`       | Integer  | FK → Car                                  |
| `owner_id`     | Integer  | FK → User (car owner)                     |
| `customer_id`  | Integer  | FK → User (person renting)                |
| `start_date`   | Date     | Format: `YYYY-MM-DD`                      |
| `end_date`     | Date     | Format: `YYYY-MM-DD`                      |
| `total_amount` | Decimal  | Calculated total                          |
| `status`       | String   | `"pending"`, `"confirmed"`, `"cancelled"` |
| `created_at`   | DateTime |                                           |

### 💳 Payment
| Field            | Type     | Notes                                     |
|------------------|----------|-------------------------------------------|
| `payment_id`     | Integer  | Primary key (auto)                        |
| `booking_id`     | Integer  | FK → Booking                              |
| `amount`         | Decimal  |                                           |
| `payment_mode`   | String   | `"UPI"`, `"COD"`, etc.                    |
| `payment_status` | String   | `"pending"`, `"completed"`, `"failed"`    |
| `payment_date`   | DateTime |                                           |

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

## 📝 Quick Fetch Examples (JavaScript)

### Register as Owner
```js
const res = await fetch("http://127.0.0.1:5000/api/auth/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Anas",
    email: "anas@example.com",
    password: "mypassword",
    role: "owner"
  })
});
const data = await res.json();
// { message: "User registered successfully" }
```

### Login
```js
const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email: "anas@example.com", password: "mypassword" })
});
const { access_token, user_id, role } = await res.json();
// Save access_token!
```

### Get All Cars
```js
const res = await fetch("http://127.0.0.1:5000/api/cars/");
const cars = await res.json();
```

### Add a Car (Owner only)
```js
const res = await fetch("http://127.0.0.1:5000/api/cars/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${access_token}`
  },
  body: JSON.stringify({
    brand: "Toyota",
    model: "Corolla",
    price_per_day: 1500,
    city: "Delhi"
  })
});
```

---

## ⚙️ CORS

**CORS is enabled** for all origins, so requests from `localhost:3000`, `localhost:5173`, etc. will work without any issues.

---

## 📌 Notes for Frontend Dev

- All request bodies must be **JSON** — always set `Content-Type: application/json`.
- All dates should be in **`YYYY-MM-DD`** format.
- Use the `role` from the login response to conditionally show UI (e.g., show "Add Car" only for `"owner"`).
- Booking and Payment **CRUD routes are coming soon** — check back as the backend evolves.
