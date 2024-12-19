from django.http import JsonResponse
from rest_framework.decorators import api_view
from instagram.core.instagram_service import InstagramService
from rest_framework import status

@api_view(['POST'])
def authenticate_instagram_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    otp = request.data.get('otp')  # OTP est facultatif

    # Vérification que le nom d'utilisateur et le mot de passe sont fournis
    if not username or not password:
        return JsonResponse({"error": "Nom d'utilisateur et mot de passe sont requis."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Créer une instance du service Instagram
        instagram_service = InstagramService()

        # Tentative de connexion via le service
        user_info = instagram_service.authenticate(username, password, otp)

        # Retourner les informations utilisateur en réponse
        return JsonResponse({
            "username": user_info["username"],
            "profile_picture": user_info["profile_picture"],
            "bio": user_info["bio"],
            "bio_link": user_info["bio_link"]
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        # En cas d'erreur d'authentification ou d'OTP
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Gérer toute autre exception
        return JsonResponse({"error": f"Une erreur est survenue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
