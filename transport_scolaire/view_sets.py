from typing import Any

from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import viewsets
from .models import ( AnneeInscription, Chauffeur, EcoleAssignation, Inscription , TypeVehicule , Bus , LieuLigne , Ligne , LieuRamassage , OrdreLieu , Ecole , Classe , Parent , Eleve , Itineraire , Horaire , BusAssignation , AssignationItineraire ,)
from .serializers import (AnneeInscriptionSerializer, ChauffeurSerializer, EcoleAssignationDetailSerializer, EcoleAssignationSerializer, InscriptionDetailSerializer, InscriptionSerializer,TypeVehiculeSerializer,BusSerializer,LieuLigneSerializer,LigneSerializer,LieuRamassageSerializer,OrdreLieuSerializer,EcoleSerializer,ClasseSerializer,ParentSerializer,EleveSerializer,ItineraireSerializer,HoraireSerializer,BusAssignationSerializer,AssignationItineraireSerializer,)
from .serializers import (ChauffeurDetailSerializer,TypeVehiculeDetailSerializer,BusDetailSerializer,LieuLigneDetailSerializer,LigneDetailSerializer,LieuRamassageDetailSerializer,OrdreLieuDetailSerializer,EcoleDetailSerializer,ClasseDetailSerializer,ParentDetailSerializer,EleveDetailSerializer,ItineraireDetailSerializer,HoraireDetailSerializer,BusAssignationDetailSerializer,AssignationItineraireDetailSerializer,)
from .serializers import (ChauffeurMinSerializer,TypeVehiculeMinSerializer,BusMinSerializer,LieuLigneMinSerializer,LigneMinSerializer,LieuRamassageMinSerializer,OrdreLieuMinSerializer,EcoleMinSerializer,ClasseMinSerializer,ParentMinSerializer,EleveMinSerializer,ItineraireMinSerializer,HoraireMinSerializer,BusAssignationMinSerializer,AssignationItineraireMinSerializer,)
from .tasks import send_confirmation_email
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AssignationBusItineraireViewSet(APIView):
     # permission_classes = [IsAuthenticated]
     serializer = AssignationItineraire  # Remplacez UserSerializer par votre propre sérialiseur d'utilisateur

     def get(self, request):
               
          return Response(request.data)
          #    serialized_user = self.user_serializer(request.user).data
          #    return Response({'token': 'Token is valid', 'user': serialized_user})
     
     

     def post(self, request):
          print(request.data)
          try:
               for ass in request.data:
                    assignationItineraire = AssignationItineraire.objects.get(pk=ass.get('pk'))
                    assignationItineraire.bus = Bus.objects.get(pk=ass.get('bus'))
                    assignationItineraire.save()
               
               
               return Response({"data","ok"})
          
          except AssignationItineraire.DoesNotExist:
               return Response({'error': 'AssignationItineraire does not exist'}, status=status.HTTP_404_NOT_FOUND)
          
          except Bus.DoesNotExist:
               return Response({'error': 'Bus does not exist'}, status=status.HTTP_404_NOT_FOUND)
          
          except BaseException as e:
               return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         


class CountViewSet(APIView):
    def get(self, request):
        
        # Logique de récupération des données
        ligne_eleve=[]

        

        colors=['#6C9BCF', '#1B9C85', '#FF0060','#6C9BCF', '#1B9C85', '#FF0060']
        reprs=[ligne.__str__() for ligne in Ligne.objects.all()]

        data=[len(ligne.inscription_set.all()) for ligne in Ligne.objects.all()]

        ligne_eleve={
             'colors':colors,
             'labels':reprs,
             'values':data
        }

        data = {
               'eleve': Inscription.objects.filter(etat="validé").count(),
               'bus': Bus.objects.count(),
               'ligne_eleve':ligne_eleve,
               'ligne': Ligne.objects.count(),
               'inscription_en_attente': Inscription.objects.filter(etat="en_attente").count(),
               'inscription_annule': Inscription.objects.filter(etat="annulé").count(),
          }
        
        return Response(data)

class CustomPagination(PageNumberPagination):
    page_size = 5
    
