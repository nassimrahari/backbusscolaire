from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model

User=get_user_model()
    
class Chauffeur(models.Model):
     nom = models.CharField(max_length=50,)
     prenoms = models.CharField(max_length=50,)
     tel = models.CharField(max_length=50,)
     email = models.CharField(max_length=50,)
     def __str__(self) -> str:
          return f"{self.pk} {self.nom} {self.prenoms}"
          

class TypeVehicule(models.Model):
     nom = models.CharField(max_length=50,verbose_name="Nom Type Vehicule",)
     def __str__(self) -> str:
          return f"{self.id} {self.nom}"
          

class Bus(models.Model):
     immatriculation = models.CharField(max_length=50, null=False,verbose_name="Immatruculation",)
     type = models.ForeignKey(TypeVehicule, on_delete=models.CASCADE,)
     chauffeur = models.ForeignKey('Chauffeur', on_delete=models.SET_NULL, null=True,)
     couleur = models.CharField(max_length=50, null=True,blank=False,)
     nbr_place = models.IntegerField()
     def __str__(self) -> str:
          return f"{self.immatriculation}"
          
          
          

class LieuLigne(models.Model):
     nom_lieu = models.CharField(max_length=50,)
     latitude = models.CharField(max_length=50,default="-18.881589691375204",blank=False,)
     longitude = models.CharField(max_length=50,default="47.50664234161377",null=True,blank=False,)
     def __str__(self):
          return f"{self.id} {self.nom_lieu}"
          
          

class Ligne(models.Model):
     nom = models.CharField(max_length=50,)
     def __str__(self):
          return f"{self.nom}"
          
          

class LieuRamassage(models.Model):
     nom_lieu = models.CharField(max_length=50,)
     latitude = models.CharField(max_length=50,default="-18.881589691375204",blank=False,null=True,)
     longitude = models.CharField(max_length=50,default="47.50664234161377",null=True,blank=False,)
     ligne = models.ForeignKey("Ligne",null=True,on_delete=models.CASCADE,)
     lieu_ligne = models.ForeignKey("LieuLigne",null=True,on_delete=models.CASCADE,)
     def __str__(self):
          return f"{self.id} {self.nom_lieu}"
          
          
          
          

class OrdreLieu(models.Model):
     ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE,)
     lieu_ligne = models.ForeignKey(LieuLigne, on_delete=models.CASCADE,)
     num_ordre = models.IntegerField()

class Ecole(models.Model):
     nom = models.CharField(max_length=150,unique=True,)
     def __str__(self):
          return f"{self.pk} | {self.nom}"
          
          # Create your models here.

class Classe(models.Model):
     nom = models.CharField(max_length=50,unique=True,)
     ecole = models.ForeignKey(Ecole,on_delete=models.CASCADE,null=True,)
     def __str__(self):
          return f"{self.pk} | {self.nom}"
          
          
          
          # Create your models here.

class Parent(models.Model):
     nom_mere = models.CharField(max_length=50,null=True,blank=False,)
     nom_pere = models.CharField(max_length=50,null=True,blank=False,)
     tel_mere = models.CharField(max_length=50,null=True,blank=False,)
     tel_pere = models.CharField(max_length=50,null=True,blank=False,)
     email = models.EmailField(null=True,unique=True,)
     adresse = models.CharField(max_length=50,null=True,blank=False,)
     def __str__(self):
          return f"{self.pk} {self.nom_mere} | {self.nom_pere}"
          
          
          # Create your models here.

class Eleve(models.Model):
     date_inscription = models.DateField(default=datetime.date.today,)
     date_naissance = models.DateField(null=True,)
     image = models.ImageField(null=True,)
     nom = models.CharField(max_length=100,)
     prenoms = models.CharField(max_length=100,)
     adresse = models.CharField(max_length=100,)
     ligne = models.ForeignKey(Ligne, on_delete=models.SET_NULL,null=True,blank=False,)
     parent = models.ForeignKey(Parent, on_delete=models.SET_NULL,null=True,blank=False,)
     ecole = models.ForeignKey(Ecole, on_delete=models.SET_NULL,null=True,blank=False,)
     classe = models.ForeignKey(Classe, on_delete=models.SET_NULL,null=True,blank=False,)
     lieu_ramassage = models.ForeignKey(LieuRamassage, on_delete=models.SET_NULL,verbose_name="lieu de ramassage",null=True,blank=False,)
     montant_frais = models.DecimalField(max_length=50,decimal_places=2,max_digits=10,null=True,blank=True,)
     etat = models.CharField(max_length=50,default="en_attente",)
     user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

     
     def __str__(self):
          return self.nom
          

class Itineraire(models.Model):
     date_itineraire = models.DateField(null=True, default=datetime.date.today,)
     ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE,)
     ligne_inverse = models.BooleanField(default=False,)

class Horaire(models.Model):
     pointArret = models.ForeignKey('LieuLigne',on_delete=models.CASCADE,)
     itineraire = models.ForeignKey('Itineraire',on_delete=models.CASCADE,)
     heureDebut = models.TimeField()
     heureFin = models.TimeField()

class BusAssignation(models.Model):
     date_assignation = models.DateField(default=timezone.now,)
     bus = models.ForeignKey(Bus,on_delete=models.CASCADE,)
     itineraire = models.ForeignKey("Itineraire",on_delete=models.CASCADE,)
     def __str__(self):
          return f"ItinÃ©raire NÂ° {self.pk}"
          
          
          

class AssignationItineraire(models.Model):
     dateAssigntion = models.DateField(default=timezone.now,)
     eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE,null=True,blank=False,)
     itineraire = models.ForeignKey('Itineraire', on_delete=models.CASCADE,null=True,blank=False,)

