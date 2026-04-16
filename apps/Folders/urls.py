from rest_framework_nested import routers
from .views import FolderViewSet, FolderTodoViewSet

router = routers.DefaultRouter()
router.register(r"folders", FolderViewSet, basename="folder")

folders_router = routers.NestedDefaultRouter(router, r"folders", lookup="folder")
folders_router.register(r"todos", FolderTodoViewSet, basename="folder-todos")

urlpatterns = router.urls + folders_router.urls

