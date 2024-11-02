from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls')),
    path('tasks/', include('task.urls')),
    path('blog/', include('blog.urls'))
]