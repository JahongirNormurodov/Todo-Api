from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_nested import routers

from apps.accounts.views import RegisterView, LoginView, LogoutView, MeView
from apps.folders.views import FolderViewSet, FolderTodoViewSet
from apps.categories.views import CategoryViewSet, CategoryTodoViewSet
from apps.tags.views import TagViewSet
from apps.labels.views import LabelViewSet
from apps.todos.views import TodoViewSet, SubTodoViewSet

# ── Main router ───────────────────────────────────────────────────────────────
router = routers.DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'labels', LabelViewSet, basename='label')
router.register(r'todos', TodoViewSet, basename='todo')

# ── Nested: /folders/{folder_pk}/todos/ ───────────────────────────────────────
folders_router = routers.NestedDefaultRouter(router, r'folders', lookup='folder')
folders_router.register(r'todos', FolderTodoViewSet, basename='folder-todos')

# ── Nested: /categories/{category_pk}/todos/ ─────────────────────────────────
categories_router = routers.NestedDefaultRouter(router, r'categories', lookup='category')
categories_router.register(r'todos', CategoryTodoViewSet, basename='category-todos')

# ── Nested: /todos/{todo_pk}/sub-todos/ ───────────────────────────────────────
todos_router = routers.NestedDefaultRouter(router, r'todos', lookup='todo')
todos_router.register(r'sub-todos', SubTodoViewSet, basename='todo-subtodos')

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),

    # Resources
    path('', include(router.urls)),
    path('', include(folders_router.urls)),
    path('', include(categories_router.urls)),
    path('', include(todos_router.urls)),
]
