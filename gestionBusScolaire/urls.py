
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
        
from django.urls import path,include
from rest_framework import routers
router = routers.DefaultRouter()

from transport_scolaire.view_sets import (
     ChauffeurViewSet,
     EcoleAssignationViewSet,
     TypeVehiculeViewSet,
     BusViewSet,
     LieuLigneViewSet,
     LigneViewSet,
     LieuRamassageViewSet,
     OrdreLieuViewSet,
     EcoleViewSet,
     ClasseViewSet,
     ParentViewSet,
     EleveViewSet,
     ItineraireViewSet,
     HoraireViewSet,
     BusAssignationViewSet,
     AssignationItineraireViewSet,
)

router.register('transport_scolaire/chauffeurs', ChauffeurViewSet,basename='transport_scolaire.chauffeurs')
router.register('transport_scolaire/typevehicules', TypeVehiculeViewSet,basename='transport_scolaire.typevehicules')
router.register('transport_scolaire/buss', BusViewSet,basename='transport_scolaire.buss')
router.register('transport_scolaire/lieulignes', LieuLigneViewSet,basename='transport_scolaire.lieulignes')
router.register('transport_scolaire/lignes', LigneViewSet,basename='transport_scolaire.lignes')
router.register('transport_scolaire/lieuramassages', LieuRamassageViewSet,basename='transport_scolaire.lieuramassages')
router.register('transport_scolaire/ordrelieus', OrdreLieuViewSet,basename='transport_scolaire.ordrelieus')
router.register('transport_scolaire/ecoles', EcoleViewSet,basename='transport_scolaire.ecoles')
router.register('transport_scolaire/classes', ClasseViewSet,basename='transport_scolaire.classes')
router.register('transport_scolaire/parents', ParentViewSet,basename='transport_scolaire.parents')
router.register('transport_scolaire/eleves', EleveViewSet,basename='transport_scolaire.eleves')
router.register('transport_scolaire/itineraires', ItineraireViewSet,basename='transport_scolaire.itineraires')
router.register('transport_scolaire/horaires', HoraireViewSet,basename='transport_scolaire.horaires')
router.register('transport_scolaire/busassignations', BusAssignationViewSet,basename='transport_scolaire.busassignations')
router.register('transport_scolaire/ecoleassignations', EcoleAssignationViewSet,basename='transport_scolaire.ecoleassignations')
router.register('transport_scolaire/assignationitineraires', AssignationItineraireViewSet,basename='transport_scolaire.assignationitineraires')

from app_master.views import HomeViewPage

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views_set import TokenCheckView
from django.views.generic.base import RedirectView
from django.contrib.auth import get_user_model

from transport_scolaire.view_sets import CountViewSet,AssignationBusItineraireViewSet

User=get_user_model()
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Effectuez des modifications sur la réponse si nécessaire
        user = User.objects.get(username=request.data.get('username'))
        role = user.role if not user.is_superuser else "admin"

        # Ajoutez les informations de l'utilisateur à la réponse
        response.data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role
        }

        return response

urlpatterns = [
     path('admin/', admin.site.urls),
     path('api/', include(router.urls)),     path('',HomeViewPage.as_view(),name='dashboard'),
     path('transport_scolaire/', include('transport_scolaire.urls')),
     path('api/ts/assignation_itineraire_bus', AssignationBusItineraireViewSet.as_view(),name='transport_scolaire:assignation_itineraire_bus'),

     path('api-auth/', include('rest_framework.urls')),
     path('api/token/', CustomTokenObtainPairView.as_view(), name='obtain_tokens'),
     path('api/token/check/', TokenCheckView.as_view(), name='check_tokens'),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
     path('api/counts/', CountViewSet.as_view(), name='count'),
    #   path('<path:dummy>', HomeViewPage.as_view()),  # Redirige tous les autres URL vers HomeViewPage.as_view()
    #  path('<path:dummy>', RedirectView.as_view(url='/')),  # Redirige tous les autres URL vers '/'
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns +=[path('<path:dummy>', RedirectView.as_view(url='/')),]