# Blog API

A RESTful API for a blogging platform built with Django REST Framework. This API provides a complete backend solution for managing blog posts, user authentication, comments, and more.

## Features
- User authentication with JWT tokens
- CRUD operations for blog posts
- Category and tag management
- Comments system with nested replies
- Post likes and user interactions
- User profiles with customizable fields
- Advanced filtering and search capabilities
- Comprehensive API documentation
- Rate limiting for API endpoints
- Automated test suite
- Demo data generation

## Technologies Used
- Python 3.12
- Django 5.1
- Django REST Framework
- SimpleJWT for authentication
- drf-yasg for Swagger/OpenAPI documentation
- SQLite (default database)

## Installation

1. Clone the repository:
```bash
git clone <(https://github.com/MikiMesfin/Blogging-Platform)>
cd blog_api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py makemigrations users
python manage.py makemigrations blog
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. (Optional) Generate demo data:
```bash
python manage.py generate_demo_data
```

7. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List users
- `POST /api/users/` - Register new user
- `GET /api/users/{id}/` - Retrieve user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Posts
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `GET /api/posts/{slug}/` - Retrieve post
- `PUT /api/posts/{slug}/` - Update post
- `DELETE /api/posts/{slug}/` - Delete post
- `POST /api/posts/{slug}/like/` - Like/unlike post

### Categories & Tags
- `GET /api/categories/` - List categories
- `GET /api/tags/` - List tags

### Comments
- `GET /api/posts/{post_pk}/comments/` - List comments
- `POST /api/posts/{post_pk}/comments/` - Create comment

## Documentation
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Admin Interface: http://localhost:8000/admin/

## Testing
Run the test suite:
```bash
python manage.py test
```

## Demo Users
After running generate_demo_data, you can use:
- Username: (check database)
- Password: demo1234

Or use the superuser credentials created in step 5.

## Rate Limiting
- API endpoints are rate-limited to prevent abuse
- Anonymous users: 100 requests per hour
- Authenticated users: 1000 requests per hour

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details
