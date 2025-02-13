# Car Dealership Web App

## Overview
This is a **Car Dealership Web App** built using **Django Rest Framework (DRF)** for the backend and **React** for the frontend. The application allows users to **buy, sell, compare, and review cars**. It also includes **user authentication, messaging, wishlist, and (FUTURE) AI-based car recommendations**.

## Features
✅ User Authentication (JWT-based Login & Registration)  
✅ Car Listings with Images (Front, Side, Back, Interior)  
✅ Wishlist & Car Comparisons  
✅ Messaging between Buyers & Dealers  
✅ Reviews & Ratings  
✅ AI-Based Car Recommendations (Based on Search History)  
✅ Transaction Handling for Car Purchases  

---

## Tech Stack
- **Backend**: Django, Django Rest Framework (DRF)
- **Frontend**: React (separate repository)
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- ** >> (FUTURE) AI/ML**: Search History-Based Car Recommendations, User search history.

---

## Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/car-dealership.git
cd car-dealership
```

### 2️⃣ Set Up Virtual Environment
```bash
pip install pipenv
pipenv shell
```

### 3️⃣ Install Dependencies
```bash
pipenv install
```

### 4️⃣ Configure `.env` File
Create a `.env` file in the root directory and add:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/car_db
ALLOWED_HOSTS=*
```

### 5️⃣ Run Migrations
```bash
python manage.py migrate
```

### 6️⃣ Create Superuser
```bash
python manage.py createsuperuser
```

### 7️⃣ Start the Server
```bash
python manage.py runserver
```

---

## API Endpoints

### Authentication
- `POST /scs/users/` → Register a new user
- `POST /scs/token/` → Get JWT token (Login)
- `POST /scs/token/refresh/` → Refresh JWT token

### Car Management
- `GET /scs/cars/` → List all cars
- `POST /scs/cars/` → Add a new car (Authenticated users only)
- `GET /scs/cars/{id}/` → Get details of a specific car
- `PUT /scs/cars/{id}/` → Update a car listing
- `DELETE /scs/cars/{id}/` → Delete a car listing

### Car Images
- `POST /scs/car-images/` → Upload images for a car

### Wishlist
- `GET /scs/wishlist/` → Get user’s wishlist
- `POST /scs/wishlist/` → Add a car to wishlist
- `DELETE /scs/wishlist/{id}/` → Remove a car from wishlist

### Car Comparison
- `POST /scs/compare/` → Compare two cars

### Reviews & Ratings
- `POST /scs/reviews/` → Add a review
- `GET /scs/reviews/{car_id}/` → Get reviews for a car

### Messaging
- `POST /scs/messages/` → Send a message to a dealer
- `GET /scs/messages/` → Get messages

### Transactions
- `POST /scs/transactions/` → Purchase a car
- `GET /scs/transactions/` → Get user transactions

---

## Running Tests
```bash
python manage.py test
```

---

## Deployment
- Deploy using **Docker, AWS, or Heroku**

**Example (Docker)**:
```bash
docker build -t car-dealership-app .
docker run -p 8000:8000 car-dealership-app
```

---
## 🏗️ Project Structure
```bash
📂 SCS-203/
├── 📂 Car/
│   ├── 📜 models.py       # Defines Car & SearchHistory models
│   ├── 📜 views.py        # API views
│   ├── 📜 urls.py         # API endpoints
│   ├── 📜 serializers.py  # DRF serializers
│   ├── 📜 recommendations.py  # Hybrid recommendation logic
│   ├── 📜 tasks.py        # Celery tasks for retraining
│   ├── 📜 apps.py         # App configurations
├── 📜 settings.py         # Django settings
├── 📜 manage.py           # Django entry point
├── 📜 README.md           # Project documentation
```
---
### Expected POST request
/scs/register/
{
    "first_name":"John",
    "last_name" :"hire",
    "username": "john_doe",
    "email": "john@hotwheel.com",
    "password": "securepassword123",
    "phone": "+123456789"
}
---
/scs/car-images/
'''
    {
        "id": 1,
        "car": 1,
        "image": "/media/car_images/GLA_s8Dfuda.jpg",
        "image_type": "front"
    },
    {
        "id": 2,
        "car": 1,
        "image": "/media/car_images/GLA_back_INbZDBY.jpeg",
        "image_type": "interior"
    },

/scs/cars/
[
    {
        "id": 1,
        "dealer": 1,
        "make": "Mercede-Benz",
        "model": "2024 model",
        "year": 2024,
        "price": "5420800.00",
        "mileage": 0,
        "condition": "new",
        "transmission": "automatic",
        "fuel_type": "petrol",
        "color": "Black",
        "description": "The GLA features a sleek and dynamic exterior, characterized by      its aerodynamic lines and modern aesthetics. Inside, the cabin offers a spacious and luxurious environment, equipped with high-quality materials and advanced technology. Standard amenities include power-adjustable front seats with memory, dual-zone climate control, and a panoramic sunroof. The rear seats are designed to provide ample head and legroom, ensuring comfort for all passengers.",
        "created_at": "2025-02-10T11:38:08.612115Z",
        "updated_at": "2025-02-10T11:40:09.797295Z"
    }
]


## Contributing
- Fork the repo
- Create a new branch (`git checkout -b feature-name`)
- Commit changes (`git commit -m 'Added new feature'`)
- Push branch (`git push origin feature-name`)
- Open a Pull Request

---

## License
This project is licensed under the MIT License.

