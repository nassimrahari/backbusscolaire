from typing import Any

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User=get_user_model()

from .models import ( AnneeInscription, Chauffeur, EcoleAssignation , TypeVehicule , Bus ,
                      LieuLigne , Ligne , LieuRamassage , OrdreLieu , Ecole ,
                        Classe , Parent , Eleve , Itineraire , Horaire , Inscription,
                        BusAssignation , AssignationItineraire ,)
class ChauffeurMinSerializer(serializers.ModelSerializer):
     class Meta:
          model = Chauffeur
          fields = ['pk','nom','prenoms','tel','email',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class TypeVehiculeMinSerializer(serializers.ModelSerializer):
     class Meta:
          model = TypeVehicule
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class BusMinSerializer(serializers.ModelSerializer):
     type=TypeVehiculeMinSerializer()
     chauffeur=ChauffeurMinSerializer()
     class Meta:
          model = Bus
          fields = ['pk','immatriculation','pk','type','pk','chauffeur','pk','couleur','pk','nbr_place',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class LieuLigneMinSerializer(serializers.ModelSerializer):
     class Meta:
          model = LieuLigne
          fields = ['pk','nom_lieu','pk','latitude','pk','longitude',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class LigneMinSerializer(serializers.ModelSerializer):
     class Meta:
          model = Ligne
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class LieuRamassageMinSerializer(serializers.ModelSerializer):
     ligne=LigneMinSerializer()
     lieu_ligne=LieuLigneMinSerializer()
     class Meta:
          model = LieuRamassage
          fields = ['pk','nom_lieu','pk','latitude','pk','longitude','pk','ligne','pk','lieu_ligne',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class OrdreLieuMinSerializer(serializers.ModelSerializer):
     ligne=LigneMinSerializer()
     lieu_ligne=LieuLigneMinSerializer()
     class Meta:
          model = OrdreLieu
          fields = ['pk','ligne','pk','lieu_ligne','pk','num_ordre',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class EcoleMinSerializer(serializers.ModelSerializer):
     class Meta:
          model = Ecole
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class ClasseMinSerializer(serializers.ModelSerializer):
     ecole=EcoleMinSerializer()
     class Meta:
          model = Classe
          fields = ['pk','nom','pk','ecole',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class ParentMinSerializer(serializers.ModelSerializer):
     class Meta:
          model = Parent
          fields = ['pk','nom_mere','pk','nom_pere','pk','tel_mere','pk','tel_pere','pk','email','pk','adresse',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class UserMinSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['pk','username','email','password','role']
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          ret['role'] = instance.role

          if instance.is_superuser:
               ret['role'] = "admin"

          return ret
          

class EleveMinSerializer(serializers.ModelSerializer):

     parent=ParentMinSerializer()
     ecole=EcoleMinSerializer()

     class Meta:
          model = Eleve
          fields = ['pk','date_naissance','image','nom','prenoms','adresse','parent','ecole']

     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)

          ret = super().to_representation(instance)
          inscriptions=Inscription.objects.filter(eleve__pk=instance.pk)

         

          ret['parent'] = str(instance.parent)
          ret['ecole'] = str(instance.ecole)
          
          if inscriptions.count():
               inscription=inscriptions.first()
               if inscription:
                    ret['classe'] = str(inscription.classe)
                    ret['date_inscription'] = str(inscription.date_inscription)
                    ret['lieu_ramassage'] =str(inscription.lieu_ramassage)
                    ret['lieu_remisage'] = str(inscription.lieu_remisage)



          return ret


class InscriptionMinSerializer(serializers.ModelSerializer):

     user=UserMinSerializer()

     classe=ClasseMinSerializer()
     eleve=EleveMinSerializer()

     class Meta:
          model = Inscription
          fields = ['pk','date_inscription','annee','eleve','user','ligne','classe','type_inscription','lieu_ramassage','lieu_remisage','montant_frais']
     
     def to_representation(self, instance):

          ret = super().to_representation(instance)

          ret['ligne'] = str(instance.ligne)
          ret['ecole'] = str(instance.eleve.ecole)
          ret['user'] = str(instance.user)
          ret['classe'] = str(instance.classe)
          ret['lieu_ramassage'] = str(instance.lieu_ramassage)
          ret['lieu_remisage'] = str(instance.lieu_remisage)
          ret['type_inscription'] = str(instance.type_inscription)
        
          return ret
     


class ItineraireMinSerializer(serializers.ModelSerializer):

     ligne=LigneMinSerializer()
     class Meta:
          model = Itineraire
          fields = ['pk','date_itineraire','pk','ligne','pk','ligne_inverse',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          horaires = instance.horaire_set.all()
          ret['horaires'] =HoraireMinMinSerializer(horaires, many=True).data
          return ret

class HoraireMinSerializer(serializers.ModelSerializer):
     pointArret=LieuLigneMinSerializer()
     itineraire=ItineraireMinSerializer()
     class Meta:
          model = Horaire
          fields = ['pk','pointArret','pk','itineraire','pk','heureDebut','pk','heureFin',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class EcoleAssignationMinSerializer(serializers.ModelSerializer):
     itineraire=ItineraireMinSerializer()
     ecole=EcoleMinSerializer()
     class Meta:
          model = EcoleAssignation
          fields = ['pk','date_assignation','pk','itineraire','pk','ecole',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class BusAssignationMinSerializer(serializers.ModelSerializer):
     bus=BusMinSerializer()
     itineraire=ItineraireMinSerializer()
     class Meta:
          model = BusAssignation
          fields = ['pk','date_assignation','pk','bus','pk','itineraire',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class AssignationItineraireMinSerializer(serializers.ModelSerializer):
     inscription=InscriptionMinSerializer()
     bus=BusMinSerializer()
     itineraire=ItineraireMinSerializer()
     class Meta:
          model = AssignationItineraire
          fields = ['pk','dateAssigntion','inscription','bus','itineraire',]

     def to_representation(self, instance:AssignationItineraire):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          
          ret['eleve'] = EleveMinSerializer(instance.inscription.eleve).data

          # ret['parent'] = str(instance.inscription.eleve.parent)
          # ret['ecole'] = str(instance.inscription.eleve.ecole)
          
 
         
         
          return ret



class ChauffeurSerializer(serializers.ModelSerializer):
     class Meta:
          model = Chauffeur
          fields = ['pk','nom','pk','prenoms','pk','tel','pk','email',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'buss' in special_details:
                    buss = instance.bus_set.all()
                    ret['buss'] =BusMinSerializer(buss, many=True).data
          ret['repr'] = str(instance)
          return ret

class TypeVehiculeSerializer(serializers.ModelSerializer):
     class Meta:
          model = TypeVehicule
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'buss' in special_details:
                    buss = instance.bus_set.all()
                    ret['buss'] =BusMinSerializer(buss, many=True).data
          ret['repr'] = str(instance)
          return ret

class BusSerializer(serializers.ModelSerializer):
     class Meta:
          model = Bus
          fields = ['pk','immatriculation','pk','type','pk','chauffeur','pk','couleur','pk','nbr_place',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['type'] = str(instance.type)
          ret['chauffeur'] = str(instance.chauffeur)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'busassignations' in special_details:
                    busassignations = instance.busassignation_set.all()
                    ret['busassignations'] =BusAssignationMinSerializer(busassignations, many=True).data
          ret['repr'] = str(instance)
          return ret

class LieuLigneSerializer(serializers.ModelSerializer):
     class Meta:
          model = LieuLigne
          fields = ['pk','nom_lieu','pk','latitude','pk','longitude',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'lieuramassages' in special_details:
                    lieuramassages = instance.lieuramassage_set.all()
                    ret['lieuramassages'] =LieuRamassageMinSerializer(lieuramassages, many=True).data
               if 'ordrelieus' in special_details:
                    ordrelieus = instance.ordrelieu_set.all()
                    ret['ordrelieus'] =OrdreLieuMinSerializer(ordrelieus, many=True).data
               if 'horaires' in special_details:
                    horaires = instance.horaire_set.all()
                    ret['horaires'] =HoraireMinSerializer(horaires, many=True).data
          ret['repr'] = str(instance)
          return ret

class LigneSerializer(serializers.ModelSerializer):
     class Meta:
          model = Ligne
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'lieuramassages' in special_details:
                    lieuramassages = instance.lieuramassage_set.all()
                    ret['lieuramassages'] =LieuRamassageMinSerializer(lieuramassages, many=True).data
               if 'ordrelieus' in special_details:
                    ordrelieus = instance.ordrelieu_set.all()
                    ret['ordrelieus'] =OrdreLieuMinSerializer(ordrelieus, many=True).data
               if 'eleves' in special_details:
                    eleves = instance.eleve_set.all()
                    ret['eleves'] =EleveMinSerializer(eleves, many=True).data
               if 'itineraires' in special_details:
                    itineraires = instance.itineraire_set.all()
                    ret['itineraires'] =ItineraireMinSerializer(itineraires, many=True).data
          ret['repr'] = str(instance)
          return ret

class LieuRamassageSerializer(serializers.ModelSerializer):
     class Meta:
          model = LieuRamassage
          fields = ['pk','nom_lieu','pk','latitude','pk','longitude','pk','ligne','pk','lieu_ligne',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['ligne'] = str(instance.ligne)
          ret['lieu_ligne'] = str(instance.lieu_ligne)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'eleves' in special_details:
                    eleves = instance.eleve_set.all()
                    ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          ret['repr'] = str(instance)
          return ret

class OrdreLieuSerializer(serializers.ModelSerializer):
     class Meta:
          model = OrdreLieu
          fields = ['pk','ligne','pk','lieu_ligne','pk','num_ordre',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['ligne'] = str(instance.ligne)
          ret['lieu_ligne'] = str(instance.lieu_ligne)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
          ret['repr'] = str(instance)
          return ret

class EcoleSerializer(serializers.ModelSerializer):
     class Meta:
          model = Ecole
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               print(special_detail_manytoone_class)
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'classes' in special_details:
                    classes = instance.classe_set.all()
                    ret['classes'] =ClasseMinSerializer(classes, many=True).data
               if 'eleves' in special_details:
                    eleves = instance.eleve_set.all()
                    ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          ret['repr'] = str(instance)
          return ret

class ClasseSerializer(serializers.ModelSerializer):
     class Meta:
          model = Classe
          fields = ['pk','nom','pk','ecole',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['ecole'] = str(instance.ecole)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'eleves' in special_details:
                    eleves = instance.eleve_set.all()
                    ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          ret['repr'] = str(instance)
          return ret

class ParentSerializer(serializers.ModelSerializer):
     class Meta:
          model = Parent
          fields = ['pk','nom_mere','pk','nom_pere','pk','tel_mere','pk','tel_pere','pk','email','pk','adresse',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'eleves' in special_details:
                    eleves = instance.eleve_set.all()
                    ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          ret['repr'] = str(instance)
          return ret


class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['pk','username','email','password',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          request = self.context.get('request')
          special_details=None

          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass

          if type(special_details) is list:
               pass
               if 'eleves' in special_details:
                    eleves = instance.eleve_set.all()
                    ret['eleves'] =EleveMinSerializer(eleves, many=True).data

          ret['repr'] = str(instance)
          ret['role'] = instance.role

          if instance.is_superuser:
               ret['role'] = "admin"

          return ret

class EleveSerializer(serializers.ModelSerializer):
     image = Base64ImageField(required=False)
     parent=ParentMinSerializer()
     ecole=EcoleMinSerializer()
     class Meta:
          model = Eleve
          fields = ['pk','date_naissance','image','nom','prenoms','adresse','parent','ecole']
     
     def to_representation(self, instance):

          ret = super().to_representation(instance)
          inscriptions=Inscription.objects.filter(eleve__pk=instance.pk)

         

          # ret['parent'] = str(instance.parent)
          # ret['ecole'] = str(instance.ecole)
          
          if inscriptions.count():
               inscription=inscriptions.first()
               if inscription:
                    ret['classe'] = str(inscription.classe)
                    ret['date_inscription'] = str(inscription.date_inscription)
                    ret['lieu_ramassage'] =str(inscription.lieu_ramassage)
                    ret['lieu_remisage'] = str(inscription.lieu_remisage)


          ret['repr'] = str(instance)
          return ret

class AnneeInscriptionSerializer(serializers.ModelSerializer):

     class Meta:
          model = AnneeInscription
          fields = ['pk','annee']

class InscriptionSerializer(serializers.ModelSerializer):
     eleve=EleveSerializer()

     class Meta:
          model = Inscription
          fields = ['pk','etat','date_inscription','annee','eleve','user','ligne','classe','type_inscription','lieu_ramassage','lieu_remisage','montant_frais']
     
     def to_representation(self, instance):

          ret = super().to_representation(instance)

          ret['ligne'] = str(instance.ligne)
          ret['ecole'] = str(instance.eleve.ecole)
          ret['user'] = str(instance.user)
          ret['classe'] = str(instance.classe)
          ret['lieu_ramassage'] = str(instance.lieu_ramassage)
          ret['lieu_remisage'] = str(instance.lieu_remisage)
          ret['type_inscription'] = str(instance.type_inscription)
          ret['repr'] = str(instance)

          request = self.context.get('request')
          special_details=None

          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass

          if type(special_details) is list:
               pass
               if 'assignationitineraires' in special_details:
                    assignationitineraires = instance.assignationitineraire_set.all()
                    ret['assignationitineraires'] =AssignationItineraireMinSerializer(assignationitineraires, many=True).data
         
               # if 'assignationitineraires' in special_details:
               #      assignationitineraires = instance.assignationitineraire_set.all()
               #      ret['assignationitineraires'] =AssignationItineraireMinSerializer(assignationitineraires, many=True).data

           

          return ret

class ItineraireSerializer(serializers.ModelSerializer):
     class Meta:
          model = Itineraire
          fields = ['pk','date_itineraire','pk','ligne','pk','ligne_inverse',]

     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['ligne'] = str(instance.ligne)
          request = self.context.get('request')
          special_details=None

          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
               if 'horaires' in special_details:
                    horaires = instance.horaire_set.all()
                    ret['horaires'] =HoraireMinSerializer(horaires, many=True).data

               if 'busassignations' in special_details:
                    busassignations = instance.busassignation_set.all()
                    ret['busassignations'] =BusAssignationMinSerializer(busassignations, many=True).data
               
               if 'ecoleassignations' in special_details:
                    ecoleassignations = instance.ecoleassignation_set.all()
                    ret['ecoleassignations'] =EcoleAssignationMinSerializer(ecoleassignations, many=True).data

               if 'assignationitineraires' in special_details:
                    assignationitineraires = instance.assignationitineraire_set.all()
                    ret['assignationitineraires'] =AssignationItineraireMinSerializer(assignationitineraires, many=True).data
          ret['repr'] = str(instance)
          return ret

class HoraireSerializer(serializers.ModelSerializer):
     class Meta:
          model = Horaire
          fields = ['pk','pointArret','pk','itineraire','pk','heureDebut','pk','heureFin',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['pointArret'] = str(instance.pointArret)
          ret['itineraire'] = str(instance.itineraire)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
          ret['repr'] = str(instance)
          return ret
     


class EcoleAssignationSerializer(serializers.ModelSerializer):
     class Meta:
          model = EcoleAssignation
          fields = ['pk','date_assignation','pk','itineraire','pk','ecole',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['itineraire'] = str(instance.itineraire)
          ret['ecole'] = str(instance.ecole)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
          ret['repr'] = str(instance)
          return ret


class BusAssignationSerializer(serializers.ModelSerializer):
     class Meta:
          model = BusAssignation
          fields = ['pk','date_assignation','pk','bus','pk','itineraire',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['bus'] = str(instance.bus)
          ret['itineraire'] = str(instance.itineraire)
          request = self.context.get('request')
          special_details=None
          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
          ret['repr'] = str(instance)
          return ret

class AssignationItineraireSerializer(serializers.ModelSerializer):
     class Meta:
          model = AssignationItineraire
          fields = ['pk','dateAssigntion','inscription','bus','itineraire',]

     def to_representation(self, instance):
          ret = super().to_representation(instance)

          ret['inscription'] = str(instance.inscription)
          ret['itineraire'] = str(instance.itineraire)
          ret['bus'] = str(instance.bus)

          request = self.context.get('request')
          special_details=None

          try:
               special_detail_manytoone_class=request.query_params.get('special_detail_manytoone_class', '')
               special_details=eval(special_detail_manytoone_class)
          except:
               pass
          if type(special_details) is list:
               pass
          ret['repr'] = str(instance)
          return ret



class ChauffeurDetailSerializer(serializers.ModelSerializer):
     class Meta:
          model = Chauffeur
          fields = ['pk','nom','pk','prenoms','pk','tel','pk','email',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          buss = instance.bus_set.all()
          ret['buss'] =BusMinSerializer(buss, many=True).data
          return ret

class TypeVehiculeDetailSerializer(serializers.ModelSerializer):
     class Meta:
          model = TypeVehicule
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          buss = instance.bus_set.all()
          ret['buss'] =BusMinSerializer(buss, many=True).data
          return ret

class BusDetailSerializer(serializers.ModelSerializer):
     type=TypeVehiculeMinSerializer()
     chauffeur=ChauffeurMinSerializer()
     class Meta:
          model = Bus
          fields = ['pk','immatriculation','pk','type','pk','chauffeur','pk','couleur','pk','nbr_place',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          busassignations = instance.busassignation_set.all()
          ret['busassignations'] =BusAssignationMinSerializer(busassignations, many=True).data
          return ret


class HoraireMinMinSerializer(serializers.ModelSerializer):
     pointArret=LieuLigneMinSerializer()
     class Meta:
          model = Horaire
          fields = ['pk','pointArret','pk','itineraire','pk','heureDebut','pk','heureFin',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret
     
class LieuLigneDetailSerializer(serializers.ModelSerializer):
     class Meta:
          model = LieuLigne
          fields = ['pk','nom_lieu','pk','latitude','pk','longitude',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          lieuramassages = instance.lieuramassage_set.all()
          ret['lieuramassages'] =LieuRamassageMinSerializer(lieuramassages, many=True).data
          ordrelieus = instance.ordrelieu_set.all()
          ret['ordrelieus'] =OrdreLieuMinSerializer(ordrelieus, many=True).data
          horaires = instance.horaire_set.all()
          ret['horaires'] =HoraireMinSerializer(horaires, many=True).data
          return ret

class LigneDetailSerializer(serializers.ModelSerializer):
     class Meta:
          model = Ligne
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)

          lieuramassages = instance.lieuramassage_set.all()
          ret['lieuramassages'] =LieuRamassageMinSerializer(lieuramassages, many=True).data
          ordrelieus = instance.ordrelieu_set.all()
          ret['ordrelieus'] =OrdreLieuMinSerializer(ordrelieus, many=True).data
          inscriptions = instance.inscription_set.all()
          ret['inscriptions'] =InscriptionMinSerializer(inscriptions, many=True).data
          itineraires = instance.itineraire_set.all()
          ret['itineraires'] =ItineraireMinSerializer(itineraires, many=True).data
          return ret

class LieuRamassageDetailSerializer(serializers.ModelSerializer):
     ligne=LigneMinSerializer()
     lieu_ligne=LieuLigneMinSerializer()
     class Meta:
          model = LieuRamassage
          fields = ['pk','nom_lieu','pk','latitude','pk','longitude','pk','ligne','pk','lieu_ligne',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          eleves = instance.eleve_set.all()
          ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          return ret

class OrdreLieuDetailSerializer(serializers.ModelSerializer):
     ligne=LigneMinSerializer()
     lieu_ligne=LieuLigneMinSerializer()
     class Meta:
          model = OrdreLieu
          fields = ['pk','ligne','pk','lieu_ligne','pk','num_ordre',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class EcoleDetailSerializer(serializers.ModelSerializer):
     class Meta:
          model = Ecole
          fields = ['pk','nom',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          classes = instance.classe_set.all()
          ret['classes'] =ClasseMinSerializer(classes, many=True).data
          eleves = instance.eleve_set.all()
          ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          return ret

class ClasseDetailSerializer(serializers.ModelSerializer):
     ecole=EcoleMinSerializer()
     class Meta:
          model = Classe
          fields = ['pk','nom','pk','ecole',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          eleves = instance.eleve_set.all()
          ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          return ret

class ParentDetailSerializer(serializers.ModelSerializer):
     class Meta:
          model = Parent
          fields = ['pk','nom_mere','pk','nom_pere','pk','tel_mere','pk','tel_pere','pk','email','pk','adresse',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          eleves = instance.eleve_set.all()
          ret['eleves'] =EleveMinSerializer(eleves, many=True).data
          return ret

class EleveDetailSerializer(serializers.ModelSerializer):

     image = Base64ImageField(required=False)
     parent=ParentMinSerializer()

     ecole=EcoleMinSerializer()



     class Meta:
          model = Eleve
          fields = ['pk','date_naissance','image','nom','prenoms','adresse','parent','ecole']

     def to_representation(self, instance):

          ret = super().to_representation(instance)
          inscriptions=Inscription.objects.filter(eleve__pk=instance.pk)

          # ret['parent'] = str(instance.parent)
          # ret['ecole'] = str(instance.ecole)
          
          if inscriptions.count():
               inscription=inscriptions.first()
               if inscription:
                    assignationitineraires = inscription.assignationitineraire_set.all()
                    ret['assignationitineraires'] =AssignationItineraireMinSerializer(assignationitineraires, many=True).data
                    ret['user'] = UserMinSerializer(inscription.user).data
                    ret['classe'] = ClasseMinSerializer(inscription.classe).data     
                    ret['date_inscription'] = str(inscription.date_inscription)
                    ret['lieu_ramassage'] =LieuRamassageMinSerializer(inscription.lieu_ramassage).data
                    ret['lieu_remisage'] = LieuRamassageMinSerializer(inscription.lieu_remisage).data
                    ret['ligne'] = LigneMinSerializer(inscription.ligne).data



          ret['repr'] = str(instance)
          return ret

class InscriptionDetailSerializer(serializers.ModelSerializer):


     user=UserMinSerializer()

     classe=ClasseMinSerializer()
     eleve=EleveSerializer()
     lieu_ramassage=LieuRamassageMinSerializer()
     lieu_remisage=LieuRamassageMinSerializer()
     ligne=LigneMinSerializer()

     class Meta:
          model = Inscription
          fields = ['pk','etat','date_inscription','annee','eleve','user','ligne','classe','type_inscription','lieu_ramassage','lieu_remisage','montant_frais']
     
     def to_representation(self, instance):

          ret = super().to_representation(instance)

          # ret['ligne'] = str(instance.ligne)
          ret['ecole'] = EcoleMinSerializer(instance.eleve.ecole).data
          # ret['user'] = str(instance.user)
          # ret['classe'] = str(instance.classe)
          # ret['lieu_ramassage'] = str(instance.lieu_ramassage)
          # ret['lieu_remisage'] = str(instance.lieu_remisage)
          # ret['type_inscription'] = str(instance.type_inscription)
          ret['repr'] = str(instance)
          assignationitineraires = instance.assignationitineraire_set.all()
          ret['assignationitineraires'] =AssignationItineraireMinSerializer(assignationitineraires, many=True).data
          
          return ret


# class InscriptionDetailSerializer(serializers.ModelSerializer):


#      user=UserMinSerializer()

#      classe=ClasseMinSerializer()

#      class Meta:
#           model = Eleve
#           fields = ['pk','user','classe','montant_frais',]
    
#      def to_representation(self, instance):
#           ret = super().to_representation(instance)
#           ret['repr'] = str(instance)
#           assignationitineraires = instance.assignationitineraire_set.all()
#           ret['assignationitineraires'] =AssignationItineraireMinSerializer(assignationitineraires, many=True).data
#           return ret
     
class ItineraireDetailSerializer(serializers.ModelSerializer):
     ligne=LigneMinSerializer()
     class Meta:
          model = Itineraire
          fields = ['pk','date_itineraire','pk','ligne','pk','ligne_inverse',]
          
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          horaires = instance.horaire_set.all()
          ret['horaires'] =HoraireMinSerializer(horaires, many=True).data
          busassignations = instance.busassignation_set.all()
          ret['busassignations'] =BusAssignationMinSerializer(busassignations, many=True).data


          ecoleassignations = instance.ecoleassignation_set.all()
          ret['ecoleassignations'] =EcoleAssignationMinSerializer(ecoleassignations, many=True).data

          assignationitineraires = instance.assignationitineraire_set.all()
          ret['assignationitineraires'] =AssignationItineraireMinSerializer(assignationitineraires, many=True).data
          return ret

class HoraireDetailSerializer(serializers.ModelSerializer):
     pointArret=LieuLigneMinSerializer()
     itineraire=ItineraireMinSerializer()
     class Meta:
          model = Horaire
          fields = ['pk','pointArret','pk','itineraire','pk','heureDebut','pk','heureFin',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class EcoleAssignationDetailSerializer(serializers.ModelSerializer):
     itineraire=ItineraireMinSerializer()
     ecole=EcoleMinSerializer()
     class Meta:
          model = EcoleAssignation
          fields = ['pk','date_assignation','pk','itineraire','pk','ecole',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret


class BusAssignationDetailSerializer(serializers.ModelSerializer):
     bus=BusMinSerializer()
     itineraire=ItineraireMinSerializer()
     class Meta:
          model = BusAssignation
          fields = ['pk','date_assignation','pk','bus','pk','itineraire',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

class AssignationItineraireDetailSerializer(serializers.ModelSerializer):
     inscription=InscriptionMinSerializer()
     itineraire=ItineraireMinSerializer()

     class Meta:
          model = AssignationItineraire
          fields = ['pk','dateAssigntion','inscription','bus','itineraire',]
     def to_representation(self, instance):
          ret = super().to_representation(instance)
          ret['repr'] = str(instance)
          return ret

