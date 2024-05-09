from typing import Any

from django.db.models import Q
from django.core.paginator import Paginator
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ( Chauffeur , TypeVehicule , Bus , LieuLigne , Ligne , LieuRamassage , OrdreLieu , Ecole , Classe , Parent , Eleve , Itineraire , Horaire , BusAssignation , AssignationItineraire ,)
from .forms import (ChauffeurCreateForm, ChauffeurUpdateForm ,TypeVehiculeCreateForm, TypeVehiculeUpdateForm ,BusCreateForm, BusUpdateForm ,LieuLigneCreateForm, LieuLigneUpdateForm ,LigneCreateForm, LigneUpdateForm ,LieuRamassageCreateForm, LieuRamassageUpdateForm ,OrdreLieuCreateForm, OrdreLieuUpdateForm ,EcoleCreateForm, EcoleUpdateForm ,ClasseCreateForm, ClasseUpdateForm ,ParentCreateForm, ParentUpdateForm ,EleveCreateForm, EleveUpdateForm ,ItineraireCreateForm, ItineraireUpdateForm ,HoraireCreateForm, HoraireUpdateForm ,BusAssignationCreateForm, BusAssignationUpdateForm ,AssignationItineraireCreateForm, AssignationItineraireUpdateForm ,)

class ChauffeurListView(ListView):
     model = Chauffeur
     template_name = 'chauffeur/list.html'
     context_object_name = 'chauffeurs'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Chauffeur.objects.all().order_by('-pk')
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom__icontains=search_query) | Q(prenoms__icontains=search_query) | Q(tel__icontains=search_query) | Q(email__icontains=search_query) )
          context['search_query']=search_query
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['chauffeurs']=page_obj
          return context

class ChauffeurDetailView(DetailView):
     model = Chauffeur
     template_name = 'chauffeur/detail.html'
     context_object_name = 'chauffeurs'

class ChauffeurCreateView(CreateView):
     model = Chauffeur
     template_name = 'chauffeur/create.html'
     form_class  = ChauffeurCreateForm
     success_url = reverse_lazy('transport_scolaire:chauffeur-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          chauffeur = form.save()
          return super().form_valid(form)

class ChauffeurUpdateView(UpdateView):
     model = Chauffeur
     template_name = 'chauffeur/update.html'
     form_class  = ChauffeurUpdateForm
     success_url = reverse_lazy('transport_scolaire:chauffeur-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          chauffeur = form.save()
          return super().form_valid(form)

class ChauffeurDeleteView(DeleteView):
     model = Chauffeur
     template_name = 'chauffeur/delete.html'
     success_url = reverse_lazy('transport_scolaire:chauffeur-list')
class TypeVehiculeListView(ListView):
     model = TypeVehicule
     template_name = 'typevehicule/list.html'
     context_object_name = 'typevehicules'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =TypeVehicule.objects.all().order_by('-pk')
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom__icontains=search_query) )
          context['search_query']=search_query
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['typevehicules']=page_obj
          return context

class TypeVehiculeDetailView(DetailView):
     model = TypeVehicule
     template_name = 'typevehicule/detail.html'
     context_object_name = 'typevehicules'

