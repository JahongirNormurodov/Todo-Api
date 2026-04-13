
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from .models import Folder
from .serializers import FolderSerializer

### folder todo
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.Todos.models import Todo
from apps.Todos.serializers import TodoSerializer



class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all().annotate(
        todo_count=Count('todos')
    )
    serializer_class = FolderSerializer


### folder todo 
class FolderTodoViewSet(ReadOnlyModelViewSet):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(
            folder_id=self.kwargs['folder_pk']
        ).select_related('folder')