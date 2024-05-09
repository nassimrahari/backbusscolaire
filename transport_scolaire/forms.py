from django import forms
from django.utils import timezone
from .models import ( Chauffeur , TypeVehicule , Bus , LieuLigne , Ligne , LieuRamassage , OrdreLieu , Ecole , Classe , Parent , Eleve , Itineraire , Horaire , BusAssignation , AssignationItineraire ,)

class ChauffeurCreateForm(forms.ModelForm):
     class Meta:
          model = Chauffeur
          fields = ['nom','prenoms','tel','email',]

class ChauffeurUpdateForm(forms.ModelForm):
     class Meta:
          model = Chauffeur
          fields = ['nom','prenoms','tel','email',]


class TypeVehiculeCreateForm(forms.ModelForm):
     class Meta:
          model = TypeVehicule
          fields = ['nom',]

class TypeVehiculeUpdateForm(forms.ModelForm):
     class Meta:
          model = TypeVehicule
          fields = ['nom',]


class BusCreateForm(forms.ModelForm):
     class Meta:
          model = Bus
          fields = ['immatriculation','type','chauffeur','couleur','nbr_place',]

class BusUpdateForm(forms.ModelForm):
     class Meta:
          model = Bus
          fields = ['immatriculation','type','chauffeur','couleur','nbr_place',]


class LieuLigneCreateForm(forms.ModelForm):
     class Meta:
          model = LieuLigne
          fields = ['nom_lieu','latitude','longitude',]

class LieuLigneUpdateForm(forms.ModelForm):
     class Meta:
          model = LieuLigne
          fields = ['nom_lieu','latitude','longitude',]


class LigneCreateForm(forms.ModelForm):
     class Meta:
          model = Ligne
          fields = ['nom',]

class LigneUpdateForm(forms.ModelForm):
     class Meta:
          model = Ligne
          fields = ['nom',]


class LieuRamassageCreateForm(forms.ModelForm):
     class Meta:
          model = LieuRamassage
          fields = ['nom_lieu','latitude','longitude','ligne','lieu_ligne',]

class LieuRamassageUpdateForm(forms.ModelForm):
     class Meta:
          model = LieuRamassage
          fields = ['nom_lieu','latitude','longitude','ligne','lieu_ligne',]


class OrdreLieuCreateForm(forms.ModelForm):
     class Meta:
          model = OrdreLieu
          fields = ['ligne','lieu_ligne','num_ordre',]

class OrdreLieuUpdateForm(forms.ModelForm):
     class Meta:
          model = OrdreLieu
          fields = ['ligne','lieu_ligne','num_ordre',]


class EcoleCreateForm(forms.ModelForm):
     class Meta:
          model = Ecole
          fields = ['nom',]

class EcoleUpdateForm(forms.ModelForm):
     class Meta:
          model = Ecole
          fields = ['nom',]


class ClasseCreateForm(forms.ModelForm):
     class Meta:
          model = Classe
          fields = ['nom','ecole',]

class ClasseUpdateForm(forms.ModelForm):
     class Meta:
          model = Classe
          fields = ['nom','ecole',]


class ParentCreateForm(forms.ModelForm):
     class Meta:
          model = Parent
          fields = ['nom_mere','nom_pere','tel_mere','tel_pere','email','adresse',]

class ParentUpdateForm(forms.ModelForm):
     class Meta:
          model = Parent
          fields = ['nom_mere','nom_pere','tel_mere','tel_pere','email','adresse',]


class EleveCreateForm(forms.ModelForm):
     date_inscription = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'}))
     date_naissance = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'}))
     class Meta:
          model = Eleve
          fields = ['date_inscription','date_naissance','image','nom','prenoms','adresse','ligne','parent','ecole','classe','lieu_ramassage','montant_frais','etat',]

class EleveUpdateForm(forms.ModelForm):
     date_inscription = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'))
     date_naissance = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'))
     class Meta:
          model = Eleve
          fields = ['date_inscription','date_naissance','image','nom','prenoms','adresse','ligne','parent','ecole','classe','lieu_ramassage','montant_frais','etat',]


class ItineraireCreateForm(forms.ModelForm):
     date_itineraire = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'}))
     class Meta:
          model = Itineraire
          fields = ['date_itineraire','ligne','ligne_inverse',]

class ItineraireUpdateForm(forms.ModelForm):
     date_itineraire = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'))
     class Meta:
          model = Itineraire
          fields = ['date_itineraire','ligne','ligne_inverse',]


class HoraireCreateForm(forms.ModelForm):
     heureDebut = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
     heureFin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
     class Meta:
          model = Horaire
          fields = ['pointArret','itineraire','heureDebut','heureFin',]

class HoraireUpdateForm(forms.ModelForm):
     heureDebut = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
     heureFin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
     class Meta:
          model = Horaire
          fields = ['pointArret','itineraire','heureDebut','heureFin',]


class BusAssignationCreateForm(forms.ModelForm):
     date_assignation = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'}))
     class Meta:
          model = BusAssignation
          fields = ['date_assignation','bus','itineraire',]

class BusAssignationUpdateForm(forms.ModelForm):
     date_assignation = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'))
     class Meta:
          model = BusAssignation
          fields = ['date_assignation','bus','itineraire',]


class AssignationItineraireCreateForm(forms.ModelForm):
     dateAssigntion = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'}))
     class Meta:
          model = AssignationItineraire
          fields = ['dateAssigntion','eleve','itineraire',]

class AssignationItineraireUpdateForm(forms.ModelForm):
     dateAssigntion = forms.DateField(initial=str(timezone.now().date()).replace("/","-"),widget=forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'))
     class Meta:
          model = AssignationItineraire
          fields = ['dateAssigntion','eleve','itineraire',]



