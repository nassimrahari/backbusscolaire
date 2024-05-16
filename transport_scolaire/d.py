# Mettre à jour les ecoleassignations existants pour cette itineraire
               ecoleassignations_digits = [int(value['pk']) for value in request.data['ecoleassignations'] if value.get('pk',None)]
               EcoleAssignation.objects.filter(itineraire=itineraire).exclude(pk__in=ecoleassignations_digits).delete()
               for ecoleassignation in request.data['ecoleassignations']:
                    ecoleassignation['itineraire']=itineraire.pk
                    instance_ecoleassignation = EcoleAssignation.objects.filter(pk=ecoleassignation.get('pk',None)).first()
                    ecoleassignation_serializer=EcoleAssignationSerializer(instance_ecoleassignation,data=ecoleassignation)
                    if ecoleassignation_serializer.is_valid():
                         ecoleassignation_serializer.save()