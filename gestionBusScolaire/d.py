
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
        
from django.urls import path,include
from rest_framework import routers

router = routers.DefaultRouter()

from transport_scolaire.view_sets import (
     ChauffeurViewSet,
     TypeVehiculeViewSet,
)

router.register('transport_scolaire/chauffeurs', ChauffeurViewSet,basename='transport_scolaire.chauffeurs')
router.register('transport_scolaire/typevehicules', TypeVehiculeViewSet,basename='transport_scolaire.typevehicules')

from app_master.views import HomeViewPage


urlpatterns = [
     path('admin/', admin.site.urls),
     path('api/', include(router.urls)),     path('',HomeViewPage.as_view(),name='dashboard'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns +=[path('<path:dummy>', RedirectView.as_view(url='/')),]