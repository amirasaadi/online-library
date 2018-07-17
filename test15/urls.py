from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from book import views as book_view

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('',book_view.HomePageView.as_view(),name='home'),

    path('admin/', admin.site.urls),

    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),

    path('book/',include('book.urls',namespace='book')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)