class TypeVehiculeCreateView(CreateView):
     model = TypeVehicule
     template_name = 'typevehicule/create.html'
     form_class  = TypeVehiculeCreateForm
     success_url = reverse_lazy('transport_scolaire:typevehicule-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          typevehicule = form.save()
          return super().form_valid(form)

class TypeVehiculeUpdateView(UpdateView):
     model = TypeVehicule
     template_name = 'typevehicule/update.html'
     form_class  = TypeVehiculeUpdateForm
     success_url = reverse_lazy('transport_scolaire:typevehicule-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          typevehicule = form.save()
          return super().form_valid(form)

class TypeVehiculeDeleteView(DeleteView):
     model = TypeVehicule
     template_name = 'typevehicule/delete.html'
     success_url = reverse_lazy('transport_scolaire:typevehicule-list')
class BusListView(ListView):
     model = Bus
     template_name = 'bus/list.html'
     context_object_name = 'buss'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Bus.objects.all().order_by('-pk')
          search_filter = self.request.GET.get('search_filter_type') or ''
          if search_filter:
               objects=objects.filter(Q(type__pk=search_filter))
               context['search_filter_type']=search_filter
          search_filter = self.request.GET.get('search_filter_chauffeur') or ''
          if search_filter:
               objects=objects.filter(Q(chauffeur__pk=search_filter))
               context['search_filter_chauffeur']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(immatriculation__icontains=search_query) | Q(couleur__icontains=search_query) | Q(nbr_place__icontains=search_query) )
          context['search_query']=search_query
          context['types']=TypeVehicule.objects.all()
          context['chauffeurs']=Chauffeur.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['buss']=page_obj
          return context

class BusDetailView(DetailView):
     model = Bus
     template_name = 'bus/detail.html'
     context_object_name = 'buss'

class BusCreateView(CreateView):
     model = Bus
     template_name = 'bus/create.html'
     form_class  = BusCreateForm
     success_url = reverse_lazy('transport_scolaire:bus-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          bus = form.save()
          return super().form_valid(form)

class BusUpdateView(UpdateView):
     model = Bus
     template_name = 'bus/update.html'
     form_class  = BusUpdateForm
     success_url = reverse_lazy('transport_scolaire:bus-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          bus = form.save()
          return super().form_valid(form)

class BusDeleteView(DeleteView):
     model = Bus
     template_name = 'bus/delete.html'
     success_url = reverse_lazy('transport_scolaire:bus-list')
class LieuLigneListView(ListView):
     model = LieuLigne
     template_name = 'lieuligne/list.html'
     context_object_name = 'lieulignes'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =LieuLigne.objects.all().order_by('-pk')
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom_lieu__icontains=search_query) | Q(latitude__icontains=search_query) | Q(longitude__icontains=search_query) )
          context['search_query']=search_query
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['lieulignes']=page_obj
          return context

class LieuLigneDetailView(DetailView):
     model = LieuLigne
     template_name = 'lieuligne/detail.html'
     context_object_name = 'lieulignes'

class LieuLigneCreateView(CreateView):
     model = LieuLigne
     template_name = 'lieuligne/create.html'
     form_class  = LieuLigneCreateForm
     success_url = reverse_lazy('transport_scolaire:lieuligne-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          lieuligne = form.save()
          return super().form_valid(form)

class LieuLigneUpdateView(UpdateView):
     model = LieuLigne
     template_name = 'lieuligne/update.html'
     form_class  = LieuLigneUpdateForm
     success_url = reverse_lazy('transport_scolaire:lieuligne-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          lieuligne = form.save()
          return super().form_valid(form)

class LieuLigneDeleteView(DeleteView):
     model = LieuLigne
     template_name = 'lieuligne/delete.html'
     success_url = reverse_lazy('transport_scolaire:lieuligne-list')
class LigneListView(ListView):
     model = Ligne
     template_name = 'ligne/list.html'
     context_object_name = 'lignes'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Ligne.objects.all().order_by('-pk')
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom__icontains=search_query) )
          context['search_query']=search_query
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['lignes']=page_obj
          return context

class LigneDetailView(DetailView):
     model = Ligne
     template_name = 'ligne/detail.html'
     context_object_name = 'lignes'

class LigneCreateView(CreateView):
     model = Ligne
     template_name = 'ligne/create.html'
     form_class  = LigneCreateForm
     success_url = reverse_lazy('transport_scolaire:ligne-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          ligne = form.save()
          lieu_lignes= self.request.POST.getlist('lieu_ligne[]')
          num_ordres= self.request.POST.getlist('num_ordre[]')
          for  lieu_ligne, num_ordre, in zip( lieu_lignes, num_ordres):
               try:
                    OrdreLieu.objects.create(
                         ligne=ligne,
                         lieu_ligne=LieuLigne.objects.get(pk=lieu_ligne),
                         num_ordre=num_ordre,
                    )
               except:
                    pass
          return super().form_valid(form)

class LigneUpdateView(UpdateView):
     model = Ligne
     template_name = 'ligne/update.html'
     form_class  = LigneUpdateForm
     success_url = reverse_lazy('transport_scolaire:ligne-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          ligne = form.save()
          lieu_lignes= self.request.POST.getlist('lieu_ligne[]')
          num_ordres= self.request.POST.getlist('num_ordre[]')
          ordrelieus= self.request.POST.getlist('ordrelieu[]')
          # Delete OrdreLieu objects that are not in the OrdreLieus list
          ordrelieus_digits = [int(value) for value in self.request.POST.getlist('ordrelieu[]') if value.isdigit()]
          OrdreLieu.objects.filter(ligne=ligne).exclude(pk__in=ordrelieus_digits).delete()
          for ordrelieu, lieu_ligne, num_ordre in zip( ordrelieus, lieu_lignes, num_ordres):
               if ordrelieu:
                    OrdreLieu.objects.filter(pk=ordrelieu).update(
                    ligne=ligne,
                    lieu_ligne=LieuLigne.objects.get(pk=lieu_ligne),
                    num_ordre=num_ordre,
               )
               else:
                    OrdreLieu.objects.create(
                    ligne=ligne,
               lieu_ligne=LieuLigne.objects.get(pk=lieu_ligne),
               num_ordre=num_ordre,
               )
          return super().form_valid(form)

class LigneDeleteView(DeleteView):
     model = Ligne
     template_name = 'ligne/delete.html'
     success_url = reverse_lazy('transport_scolaire:ligne-list')
class LieuRamassageListView(ListView):
     model = LieuRamassage
     template_name = 'lieuramassage/list.html'
     context_object_name = 'lieuramassages'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =LieuRamassage.objects.all().order_by('-pk')
          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               objects=objects.filter(Q(ligne__pk=search_filter))
               context['search_filter_ligne']=search_filter
          search_filter = self.request.GET.get('search_filter_lieu_ligne') or ''
          if search_filter:
               objects=objects.filter(Q(lieu_ligne__pk=search_filter))
               context['search_filter_lieu_ligne']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom_lieu__icontains=search_query) | Q(latitude__icontains=search_query) | Q(longitude__icontains=search_query) )
          context['search_query']=search_query
          context['lignes']=Ligne.objects.all()
          context['lieu_lignes']=LieuLigne.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['lieuramassages']=page_obj
          return context

class LieuRamassageDetailView(DetailView):
     model = LieuRamassage
     template_name = 'lieuramassage/detail.html'
     context_object_name = 'lieuramassages'

class LieuRamassageCreateView(CreateView):
     model = LieuRamassage
     template_name = 'lieuramassage/create.html'
     form_class  = LieuRamassageCreateForm
     success_url = reverse_lazy('transport_scolaire:lieuramassage-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          lieuramassage = form.save()
          return super().form_valid(form)

class LieuRamassageUpdateView(UpdateView):
     model = LieuRamassage
     template_name = 'lieuramassage/update.html'
     form_class  = LieuRamassageUpdateForm
     success_url = reverse_lazy('transport_scolaire:lieuramassage-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          lieuramassage = form.save()
          return super().form_valid(form)

class LieuRamassageDeleteView(DeleteView):
     model = LieuRamassage
     template_name = 'lieuramassage/delete.html'
     success_url = reverse_lazy('transport_scolaire:lieuramassage-list')
class OrdreLieuListView(ListView):
     model = OrdreLieu
     template_name = 'ordrelieu/list.html'
     context_object_name = 'ordrelieus'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =OrdreLieu.objects.all().order_by('-pk')
          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               objects=objects.filter(Q(ligne__pk=search_filter))
               context['search_filter_ligne']=search_filter
          search_filter = self.request.GET.get('search_filter_lieu_ligne') or ''
          if search_filter:
               objects=objects.filter(Q(lieu_ligne__pk=search_filter))
               context['search_filter_lieu_ligne']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(num_ordre__icontains=search_query) )
          context['search_query']=search_query
          context['lignes']=Ligne.objects.all()
          context['lieu_lignes']=LieuLigne.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['ordrelieus']=page_obj
          return context

class OrdreLieuDetailView(DetailView):
     model = OrdreLieu
     template_name = 'ordrelieu/detail.html'
     context_object_name = 'ordrelieus'

class OrdreLieuCreateView(CreateView):
     model = OrdreLieu
     template_name = 'ordrelieu/create.html'
     form_class  = OrdreLieuCreateForm
     success_url = reverse_lazy('transport_scolaire:ordrelieu-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          ordrelieu = form.save()
          return super().form_valid(form)

class OrdreLieuUpdateView(UpdateView):
     model = OrdreLieu
     template_name = 'ordrelieu/update.html'
     form_class  = OrdreLieuUpdateForm
     success_url = reverse_lazy('transport_scolaire:ordrelieu-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          ordrelieu = form.save()
          return super().form_valid(form)

class OrdreLieuDeleteView(DeleteView):
     model = OrdreLieu
     template_name = 'ordrelieu/delete.html'
     success_url = reverse_lazy('transport_scolaire:ordrelieu-list')
class EcoleListView(ListView):
     model = Ecole
     template_name = 'ecole/list.html'
     context_object_name = 'ecoles'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Ecole.objects.all().order_by('-pk')
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom__icontains=search_query) )
          context['search_query']=search_query
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['ecoles']=page_obj
          return context

class EcoleDetailView(DetailView):
     model = Ecole
     template_name = 'ecole/detail.html'
     context_object_name = 'ecoles'

class EcoleCreateView(CreateView):
     model = Ecole
     template_name = 'ecole/create.html'
     form_class  = EcoleCreateForm
     success_url = reverse_lazy('transport_scolaire:ecole-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          ecole = form.save()
          noms= self.request.POST.getlist('nom[]')
          for  nom, in zip( noms):
               try:
                    Classe.objects.create(
                         ecole=ecole,
                         nom=nom,
                    )
               except:
                    pass
          return super().form_valid(form)

class EcoleUpdateView(UpdateView):
     model = Ecole
     template_name = 'ecole/update.html'
     form_class  = EcoleUpdateForm
     success_url = reverse_lazy('transport_scolaire:ecole-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          ecole = form.save()
          noms= self.request.POST.getlist('nom[]')
          classes= self.request.POST.getlist('classe[]')
          # Delete Classe objects that are not in the Classes list
          classes_digits = [int(value) for value in self.request.POST.getlist('classe[]') if value.isdigit()]
          Classe.objects.filter(ecole=ecole).exclude(pk__in=classes_digits).delete()
          for classe, nom in zip( classes, noms):
               if classe:
                    Classe.objects.filter(pk=classe).update(
                    ecole=ecole,
                    nom=nom,
               )
               else:
                    Classe.objects.create(
                    ecole=ecole,
               nom=nom,
               )
          return super().form_valid(form)

class EcoleDeleteView(DeleteView):
     model = Ecole
     template_name = 'ecole/delete.html'
     success_url = reverse_lazy('transport_scolaire:ecole-list')
class ClasseListView(ListView):
     model = Classe
     template_name = 'classe/list.html'
     context_object_name = 'classes'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Classe.objects.all().order_by('-pk')
          search_filter = self.request.GET.get('search_filter_ecole') or ''
          if search_filter:
               objects=objects.filter(Q(ecole__pk=search_filter))
               context['search_filter_ecole']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom__icontains=search_query) )
          context['search_query']=search_query
          context['ecoles']=Ecole.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['classes']=page_obj
          return context

class ClasseDetailView(DetailView):
     model = Classe
     template_name = 'classe/detail.html'
     context_object_name = 'classes'

class ClasseCreateView(CreateView):
     model = Classe
     template_name = 'classe/create.html'
     form_class  = ClasseCreateForm
     success_url = reverse_lazy('transport_scolaire:classe-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          classe = form.save()
          return super().form_valid(form)

class ClasseUpdateView(UpdateView):
     model = Classe
     template_name = 'classe/update.html'
     form_class  = ClasseUpdateForm
     success_url = reverse_lazy('transport_scolaire:classe-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          classe = form.save()
          return super().form_valid(form)

class ClasseDeleteView(DeleteView):
     model = Classe
     template_name = 'classe/delete.html'
     success_url = reverse_lazy('transport_scolaire:classe-list')
class ParentListView(ListView):
     model = Parent
     template_name = 'parent/list.html'
     context_object_name = 'parents'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Parent.objects.all().order_by('-pk')
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(nom_mere__icontains=search_query) | Q(nom_pere__icontains=search_query) | Q(tel_mere__icontains=search_query) | Q(tel_pere__icontains=search_query) | Q(email__icontains=search_query) | Q(adresse__icontains=search_query) )
          context['search_query']=search_query
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['parents']=page_obj
          return context

class ParentDetailView(DetailView):
     model = Parent
     template_name = 'parent/detail.html'
     context_object_name = 'parents'

class ParentCreateView(CreateView):
     model = Parent
     template_name = 'parent/create.html'
     form_class  = ParentCreateForm
     success_url = reverse_lazy('transport_scolaire:parent-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          parent = form.save()
          return super().form_valid(form)

class ParentUpdateView(UpdateView):
     model = Parent
     template_name = 'parent/update.html'
     form_class  = ParentUpdateForm
     success_url = reverse_lazy('transport_scolaire:parent-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          parent = form.save()
          return super().form_valid(form)

class ParentDeleteView(DeleteView):
     model = Parent
     template_name = 'parent/delete.html'
     success_url = reverse_lazy('transport_scolaire:parent-list')
class EleveListView(ListView):
     model = Eleve
     template_name = 'eleve/list.html'
     context_object_name = 'eleves'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Eleve.objects.all().order_by('-pk')
          search_filter_gte = self.request.GET.get('search_filter_date_inscription_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_inscription_lte') or ''
          if search_filter_gte and search_filter_lte:
               objects=objects.filter(date_inscription__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               objects=objects.filter(date_inscription__lte=search_filter_lte)
          elif search_filter_gte:
               objects=objects.filter(date_inscription__gte=search_filter_gte)
          context['search_filter_date_inscription_gte']=search_filter_gte
          context['search_filter_date_inscription_lte']=search_filter_lte
          search_filter_gte = self.request.GET.get('search_filter_date_naissance_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_naissance_lte') or ''
          if search_filter_gte and search_filter_lte:
               objects=objects.filter(date_naissance__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               objects=objects.filter(date_naissance__lte=search_filter_lte)
          elif search_filter_gte:
               objects=objects.filter(date_naissance__gte=search_filter_gte)
          context['search_filter_date_naissance_gte']=search_filter_gte
          context['search_filter_date_naissance_lte']=search_filter_lte
          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               objects=objects.filter(Q(ligne__pk=search_filter))
               context['search_filter_ligne']=search_filter
          search_filter = self.request.GET.get('search_filter_parent') or ''
          if search_filter:
               objects=objects.filter(Q(parent__pk=search_filter))
               context['search_filter_parent']=search_filter
          search_filter = self.request.GET.get('search_filter_ecole') or ''
          if search_filter:
               objects=objects.filter(Q(ecole__pk=search_filter))
               context['search_filter_ecole']=search_filter
          search_filter = self.request.GET.get('search_filter_classe') or ''
          if search_filter:
               objects=objects.filter(Q(classe__pk=search_filter))
               context['search_filter_classe']=search_filter
          search_filter = self.request.GET.get('search_filter_lieu_ramassage') or ''
          if search_filter:
               objects=objects.filter(Q(lieu_ramassage__pk=search_filter))
               context['search_filter_lieu_ramassage']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(image__icontains=search_query) | Q(nom__icontains=search_query) | Q(prenoms__icontains=search_query) | Q(adresse__icontains=search_query) | Q(montant_frais__icontains=search_query) | Q(etat__icontains=search_query) )
          context['search_query']=search_query
          context['lignes']=Ligne.objects.all()
          context['parents']=Parent.objects.all()
          context['ecoles']=Ecole.objects.all()
          context['classes']=Classe.objects.all()
          context['lieu_ramassages']=LieuRamassage.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['eleves']=page_obj
          return context

class EleveDetailView(DetailView):
     model = Eleve
     template_name = 'eleve/detail.html'
     context_object_name = 'eleves'

class EleveCreateView(CreateView):
     model = Eleve
     template_name = 'eleve/create.html'
     form_class  = EleveCreateForm
     success_url = reverse_lazy('transport_scolaire:eleve-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          eleve = form.save()
          return super().form_valid(form)

class EleveUpdateView(UpdateView):
     model = Eleve
     template_name = 'eleve/update.html'
     form_class  = EleveUpdateForm
     success_url = reverse_lazy('transport_scolaire:eleve-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          eleve = form.save()
          return super().form_valid(form)

class EleveDeleteView(DeleteView):
     model = Eleve
     template_name = 'eleve/delete.html'
     success_url = reverse_lazy('transport_scolaire:eleve-list')
class ItineraireListView(ListView):
     model = Itineraire
     template_name = 'itineraire/list.html'
     context_object_name = 'itineraires'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Itineraire.objects.all().order_by('-pk')
          search_filter_gte = self.request.GET.get('search_filter_date_itineraire_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_itineraire_lte') or ''
          if search_filter_gte and search_filter_lte:
               objects=objects.filter(date_itineraire__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               objects=objects.filter(date_itineraire__lte=search_filter_lte)
          elif search_filter_gte:
               objects=objects.filter(date_itineraire__gte=search_filter_gte)
          context['search_filter_date_itineraire_gte']=search_filter_gte
          context['search_filter_date_itineraire_lte']=search_filter_lte
          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               objects=objects.filter(Q(ligne__pk=search_filter))
               context['search_filter_ligne']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(ligne_inverse__icontains=search_query) )
          context['search_query']=search_query
          context['lignes']=Ligne.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['itineraires']=page_obj
          return context

class ItineraireDetailView(DetailView):
     model = Itineraire
     template_name = 'itineraire/detail.html'
     context_object_name = 'itineraires'

class ItineraireCreateView(CreateView):
     model = Itineraire
     template_name = 'itineraire/create.html'
     form_class  = ItineraireCreateForm
     success_url = reverse_lazy('transport_scolaire:itineraire-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          itineraire = form.save()
          date_assignations= self.request.POST.getlist('date_assignation[]')
          buss= self.request.POST.getlist('bus[]')
          for  date_assignation, bus, in zip( date_assignations, buss):
               try:
                    BusAssignation.objects.create(
                         itineraire=itineraire,
                         date_assignation=date_assignation,
                         bus=Bus.objects.get(pk=bus),
                    )
               except:
                    pass
          pointArrets= self.request.POST.getlist('pointArret[]')
          heureDebuts= self.request.POST.getlist('heureDebut[]')
          heureFins= self.request.POST.getlist('heureFin[]')
          for  pointArret, heureDebut, heureFin, in zip( pointArrets, heureDebuts, heureFins):
               try:
                    Horaire.objects.create(
                         itineraire=itineraire,
                         pointArret=LieuLigne.objects.get(pk=pointArret),
                         heureDebut=heureDebut,
                         heureFin=heureFin,
                    )
               except:
                    pass
          return super().form_valid(form)

class ItineraireUpdateView(UpdateView):
     model = Itineraire
     template_name = 'itineraire/update.html'
     form_class  = ItineraireUpdateForm
     success_url = reverse_lazy('transport_scolaire:itineraire-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          itineraire = form.save()
          date_assignations= self.request.POST.getlist('date_assignation[]')
          buss= self.request.POST.getlist('bus[]')
          busassignations= self.request.POST.getlist('busassignation[]')
          # Delete BusAssignation objects that are not in the BusAssignations list
          busassignations_digits = [int(value) for value in self.request.POST.getlist('busassignation[]') if value.isdigit()]
          BusAssignation.objects.filter(itineraire=itineraire).exclude(pk__in=busassignations_digits).delete()
          for busassignation, date_assignation, bus in zip( busassignations, date_assignations, buss):
               if busassignation:
                    BusAssignation.objects.filter(pk=busassignation).update(
                    itineraire=itineraire,
                    date_assignation=date_assignation,
                    bus=Bus.objects.get(pk=bus),
               )
               else:
                    BusAssignation.objects.create(
                    itineraire=itineraire,
               date_assignation=date_assignation,
               bus=Bus.objects.get(pk=bus),
               )
          pointArrets= self.request.POST.getlist('pointArret[]')
          heureDebuts= self.request.POST.getlist('heureDebut[]')
          heureFins= self.request.POST.getlist('heureFin[]')
          horaires= self.request.POST.getlist('horaire[]')
          # Delete Horaire objects that are not in the Horaires list
          horaires_digits = [int(value) for value in self.request.POST.getlist('horaire[]') if value.isdigit()]
          Horaire.objects.filter(itineraire=itineraire).exclude(pk__in=horaires_digits).delete()
          for horaire, pointArret, heureDebut, heureFin in zip( horaires, pointArrets, heureDebuts, heureFins):
               if horaire:
                    Horaire.objects.filter(pk=horaire).update(
                    itineraire=itineraire,
                    pointArret=LieuLigne.objects.get(pk=pointArret),
                    heureDebut=heureDebut,
                    heureFin=heureFin,
               )
               else:
                    Horaire.objects.create(
                    itineraire=itineraire,
               pointArret=LieuLigne.objects.get(pk=pointArret),
               heureDebut=heureDebut,
               heureFin=heureFin,
               )
          return super().form_valid(form)

class ItineraireDeleteView(DeleteView):
     model = Itineraire
     template_name = 'itineraire/delete.html'
     success_url = reverse_lazy('transport_scolaire:itineraire-list')
class HoraireListView(ListView):
     model = Horaire
     template_name = 'horaire/list.html'
     context_object_name = 'horaires'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =Horaire.objects.all().order_by('-pk')
          search_filter = self.request.GET.get('search_filter_pointArret') or ''
          if search_filter:
               objects=objects.filter(Q(pointArret__pk=search_filter))
               context['search_filter_pointArret']=search_filter
          search_filter = self.request.GET.get('search_filter_itineraire') or ''
          if search_filter:
               objects=objects.filter(Q(itineraire__pk=search_filter))
               context['search_filter_itineraire']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) | Q(heureDebut__icontains=search_query) | Q(heureFin__icontains=search_query) )
          context['search_query']=search_query
          context['pointArrets']=LieuLigne.objects.all()
          context['itineraires']=Itineraire.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['horaires']=page_obj
          return context

class HoraireDetailView(DetailView):
     model = Horaire
     template_name = 'horaire/detail.html'
     context_object_name = 'horaires'

class HoraireCreateView(CreateView):
     model = Horaire
     template_name = 'horaire/create.html'
     form_class  = HoraireCreateForm
     success_url = reverse_lazy('transport_scolaire:horaire-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          horaire = form.save()
          return super().form_valid(form)

class HoraireUpdateView(UpdateView):
     model = Horaire
     template_name = 'horaire/update.html'
     form_class  = HoraireUpdateForm
     success_url = reverse_lazy('transport_scolaire:horaire-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          horaire = form.save()
          return super().form_valid(form)

class HoraireDeleteView(DeleteView):
     model = Horaire
     template_name = 'horaire/delete.html'
     success_url = reverse_lazy('transport_scolaire:horaire-list')
class BusAssignationListView(ListView):
     model = BusAssignation
     template_name = 'busassignation/list.html'
     context_object_name = 'busassignations'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =BusAssignation.objects.all().order_by('-pk')
          search_filter_gte = self.request.GET.get('search_filter_date_assignation_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_assignation_lte') or ''
          if search_filter_gte and search_filter_lte:
               objects=objects.filter(date_assignation__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               objects=objects.filter(date_assignation__lte=search_filter_lte)
          elif search_filter_gte:
               objects=objects.filter(date_assignation__gte=search_filter_gte)
          context['search_filter_date_assignation_gte']=search_filter_gte
          context['search_filter_date_assignation_lte']=search_filter_lte
          search_filter = self.request.GET.get('search_filter_bus') or ''
          if search_filter:
               objects=objects.filter(Q(bus__pk=search_filter))
               context['search_filter_bus']=search_filter
          search_filter = self.request.GET.get('search_filter_itineraire') or ''
          if search_filter:
               objects=objects.filter(Q(itineraire__pk=search_filter))
               context['search_filter_itineraire']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) )
          context['search_query']=search_query
          context['buss']=Bus.objects.all()
          context['itineraires']=Itineraire.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['busassignations']=page_obj
          return context

class BusAssignationDetailView(DetailView):
     model = BusAssignation
     template_name = 'busassignation/detail.html'
     context_object_name = 'busassignations'

class BusAssignationCreateView(CreateView):
     model = BusAssignation
     template_name = 'busassignation/create.html'
     form_class  = BusAssignationCreateForm
     success_url = reverse_lazy('transport_scolaire:busassignation-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          busassignation = form.save()
          return super().form_valid(form)

class BusAssignationUpdateView(UpdateView):
     model = BusAssignation
     template_name = 'busassignation/update.html'
     form_class  = BusAssignationUpdateForm
     success_url = reverse_lazy('transport_scolaire:busassignation-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          busassignation = form.save()
          return super().form_valid(form)

class BusAssignationDeleteView(DeleteView):
     model = BusAssignation
     template_name = 'busassignation/delete.html'
     success_url = reverse_lazy('transport_scolaire:busassignation-list')
class AssignationItineraireListView(ListView):
     model = AssignationItineraire
     template_name = 'assignationitineraire/list.html'
     context_object_name = 'assignationitineraires'
     number_page =3
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context= super().get_context_data(**kwargs)
          search_query = self.request.GET.get('search_query') or ''
          objects =AssignationItineraire.objects.all().order_by('-pk')
          search_filter_gte = self.request.GET.get('search_filter_dateAssigntion_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_dateAssigntion_lte') or ''
          if search_filter_gte and search_filter_lte:
               objects=objects.filter(dateAssigntion__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               objects=objects.filter(dateAssigntion__lte=search_filter_lte)
          elif search_filter_gte:
               objects=objects.filter(dateAssigntion__gte=search_filter_gte)
          context['search_filter_dateAssigntion_gte']=search_filter_gte
          context['search_filter_dateAssigntion_lte']=search_filter_lte
          search_filter = self.request.GET.get('search_filter_eleve') or ''
          if search_filter:
               objects=objects.filter(Q(eleve__pk=search_filter))
               context['search_filter_eleve']=search_filter
          search_filter = self.request.GET.get('search_filter_itineraire') or ''
          if search_filter:
               objects=objects.filter(Q(itineraire__pk=search_filter))
               context['search_filter_itineraire']=search_filter
          if search_query:
               objects=objects.filter(Q(pk__icontains=search_query) )
          context['search_query']=search_query
          context['eleves']=Eleve.objects.all()
          context['itineraires']=Itineraire.objects.all()
          paginator = Paginator(objects,self.number_page)
          page_number = self.request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context['assignationitineraires']=page_obj
          return context

class AssignationItineraireDetailView(DetailView):
     model = AssignationItineraire
     template_name = 'assignationitineraire/detail.html'
     context_object_name = 'assignationitineraires'

class AssignationItineraireCreateView(CreateView):
     model = AssignationItineraire
     template_name = 'assignationitineraire/create.html'
     form_class  = AssignationItineraireCreateForm
     success_url = reverse_lazy('transport_scolaire:assignationitineraire-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          assignationitineraire = form.save()
          return super().form_valid(form)

class AssignationItineraireUpdateView(UpdateView):
     model = AssignationItineraire
     template_name = 'assignationitineraire/update.html'
     form_class  = AssignationItineraireUpdateForm
     success_url = reverse_lazy('transport_scolaire:assignationitineraire-list')
     def form_valid(self, form: BaseModelForm) -> HttpResponse:
          assignationitineraire = form.save()
          return super().form_valid(form)

class AssignationItineraireDeleteView(DeleteView):
     model = AssignationItineraire
     template_name = 'assignationitineraire/delete.html'
     success_url = reverse_lazy('transport_scolaire:assignationitineraire-list')

