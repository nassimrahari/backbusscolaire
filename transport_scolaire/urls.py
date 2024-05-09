from django.urls import path

from .views_generic import (
      ChauffeurListView, ChauffeurDetailView, ChauffeurCreateView, ChauffeurUpdateView, ChauffeurDeleteView,
      TypeVehiculeListView, TypeVehiculeDetailView, TypeVehiculeCreateView, TypeVehiculeUpdateView, TypeVehiculeDeleteView,
      BusListView, BusDetailView, BusCreateView, BusUpdateView, BusDeleteView,
      LieuLigneListView, LieuLigneDetailView, LieuLigneCreateView, LieuLigneUpdateView, LieuLigneDeleteView,
      LigneListView, LigneDetailView, LigneCreateView, LigneUpdateView, LigneDeleteView,
      LieuRamassageListView, LieuRamassageDetailView, LieuRamassageCreateView, LieuRamassageUpdateView, LieuRamassageDeleteView,
      OrdreLieuListView, OrdreLieuDetailView, OrdreLieuCreateView, OrdreLieuUpdateView, OrdreLieuDeleteView,
      EcoleListView, EcoleDetailView, EcoleCreateView, EcoleUpdateView, EcoleDeleteView,
      ClasseListView, ClasseDetailView, ClasseCreateView, ClasseUpdateView, ClasseDeleteView,
      ParentListView, ParentDetailView, ParentCreateView, ParentUpdateView, ParentDeleteView,
      EleveListView, EleveDetailView, EleveCreateView, EleveUpdateView, EleveDeleteView,
      ItineraireListView, ItineraireDetailView, ItineraireCreateView, ItineraireUpdateView, ItineraireDeleteView,
      HoraireListView, HoraireDetailView, HoraireCreateView, HoraireUpdateView, HoraireDeleteView,
      BusAssignationListView, BusAssignationDetailView, BusAssignationCreateView, BusAssignationUpdateView, BusAssignationDeleteView,
      AssignationItineraireListView, AssignationItineraireDetailView, AssignationItineraireCreateView, AssignationItineraireUpdateView, AssignationItineraireDeleteView,
)

app_name = 'transport_scolaire'

