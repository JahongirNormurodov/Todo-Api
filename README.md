# Todo API

Full-featured REST API — Django + DRF + PostgreSQL + JWT + Docker + Swagger.

## Tezkor ishga tushirish

```bash
git clone <repo>
cd todo-api
cp .env.example .env
docker-compose up --build
```

API tayyor: http://localhost:8000/api/v1/
Swagger docs: http://localhost:8000/api/docs/

---

## Stack

| Texnologiya | Versiya | Maqsad |
|---|---|---|
| Python | 3.12 | Backend tili |
| Django | 5.0 | Web framework |
| DRF | 3.15 | REST API |
| SimpleJWT | 5.3 | JWT auth |
| django-filter | 24.2 | FilterSet |
| drf-nested-routers | 0.94 | Nested URL |
| drf-spectacular | 0.27 | Swagger/OpenAPI |
| PostgreSQL | 16 | Database |
| Docker | — | Konteyner |

---

## Loyiha tuzilmasi

```
todo-api/
├── config/
│   ├── settings.py        # Django sozlamalari
│   ├── urls.py            # Root URL
│   ├── api_router.py      # Barcha API routerlar
│   └── wsgi.py
├── apps/
│   ├── models.py          # Abstract TimeStampedModel (UUID + timestamps)
│   ├── accounts/          # Custom User, JWT auth
│   ├── folders/           # Folder CRUD + nested todos
│   ├── categories/        # Category CRUD + nested todos
│   ├── tags/              # Tag CRUD
│   ├── labels/            # Label CRUD
│   └── todos/             # Todo + SubTodo CRUD + filters
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── .env.example
└── .gitignore
```

---

## Auth Endpointlari

### Ro'yxatdan o'tish
```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "StrongPass123!",
  "password2": "StrongPass123!"
}
```

Javob:
```json
{
  "user": { "id": "uuid", "username": "john", "email": "john@example.com" },
  "access": "<JWT access token>",
  "refresh": "<JWT refresh token>"
}
```

### Login
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "StrongPass123!"
}
```

### Token yangilash
```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{ "refresh": "<refresh token>" }
```

### Logout
```http
POST /api/v1/auth/logout/
Authorization: Bearer <access token>

{ "refresh": "<refresh token>" }
```

### Profil ko'rish / yangilash
```http
GET  /api/v1/auth/me/
PATCH /api/v1/auth/me/
Authorization: Bearer <access token>
```

---

## Barcha Endpointlar

### Folders
```
GET    /api/v1/folders/              Barcha papkalar (unpaginated)
POST   /api/v1/folders/              Papka yaratish
GET    /api/v1/folders/{id}/         Papka detail
PUT    /api/v1/folders/{id}/         To'liq yangilash
PATCH  /api/v1/folders/{id}/         Qisman yangilash
DELETE /api/v1/folders/{id}/         O'chirish (cascade todos)
GET    /api/v1/folders/{id}/todos/   Papka ichidagi todolar
GET    /api/v1/folders/{id}/todos/{tid}/
```

### Categories
```
GET    /api/v1/categories/
POST   /api/v1/categories/
GET    /api/v1/categories/{id}/
PUT    /api/v1/categories/{id}/
PATCH  /api/v1/categories/{id}/
DELETE /api/v1/categories/{id}/
GET    /api/v1/categories/{id}/todos/
GET    /api/v1/categories/{id}/todos/{tid}/
```

### Tags
```
GET    /api/v1/tags/
POST   /api/v1/tags/
GET    /api/v1/tags/{id}/
PUT    /api/v1/tags/{id}/
PATCH  /api/v1/tags/{id}/
DELETE /api/v1/tags/{id}/
```

### Labels
```
GET    /api/v1/labels/
POST   /api/v1/labels/
GET    /api/v1/labels/{id}/
PUT    /api/v1/labels/{id}/
PATCH  /api/v1/labels/{id}/
DELETE /api/v1/labels/{id}/
```

### Todos
```
GET    /api/v1/todos/
POST   /api/v1/todos/
GET    /api/v1/todos/{id}/
PUT    /api/v1/todos/{id}/
PATCH  /api/v1/todos/{id}/
DELETE /api/v1/todos/{id}/
```

### Sub-Todos
```
GET    /api/v1/todos/{todo_id}/sub-todos/
POST   /api/v1/todos/{todo_id}/sub-todos/
GET    /api/v1/todos/{todo_id}/sub-todos/{id}/
PUT    /api/v1/todos/{todo_id}/sub-todos/{id}/
PATCH  /api/v1/todos/{todo_id}/sub-todos/{id}/
DELETE /api/v1/todos/{todo_id}/sub-todos/{id}/
```

**Jami: 40 ta endpoint**

---

## Todo Filter Parametrlari

```
GET /api/v1/todos/?status=pending
GET /api/v1/todos/?priority=high
GET /api/v1/todos/?category=<uuid>
GET /api/v1/todos/?folder=<uuid>
GET /api/v1/todos/?tags=id1,id2           # AND filter
GET /api/v1/todos/?labels=id1,id2         # AND filter
GET /api/v1/todos/?due_date_before=2026-05-01
GET /api/v1/todos/?due_date_after=2026-04-01
GET /api/v1/todos/?is_overdue=true
GET /api/v1/todos/?search=api             # title + description
GET /api/v1/todos/?ordering=-due_date     # - = descending
GET /api/v1/todos/?ordering=priority,position
GET /api/v1/todos/?page=2&page_size=20
```

---

## So'rov misollari

### Folder yaratish
```http
POST /api/v1/folders/
Authorization: Bearer <token>

{
  "name": "Ish",
  "color": "#6366F1",
  "icon": "briefcase",
  "position": 0
}
```

### Todo yaratish (tag va label bilan)
```http
POST /api/v1/todos/
Authorization: Bearer <token>

{
  "folder": "folder-uuid",
  "category": "category-uuid",
  "title": "API yozish",
  "description": "DRF bilan full CRUD",
  "priority": "high",
  "due_date": "2026-05-15T18:00:00Z",
  "tag_ids": ["tag-uuid-1", "tag-uuid-2"],
  "label_ids": ["label-uuid-1"]
}
```

### Todo statusini o'zgartirish
```http
PATCH /api/v1/todos/{id}/
Authorization: Bearer <token>

{ "status": "in_progress" }
```

### Sub-todo bajarildi deb belgilash
```http
PATCH /api/v1/todos/{todo_id}/sub-todos/{id}/
Authorization: Bearer <token>

{ "is_completed": true }
```

---

## Local ishga tushirish (Docker'siz)

```bash
# 1. Virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Paketlar
pip install -r requirements.txt

# 3. .env sozlash
cp .env.example .env
# DB_HOST=localhost ga o'zgartir

# 4. PostgreSQL yaratish (local)
createdb todo_db

# 5. Migrations
python manage.py migrate

# 6. Superuser
python manage.py createsuperuser

# 7. Ishga tushirish
python manage.py runserver
```

---

## Production uchun muhim o'zgarishlar

`.env` faylida:
```
DEBUG=False
SECRET_KEY=<tasodifiy 50+ belgili key>
ALLOWED_HOSTS=yourdomain.com
```

`docker-compose.yml`da `web` servisining `command` qatorini o'zgartir:
```yaml
command: >
  sh -c "python manage.py migrate &&
         python manage.py collectstatic --noinput &&
         gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4"
```

`requirements.txt`ga qo'sh:
```
gunicorn==21.2.0
```
