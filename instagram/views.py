from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .core.instagram_service import InstagramService
from .models import InstagramAccount

@api_view(['POST'])
def add_instagram_account(request):
    # Récupérer les données de la requête
    username = request.data.get('username')
    password = request.data.get('password')
    otp = request.data.get('otp')  # Le code OTP pour 2FA, si nécessaire

    # Vérifier si les données nécessaires sont présentes
    if not username or not password:
        return JsonResponse({"error": "Le nom d'utilisateur et le mot de passe sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

    instagram_service = InstagramService()
    
    try:
        account_data = instagram_service.authenticate(username, password, otp)
        
        # # Si la connexion est réussie, ajouter le compte à la base de données
        # account = InstagramAccount.objects.create(
        #     name=account_data['username'],
        #     profile_picture=account_data['profile_picture'],
        #     bio=account_data['bio'],
        #     bio_link=account_data['bio_link'],
        # )

        # Retourner une réponse indiquant que le compte a été ajouté avec succès
        return JsonResponse({"message": "Compte ajouté avec succès!"}, status=status.HTTP_201_CREATED)
    
    except ValueError as e:
        # Retourner une erreur si la connexion échoue
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
