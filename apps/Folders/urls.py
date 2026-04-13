from rest_framework.routers import DefaultRouter
from .views import FolderViewSet

### 
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import FolderViewSet, FolderTodoViewSet

router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folders')

folder_router = NestedDefaultRouter(router, r'folders', lookup='folder')
folder_router.register(r'todos', FolderTodoViewSet, basename='folder-todos')

urlpatterns = router.urls + folder_router.urls