urlpatterns = [
      path('chauffeur',ChauffeurListView.as_view(), name='chauffeur-list'),
      path('chauffeur/<int:pk>/',ChauffeurDetailView.as_view(), name='chauffeur-detail'),
      path('chauffeur/create',ChauffeurCreateView.as_view(), name='chauffeur-create'),
      path('chauffeur/<int:pk>/update',ChauffeurUpdateView.as_view(), name='chauffeur-update'),
      path('chauffeur/<int:pk>/delete',ChauffeurDeleteView.as_view(), name='chauffeur-delete'),

      path('typevehicule',TypeVehiculeListView.as_view(), name='typevehicule-list'),
      path('typevehicule/<int:pk>/',TypeVehiculeDetailView.as_view(), name='typevehicule-detail'),
      path('typevehicule/create',TypeVehiculeCreateView.as_view(), name='typevehicule-create'),
      path('typevehicule/<int:pk>/update',TypeVehiculeUpdateView.as_view(), name='typevehicule-update'),
      path('typevehicule/<int:pk>/delete',TypeVehiculeDeleteView.as_view(), name='typevehicule-delete'),

      path('bus',BusListView.as_view(), name='bus-list'),
      path('bus/<int:pk>/',BusDetailView.as_view(), name='bus-detail'),
      path('bus/create',BusCreateView.as_view(), name='bus-create'),
      path('bus/<int:pk>/update',BusUpdateView.as_view(), name='bus-update'),
      path('bus/<int:pk>/delete',BusDeleteView.as_view(), name='bus-delete'),

      path('lieuligne',LieuLigneListView.as_view(), name='lieuligne-list'),
      path('lieuligne/<int:pk>/',LieuLigneDetailView.as_view(), name='lieuligne-detail'),
      path('lieuligne/create',LieuLigneCreateView.as_view(), name='lieuligne-create'),
      path('lieuligne/<int:pk>/update',LieuLigneUpdateView.as_view(), name='lieuligne-update'),
      path('lieuligne/<int:pk>/delete',LieuLigneDeleteView.as_view(), name='lieuligne-delete'),

      path('ligne',LigneListView.as_view(), name='ligne-list'),
      path('ligne/<int:pk>/',LigneDetailView.as_view(), name='ligne-detail'),
      path('ligne/create',LigneCreateView.as_view(), name='ligne-create'),
      path('ligne/<int:pk>/update',LigneUpdateView.as_view(), name='ligne-update'),
      path('ligne/<int:pk>/delete',LigneDeleteView.as_view(), name='ligne-delete'),

      path('lieuramassage',LieuRamassageListView.as_view(), name='lieuramassage-list'),
      path('lieuramassage/<int:pk>/',LieuRamassageDetailView.as_view(), name='lieuramassage-detail'),
      path('lieuramassage/create',LieuRamassageCreateView.as_view(), name='lieuramassage-create'),
      path('lieuramassage/<int:pk>/update',LieuRamassageUpdateView.as_view(), name='lieuramassage-update'),
      path('lieuramassage/<int:pk>/delete',LieuRamassageDeleteView.as_view(), name='lieuramassage-delete'),

      path('ordrelieu',OrdreLieuListView.as_view(), name='ordrelieu-list'),
      path('ordrelieu/<int:pk>/',OrdreLieuDetailView.as_view(), name='ordrelieu-detail'),
      path('ordrelieu/create',OrdreLieuCreateView.as_view(), name='ordrelieu-create'),
      path('ordrelieu/<int:pk>/update',OrdreLieuUpdateView.as_view(), name='ordrelieu-update'),
      path('ordrelieu/<int:pk>/delete',OrdreLieuDeleteView.as_view(), name='ordrelieu-delete'),

      path('ecole',EcoleListView.as_view(), name='ecole-list'),
      path('ecole/<int:pk>/',EcoleDetailView.as_view(), name='ecole-detail'),
      path('ecole/create',EcoleCreateView.as_view(), name='ecole-create'),
      path('ecole/<int:pk>/update',EcoleUpdateView.as_view(), name='ecole-update'),
      path('ecole/<int:pk>/delete',EcoleDeleteView.as_view(), name='ecole-delete'),

      path('classe',ClasseListView.as_view(), name='classe-list'),
      path('classe/<int:pk>/',ClasseDetailView.as_view(), name='classe-detail'),
      path('classe/create',ClasseCreateView.as_view(), name='classe-create'),
      path('classe/<int:pk>/update',ClasseUpdateView.as_view(), name='classe-update'),
      path('classe/<int:pk>/delete',ClasseDeleteView.as_view(), name='classe-delete'),

      path('parent',ParentListView.as_view(), name='parent-list'),
      path('parent/<int:pk>/',ParentDetailView.as_view(), name='parent-detail'),
      path('parent/create',ParentCreateView.as_view(), name='parent-create'),
      path('parent/<int:pk>/update',ParentUpdateView.as_view(), name='parent-update'),
      path('parent/<int:pk>/delete',ParentDeleteView.as_view(), name='parent-delete'),

      path('eleve',EleveListView.as_view(), name='eleve-list'),
      path('eleve/<int:pk>/',EleveDetailView.as_view(), name='eleve-detail'),
      path('eleve/create',EleveCreateView.as_view(), name='eleve-create'),
      path('eleve/<int:pk>/update',EleveUpdateView.as_view(), name='eleve-update'),
      path('eleve/<int:pk>/delete',EleveDeleteView.as_view(), name='eleve-delete'),

      path('itineraire',ItineraireListView.as_view(), name='itineraire-list'),
      path('itineraire/<int:pk>/',ItineraireDetailView.as_view(), name='itineraire-detail'),
      path('itineraire/create',ItineraireCreateView.as_view(), name='itineraire-create'),
      path('itineraire/<int:pk>/update',ItineraireUpdateView.as_view(), name='itineraire-update'),
      path('itineraire/<int:pk>/delete',ItineraireDeleteView.as_view(), name='itineraire-delete'),

      path('horaire',HoraireListView.as_view(), name='horaire-list'),
      path('horaire/<int:pk>/',HoraireDetailView.as_view(), name='horaire-detail'),
      path('horaire/create',HoraireCreateView.as_view(), name='horaire-create'),
      path('horaire/<int:pk>/update',HoraireUpdateView.as_view(), name='horaire-update'),
      path('horaire/<int:pk>/delete',HoraireDeleteView.as_view(), name='horaire-delete'),

      path('busassignation',BusAssignationListView.as_view(), name='busassignation-list'),
      path('busassignation/<int:pk>/',BusAssignationDetailView.as_view(), name='busassignation-detail'),
      path('busassignation/create',BusAssignationCreateView.as_view(), name='busassignation-create'),
      path('busassignation/<int:pk>/update',BusAssignationUpdateView.as_view(), name='busassignation-update'),
      path('busassignation/<int:pk>/delete',BusAssignationDeleteView.as_view(), name='busassignation-delete'),

      path('assignationitineraire',AssignationItineraireListView.as_view(), name='assignationitineraire-list'),
      path('assignationitineraire/<int:pk>/',AssignationItineraireDetailView.as_view(), name='assignationitineraire-detail'),
      path('assignationitineraire/create',AssignationItineraireCreateView.as_view(), name='assignationitineraire-create'),
      path('assignationitineraire/<int:pk>/update',AssignationItineraireUpdateView.as_view(), name='assignationitineraire-update'),
      path('assignationitineraire/<int:pk>/delete',AssignationItineraireDeleteView.as_view(), name='assignationitineraire-delete'),

]