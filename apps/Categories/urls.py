from rest_framework_nested import routers
from .views import CategoryViewSet, CategoryTodoViewSet

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")

categories_router = routers.NestedDefaultRouter(router, r"categories", lookup="category")
categories_router.register(r"todos", CategoryTodoViewSet, basename="category-todos")

urlpatterns = router.urls + categories_router.urls