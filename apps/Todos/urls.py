from rest_framework_nested import routers
from .views import TodoViewSet, SubTodoViewSet

router = routers.DefaultRouter()
router.register(r"todos", TodoViewSet, basename="todo")

todos_router = routers.NestedDefaultRouter(router, r"todos", lookup="todo")
todos_router.register(r"sub-todos", SubTodoViewSet, basename="todo-subtodos")

urlpatterns = router.urls + todos_router.urls