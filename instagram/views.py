from django.http import JsonResponse
from rest_framework.decorators import api_view
from instagram.core.instagram_service import InstagramService
from rest_framework import status
from instagram.models import InstagramUser


@api_view(['POST'])
def register_instagram_user(request):
    username = request.data.get('username')
    password = request.data.get('password')  # Le mot de passe est requis
    otp = request.data.get('otp')  # OTP est facultatif

    if not username:
        return JsonResponse({"error": "Nom d'utilisateur est requis."}, status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return JsonResponse({"error": "Le mot de passe est requis."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        instagram_service = InstagramService()
        user_info = instagram_service.authenticate(username, password, otp)

        instagram_user, created = InstagramUser.objects.update_or_create(
            username=user_info["username"],  # Le nom d'utilisateur doit être unique
            defaults={
                "profile_picture": user_info.get("profile_picture"),
                "bio": user_info.get("bio"),
                "bio_link": user_info.get("bio_link"),
            }
        )

        return JsonResponse({
            "username": instagram_user.username,
            "profile_picture": instagram_user.profile_picture,
            "bio": instagram_user.bio,
            "bio_link": instagram_user.bio_link,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": f"Une erreur est survenue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_instagram_user(request):
    try:
        instagram_service = InstagramService()
        users_data = instagram_service.get_all_count()

        return JsonResponse({
            "users": users_data  
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": f"Une erreur est survenue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