class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class ChauffeurViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Chauffeur.objects.all().order_by('-pk')
     serializer_class = ChauffeurSerializer
     detail_serializer_class = ChauffeurDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom__icontains=search_query) | Q(prenoms__icontains=search_query) | Q(tel__icontains=search_query) | Q(email__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               chauffeur=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               chauffeur=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class AnneeInscriptionViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = AnneeInscription.objects.all().order_by('-pk')
     serializer_class = AnneeInscriptionSerializer
     detail_serializer_class = AnneeInscriptionSerializer

class TypeVehiculeViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = TypeVehicule.objects.all().order_by('-pk')
     serializer_class = TypeVehiculeSerializer
     detail_serializer_class = TypeVehiculeDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               typevehicule=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               typevehicule=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class BusViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Bus.objects.all().order_by('-pk')
     serializer_class = BusSerializer
     detail_serializer_class = BusDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter = self.request.GET.get('search_filter_type') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(type__pk=search_filter))
          search_filter = self.request.GET.get('search_filter_chauffeur') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(chauffeur__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(immatriculation__icontains=search_query) | Q(couleur__icontains=search_query) | Q(nbr_place__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               bus=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               bus=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class LieuLigneViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = LieuLigne.objects.all().order_by('-pk')
     serializer_class = LieuLigneSerializer
     detail_serializer_class = LieuLigneDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom_lieu__icontains=search_query) | Q(latitude__icontains=search_query) | Q(longitude__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               lieuligne=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               lieuligne=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class LigneViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Ligne.objects.all().order_by('-pk')
     serializer_class = LigneSerializer
     detail_serializer_class = LigneDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):

          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               ligne=serializer.save()
               for ordrelieu in request.data['ordrelieus']:
                    ordrelieu['ligne']=ligne.pk
                    ordrelieu_serializer=OrdreLieuSerializer(data=ordrelieu)
                    if ordrelieu_serializer.is_valid():
                         ordrelieu_serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               ligne=serializer.save()
               # Mettre à jour les ordrelieus existants pour cette ligne
               ordrelieus_digits = [int(value['pk']) for value in request.data['ordrelieus'] if value.get('pk',None)]
               OrdreLieu.objects.filter(ligne=ligne).exclude(pk__in=ordrelieus_digits).delete()
               for ordrelieu in request.data['ordrelieus']:
                    ordrelieu['ligne']=ligne.pk
                    instance_ordrelieu = OrdreLieu.objects.filter(pk=ordrelieu.get('pk',None)).first()
                    ordrelieu_serializer=OrdreLieuSerializer(instance_ordrelieu,data=ordrelieu)
                    if ordrelieu_serializer.is_valid():
                         ordrelieu_serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class LieuRamassageViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = LieuRamassage.objects.all().order_by('-pk')
     serializer_class = LieuRamassageSerializer
     detail_serializer_class = LieuRamassageDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ligne__pk=search_filter))
          search_filter = self.request.GET.get('search_filter_lieu_ligne') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(lieu_ligne__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom_lieu__icontains=search_query) | Q(latitude__icontains=search_query) | Q(longitude__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               lieuramassage=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               lieuramassage=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class OrdreLieuViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = OrdreLieu.objects.all().order_by('-pk')
     serializer_class = OrdreLieuSerializer
     detail_serializer_class = OrdreLieuDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ligne__pk=search_filter))
          search_filter = self.request.GET.get('search_filter_lieu_ligne') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(lieu_ligne__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(num_ordre__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               ordrelieu=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               ordrelieu=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class EcoleViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Ecole.objects.all().order_by('-pk')
     serializer_class = EcoleSerializer
     detail_serializer_class = EcoleDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               ecole=serializer.save()
               for classe in request.data['classes']:
                    classe['ecole']=ecole.pk
                    classe_serializer=ClasseSerializer(data=classe)
                    if classe_serializer.is_valid():
                         classe_serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               ecole=serializer.save()
               # Mettre à jour les classes existants pour cette ecole
               classes_digits = [int(value['pk']) for value in request.data['classes'] if value.get('pk',None)]
               Classe.objects.filter(ecole=ecole).exclude(pk__in=classes_digits).delete()
               for classe in request.data['classes']:
                    classe['ecole']=ecole.pk
                    instance_classe = Classe.objects.filter(pk=classe.get('pk',None)).first()
                    classe_serializer=ClasseSerializer(instance_classe,data=classe)
                    if classe_serializer.is_valid():
                         classe_serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class ClasseViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Classe.objects.all().order_by('-pk')
     serializer_class = ClasseSerializer
     detail_serializer_class = ClasseDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter = self.request.GET.get('search_filter_ecole') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ecole__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               classe=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               classe=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class ParentViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Parent.objects.all().order_by('-pk')
     serializer_class = ParentSerializer
     detail_serializer_class = ParentDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(nom_mere__icontains=search_query) | Q(nom_pere__icontains=search_query) | Q(tel_mere__icontains=search_query) | Q(tel_pere__icontains=search_query) | Q(email__icontains=search_query) | Q(adresse__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               parent=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               parent=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


from django.core.mail import send_mail
from django.conf import settings

class EleveViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Eleve.objects.all().order_by('-pk')
     serializer_class = EleveSerializer
     detail_serializer_class = EleveDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):

          # if request.user.is_superuser==False:
          #       self.queryset=self.queryset.filter(user__id=request.user.id)
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()


          search_filter_gte = self.request.GET.get('search_filter_date_inscription_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_inscription_lte') or ''


          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(date_inscription__range=[search_filter_gte, search_filter_lte])
          
          
          elif search_filter_lte:
               self.queryset=self.queryset.filter(date_inscription__lte=search_filter_lte)


          elif search_filter_gte:
               self.queryset=self.queryset.filter(date_inscription__gte=search_filter_gte)


          search_filter_gte = self.request.GET.get('search_filter_date_naissance_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_naissance_lte') or ''


          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(date_naissance__range=[search_filter_gte, search_filter_lte])
       
       
          elif search_filter_lte:
               self.queryset=self.queryset.filter(date_naissance__lte=search_filter_lte)


          elif search_filter_gte:
               self.queryset=self.queryset.filter(date_naissance__gte=search_filter_gte)


          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ligne__pk=search_filter))


          search_filter = self.request.GET.get('search_filter_parent') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(parent__pk=search_filter))


          search_filter = self.request.GET.get('search_filter_ecole') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ecole__pk=search_filter))


          search_filter = self.request.GET.get('search_filter_classe') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(classe__pk=search_filter))


          search_filter = self.request.GET.get('search_filter_lieu_ramassage') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(lieu_ramassage__pk=search_filter))

          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
                    | Q(image__icontains=search_query) | Q(nom__icontains=search_query) | 
                    Q(prenoms__icontains=search_query) | Q(adresse__icontains=search_query) 
                    )
               
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()

          print(request.data)

          
          
          parent_serializer = ParentSerializer(data=request.data.get('parent',{}))
          if parent_serializer.is_valid():
               parent = parent_serializer.save()
               request.data['parent']=parent.pk
          
          
          user_serializer = UserSerializer(data=request.data.get('user',{}))

          print(request.user)

          print(request.data['user'].get('username',''))

          if request.user.pk:
               print("add user")
               print(request.user.username)
               request.data['user']=request.user.pk
               # return Response({})
          
          else:
               print("create user")
               username=request.data['user'].get('username','')
               email=request.data['user'].get('email','')
               role=request.data['user'].get('role','')
               password=request.data['user'].get('password','')

               if User.objects.filter(username=username).exists():
                      return Response({"user":{"username":'Nom d\'utilisateur déjà pris.'}}, status=status.HTTP_400_BAD_REQUEST)

               if User.objects.filter(email=email).exists():
                      return Response({"user":{"email":'Email d\'utilisateur déjà pris.'}}, status=status.HTTP_400_BAD_REQUEST)

               user=User.objects.create_user(username=username,password=password)
               user.role=role
               user.email=email
               user.save()
               request.data['user']=user.pk
          
          classe_serializer = ClasseSerializer(data=request.data.get('new_classe',{}))
          if request.data.get('create_classe',None):
               if classe_serializer.is_valid():
                    classe = classe_serializer.save()
                    request.data['classe']=classe.pk

          lieu_ramassage_serializer = LieuRamassageSerializer(data=request.data.get('new_lieu_ramassage',{}))
          if request.data.get('create_lieu_ramassage',None):
               if lieu_ramassage_serializer.is_valid():
                    lieu_ramassage = lieu_ramassage_serializer.save()
                    request.data['lieu_ramassage']=lieu_ramassage.pk

          # Lieu Remisage
          lieu_remisage_serializer = LieuRamassageSerializer(data=request.data.get('new_lieu_remisage',{}))

          print("lieu de remisage : ")

          print(request.data['lieu_remisage'])

          print(request.data.get('new_lieu_remisage',{}))

          if request.data.get('create_lieu_remisage',None):
               
               if lieu_remisage_serializer.is_valid():
                    lieu_remisage = lieu_remisage_serializer.save()
                    print("tesrtuuuuuuuuuuuuuuuuuuuuuu")
                    request.data['lieu_remisage']=lieu_remisage.pk
               else:
                    print("non validé")

          serializer = self.serializer_class(data=request.data)
          inscription_serializer=InscriptionSerializer(data=request.data)

          if serializer.is_valid():
               print(request.data['user'])
               eleve=serializer.save()

               date_inscription=request.data

               date_inscription['eleve']=eleve.pk

               date_inscription['annee']=AnneeInscription.objects.latest('pk').pk

               if inscription_serializer.is_valid():

                    inscription=inscription_serializer.save()
                    
                    for assignationitineraire in request.data['assignationitineraires']:
                         assignationitineraire['inscription']=inscription.pk
                         
                         assignationitineraire_serializer=AssignationItineraireSerializer(data=assignationitineraire)

                         if assignationitineraire_serializer.is_valid():
                              assignationitineraire_serializer.save()

                         else:
                              print(assignationitineraire_serializer.errors)

                    
                         return Response(serializer.data, status=status.HTTP_201_CREATED)

               else:
                    print(inscription_serializer.errors)

          errors=serializer.errors
          if not parent_serializer.is_valid():
               errors['parent']=parent_serializer.errors
          #id
          if (not classe_serializer.is_valid()) and  request.data.get('create_classe',None):
               errors['classe']=classe_serializer.errors

          if (not lieu_ramassage_serializer.is_valid()) and  request.data.get('create_lieu_ramassage',None):
               errors['lieu_ramassage']=lieu_ramassage_serializer.errors

          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance:Eleve
          instance = self.get_object()
          validation=request.data.get('validation','') 
          annulation=request.data.get('annulation','') 
          if validation:
               subject = 'Confirmation d\'inscription au transport scolaire'
               message = f'''Cher élève,Responsable ou Parent,
               
               Nous sommes ravis de vous informer que l' inscription de l'éleve {instance.nom.upper} {instance.prenoms.capitalize} 
               
               au transport scolaire a été confirmée avec succès.

               Ligne: {instance.ligne}
               Lieu de Ramassage: {instance.lieu_ramassage}

               Votre participation est très importante pour nous et nous sommes impatients de vous accueillir à bord.
               
               . Les horaires et les itinéraires seront communiqués ultérieurement.
               Si vous avez des questions ou des préoccupations, n\'hésitez pas à nous contacter.\n\nCordialement,
               
               L\'équipe du transport scolaire
               '''
               if instance.user:
                    recipient_list = [instance.user.email]

                    send_confirmation_email(subject, message, recipient_list)

               instance.etat = request.data.get('etat')
               instance.save()
               serializer = self.serializer_class(instance)
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          elif annulation:
               subject = 'Annulation d\'inscription au transport scolaire'
               message = f'''Cher élève,Responsable ou Parent,
               
               Nous sommes desolé de vous informer que l' inscription de l'éleve {instance.nom.upper} {instance.prenoms.capitalize} 
               
               au transport scolaire a été annulée.

               Ligne: {instance.ligne}
               Lieu de Ramassage: {instance.lieu_ramassage}

               Votre participation est très importante pour nous et nous sommes impatients de vous accueillir à bord.
               
               . Les horaires et les itinéraires seront communiqués ultérieurement.
               Si vous avez des questions ou des préoccupations, n\'hésitez pas à nous contacter.\n\nCordialement,
               
               L\'équipe du transport scolaire
               '''

               if instance.user:
                    recipient_list = [instance.user.email]

                    send_confirmation_email(subject, message, recipient_list)

               instance.etat = request.data.get('etat')
               instance.save()
               serializer = self.serializer_class(instance)
               return Response(serializer.data, status=status.HTTP_201_CREATED)
               
               
          parent_serializer = ParentSerializer(data=request.data['parent'])
          if parent_serializer.is_valid():
               parent = parent_serializer.save()
               request.data['parent']=parent.pk
          serializer = self.serializer_class(instance,data=request.data,partial=True)
          if serializer.is_valid():
               eleve=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          if not parent_serializer.is_valid():
               errors['parent']=parent_serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class InscriptionViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Inscription.objects.all().order_by('-pk')
     serializer_class = InscriptionSerializer
     detail_serializer_class = InscriptionDetailSerializer

     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):

          # if request.user.is_superuser==False:
          #       self.queryset=self.queryset.filter(user__id=request.user.id)
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()


          search_filter_gte = self.request.GET.get('search_filter_date_inscription_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_inscription_lte') or ''


          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(date_inscription__range=[search_filter_gte, search_filter_lte])
          
          
          elif search_filter_lte:
               self.queryset=self.queryset.filter(date_inscription__lte=search_filter_lte)


          elif search_filter_gte:
               self.queryset=self.queryset.filter(date_inscription__gte=search_filter_gte)


          search_filter_gte = self.request.GET.get('search_filter_date_naissance_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_naissance_lte') or ''


          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(eleve__date_naissance__range=[search_filter_gte, search_filter_lte])
       
       
          elif search_filter_lte:
               self.queryset=self.queryset.filter(eleve__date_naissance__lte=search_filter_lte)


          elif search_filter_gte:
               self.queryset=self.queryset.filter(eleve__date_naissance__gte=search_filter_gte)


          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ligne__pk=search_filter))


          search_filter = self.request.GET.get('search_filter_parent') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(eleve__parent__pk=search_filter))


          search_filter = self.request.GET.get('search_filter_ecole') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(eleve__ecole__pk=search_filter))

          search_filter = self.request.GET.get('search_filter_etat') or ''
          print(search_filter,"ddd")
          if search_filter:
               self.queryset=self.queryset.filter(Q(etat=search_filter))

          search_filter = self.request.GET.get('search_filter_classe') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(classe__pk=search_filter))


          search_filter = self.request.GET.get('search_filter_lieu_ramassage') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(lieu_ramassage__pk=search_filter))

          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
                    | Q(image__icontains=search_query) | Q(nom__icontains=search_query) | 
                    Q(prenoms__icontains=search_query) | Q(adresse__icontains=search_query) |
                    Q(montant_frais__icontains=search_query) | Q(etat__icontains=search_query) )
               
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          
          parent_serializer = ParentSerializer(data=request.data.get('parent',{}))
          if parent_serializer.is_valid():
               parent = parent_serializer.save()
               request.data['parent']=parent.pk
          
          user_serializer = UserSerializer(data=request.data.get('user',{}))

          print(request.user)

          print(request.data['user'].get('username',''))

          if request.user.pk:
               print("add user")
               print(request.user.username)
               request.data['user']=request.user.pk
               # return Response({})
          
          else:
               print("create user")
               username=request.data['user'].get('username','')
               email=request.data['user'].get('email','')
               role=request.data['user'].get('role','')
               password=request.data['user'].get('password','')

               if User.objects.filter(username=username).exists():
                      return Response({"user":{"username":'Nom d\'utilisateur déjà pris.'}}, status=status.HTTP_400_BAD_REQUEST)

               if User.objects.filter(email=email).exists():
                      return Response({"user":{"email":'Email d\'utilisateur déjà pris.'}}, status=status.HTTP_400_BAD_REQUEST)

               user=User.objects.create_user(username=username,password=password)
               user.role=role
               user.email=email
               user.save()
               request.data['user']=user.pk
          
          classe_serializer = ClasseSerializer(data=request.data.get('new_classe',{}))
          if request.data.get('create_classe',None):
               if classe_serializer.is_valid():
                    classe = classe_serializer.save()
                    request.data['classe']=classe.pk

          lieu_ramassage_serializer = LieuRamassageSerializer(data=request.data.get('new_lieu_ramassage',{}))
          if request.data.get('create_lieu_ramassage',None):
               if lieu_ramassage_serializer.is_valid():
                    lieu_ramassage = lieu_ramassage_serializer.save()
                    request.data['lieu_ramassage']=lieu_ramassage.pk

          # Lieu Remisage
          lieu_remisage_serializer = LieuRamassageSerializer(data=request.data.get('new_lieu_remisage',{}))

          print("lieu de remisage : ")

          print(request.data['lieu_remisage'])

          print(request.data.get('new_lieu_remisage',{}))

          if request.data.get('create_lieu_remisage',None):
               
               if lieu_remisage_serializer.is_valid():
                    lieu_remisage = lieu_remisage_serializer.save()
                    print("tesrtuuuuuuuuuuuuuuuuuuuuuu")
                    request.data['lieu_remisage']=lieu_remisage.pk
               else:
                    print("non validé")

          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               print(request.data['user'])
               eleve=serializer.save()

               for assignationitineraire in request.data['assignationitineraires']:
                    assignationitineraire['eleve']=eleve.pk
                    assignationitineraire_serializer=AssignationItineraireSerializer(data=assignationitineraire)

                    if assignationitineraire_serializer.is_valid():
                         assignationitineraire_serializer.save()
                    else:
                         print(assignationitineraire_serializer.errors)

               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          if not parent_serializer.is_valid():
               errors['parent']=parent_serializer.errors
          #id
          if (not classe_serializer.is_valid()) and  request.data.get('create_classe',None):
               errors['classe']=classe_serializer.errors

          if (not lieu_ramassage_serializer.is_valid()) and  request.data.get('create_lieu_ramassage',None):
               errors['lieu_ramassage']=lieu_ramassage_serializer.errors

          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance:Eleve
          instance = self.get_object()
          validation=request.data.get('validation','') 
          annulation=request.data.get('annulation','') 
          if validation:
               subject = 'Confirmation d\'inscription au transport scolaire'
               message = f'''Cher élève,Responsable ou Parent,
               
               Nous sommes ravis de vous informer que l' inscription de l'éleve {instance.eleve.nom.upper} {instance.eleve.prenoms.capitalize} 
               
               au transport scolaire a été confirmée avec succès.
\n
               Ligne: {instance.ligne}
               Lieu de Ramassage: {instance.lieu_ramassage}

               Votre participation est très importante pour nous et nous sommes impatients de vous accueillir à bord.
               \n
               . Les horaires et les itinéraires seront communiqués ultérieurement.
               Si vous avez des questions ou des préoccupations, n\'hésitez pas à nous contacter.\n\nCordialement,
               
               L\'équipe du transport scolaire
               '''
               if instance.user:
                    recipient_list = [instance.user.email]

                    send_confirmation_email(subject, message, recipient_list)

               instance.etat = request.data.get('etat')
               instance.save()
               serializer = self.serializer_class(instance)
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          elif annulation:
               subject = 'Annulation d\'inscription au transport scolaire'
               message = f'''Cher élève,Responsable ou Parent,
               
               Nous sommes desolé de vous informer que l' inscription de l'éleve {instance.eleve.nom.upper} {instance.eleve.prenoms.capitalize} 
               
               au transport scolaire a été annulée.

               Ligne: {instance.ligne}
               Lieu de Ramassage: {instance.lieu_ramassage}

               Votre participation est très importante pour nous et nous sommes impatients de vous accueillir à bord.
               
               . Les horaires et les itinéraires seront communiqués ultérieurement.
               Si vous avez des questions ou des préoccupations, n\'hésitez pas à nous contacter.\n\nCordialement,
               
               L\'équipe du transport scolaire
               '''

               if instance.user:
                    recipient_list = [instance.user.email]

                    send_confirmation_email(subject, message, recipient_list)

               instance.etat = request.data.get('etat')
               instance.save()
               serializer = self.serializer_class(instance)
               return Response(serializer.data, status=status.HTTP_201_CREATED)
               
               
          parent_serializer = ParentSerializer(data=request.data['parent'])
          if parent_serializer.is_valid():
               parent = parent_serializer.save()
               request.data['parent']=parent.pk
          serializer = self.serializer_class(instance,data=request.data,partial=True)
          if serializer.is_valid():
               eleve=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          if not parent_serializer.is_valid():
               errors['parent']=parent_serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class ItineraireViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Itineraire.objects.all().order_by('-pk')
     serializer_class = ItineraireSerializer
     detail_serializer_class = ItineraireDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter_gte = self.request.GET.get('search_filter_date_itineraire_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_itineraire_lte') or ''
          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(date_itineraire__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               self.queryset=self.queryset.filter(date_itineraire__lte=search_filter_lte)
          elif search_filter_gte:
               self.queryset=self.queryset.filter(date_itineraire__gte=search_filter_gte)
          search_filter = self.request.GET.get('search_filter_ligne') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ligne__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(ligne_inverse__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               itineraire=serializer.save()
               for busassignation in request.data['busassignations']:
                    busassignation['itineraire']=itineraire.pk
                    busassignation_serializer=BusAssignationSerializer(data=busassignation)
                    if busassignation_serializer.is_valid():
                         busassignation_serializer.save()

               for horaire in request.data['horaires']:
                    horaire['itineraire']=itineraire.pk
                    horaire_serializer=HoraireSerializer(data=horaire)
                    if horaire_serializer.is_valid():
                         horaire_serializer.save()
               
               for ecoleassignation in request.data['ecoleassignations']:
                    ecoleassignation['itineraire']=itineraire.pk
                    ecoleassignation_serializer=EcoleAssignationSerializer(data=ecoleassignation)

                    if ecoleassignation_serializer.is_valid():
                         ecoleassignation_serializer.save()
                    else:
                         print(ecoleassignation_serializer.errors)

               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               itineraire=serializer.save()

               # Mettre à jour les busassignations existants pour cette itineraire
               busassignations_digits = [int(value['pk']) for value in request.data['busassignations'] if value.get('pk',None)]
               BusAssignation.objects.filter(itineraire=itineraire).exclude(pk__in=busassignations_digits).delete()
               for busassignation in request.data['busassignations']:
                    busassignation['itineraire']=itineraire.pk
                    instance_busassignation = BusAssignation.objects.filter(pk=busassignation.get('pk',None)).first()
                    busassignation_serializer=BusAssignationSerializer(instance_busassignation,data=busassignation)
                    if busassignation_serializer.is_valid():
                         busassignation_serializer.save()

               # Mettre à jour les horaires existants pour cette itineraire
               horaires_digits = [int(value['pk']) for value in request.data['horaires'] if value.get('pk',None)]
               Horaire.objects.filter(itineraire=itineraire).exclude(pk__in=horaires_digits).delete()
               for horaire in request.data['horaires']:
                    horaire['itineraire']=itineraire.pk
                    instance_horaire = Horaire.objects.filter(pk=horaire.get('pk',None)).first()
                    horaire_serializer=HoraireSerializer(instance_horaire,data=horaire)
                    if horaire_serializer.is_valid():
                         horaire_serializer.save()
               
               # Mettre à jour les ecoleassignations existants pour cette itineraire
               ecoleassignations_digits = [int(value['pk']) for value in request.data['ecoleassignations'] if value.get('pk',None)]
               EcoleAssignation.objects.filter(itineraire=itineraire).exclude(pk__in=ecoleassignations_digits).delete()
               for ecoleassignation in request.data['ecoleassignations']:
                    ecoleassignation['itineraire']=itineraire.pk
                    instance_ecoleassignation = EcoleAssignation.objects.filter(pk=ecoleassignation.get('pk',None)).first()
                    ecoleassignation_serializer=EcoleAssignationSerializer(instance_ecoleassignation,data=ecoleassignation)
                    if ecoleassignation_serializer.is_valid():
                         ecoleassignation_serializer.save()

               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class HoraireViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = Horaire.objects.all().order_by('-pk')
     serializer_class = HoraireSerializer
     detail_serializer_class = HoraireDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter = self.request.GET.get('search_filter_pointArret') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(pointArret__pk=search_filter))
          search_filter = self.request.GET.get('search_filter_itineraire') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(itineraire__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
| Q(heureDebut__icontains=search_query) | Q(heureFin__icontains=search_query) )
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               horaire=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               horaire=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)



class EcoleAssignationViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = EcoleAssignation.objects.all().order_by('-pk')
     serializer_class = EcoleAssignationSerializer
     detail_serializer_class = EcoleAssignationDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter_gte = self.request.GET.get('search_filter_date_assignation_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_assignation_lte') or ''
          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(date_assignation__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               self.queryset=self.queryset.filter(date_assignation__lte=search_filter_lte)
          elif search_filter_gte:
               self.queryset=self.queryset.filter(date_assignation__gte=search_filter_gte)
          search_filter = self.request.GET.get('search_filter_itineraire') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(itineraire__pk=search_filter))
          search_filter = self.request.GET.get('search_filter_ecole') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(ecole__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
)
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               ecoleassignation=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               ecoleassignation=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class BusAssignationViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = BusAssignation.objects.all().order_by('-pk')
     serializer_class = BusAssignationSerializer
     detail_serializer_class = BusAssignationDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter_gte = self.request.GET.get('search_filter_date_assignation_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_date_assignation_lte') or ''
          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(date_assignation__range=[search_filter_gte, search_filter_lte])
          elif search_filter_lte:
               self.queryset=self.queryset.filter(date_assignation__lte=search_filter_lte)
          elif search_filter_gte:
               self.queryset=self.queryset.filter(date_assignation__gte=search_filter_gte)
          search_filter = self.request.GET.get('search_filter_bus') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(bus__pk=search_filter))
          search_filter = self.request.GET.get('search_filter_itineraire') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(itineraire__pk=search_filter))
          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
)
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               busassignation=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               busassignation=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class AssignationItineraireViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
     queryset = AssignationItineraire.objects.all().order_by('-pk')
     serializer_class = AssignationItineraireSerializer
     detail_serializer_class = AssignationItineraireDetailSerializer
     def get_paginator(self):
          if 'paginate' in self.request.query_params and self.request.query_params['paginate'] == 'false':
               return None  # Désactive la pagination si le paramètre 'paginate' est 'false'
          return CustomPagination


     def get_serializer_context(self):
          context=super().get_serializer_context()
          context['request'] = self.request
          return context


     def list(self, request, *args, **kwargs):
          search_query = self.request.query_params.get('search_query', '')
          self.pagination_class = self.get_paginator()
          search_filter_gte = self.request.GET.get('search_filter_dateAssigntion_gte') or ''
          search_filter_lte = self.request.GET.get('search_filter_dateAssigntion_lte') or ''
          if search_filter_gte and search_filter_lte:
               self.queryset=self.queryset.filter(dateAssigntion__range=[search_filter_gte, search_filter_lte])
          
          elif search_filter_lte:
               self.queryset=self.queryset.filter(dateAssigntion__lte=search_filter_lte)

          elif search_filter_gte:
               self.queryset=self.queryset.filter(dateAssigntion__gte=search_filter_gte)

          search_filter = self.request.GET.get('search_filter_eleve') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(eleve__pk=search_filter))
          
          search_filter = self.request.GET.get('search_filter_bus') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(bus__pk=search_filter))

          search_filter = self.request.GET.get('search_filter_itineraire') or ''
          if search_filter:
               self.queryset=self.queryset.filter(Q(itineraire__pk=search_filter))

          if search_query:
               self.queryset = self.queryset.filter(Q(pk__icontains=search_query)
)
          return super().list(request, *args, **kwargs)


     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               assignationitineraire=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.serializer_class(instance,data=request.data)
          serializer.is_valid()
          serializer = self.serializer_class(instance,data=request.data)
          if serializer.is_valid():
               assignationitineraire=serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          errors=serializer.errors
          return Response(errors, status=status.HTTP_400_BAD_REQUEST)


