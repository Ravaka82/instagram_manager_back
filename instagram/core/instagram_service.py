from instagrapi import Client
from instagrapi.exceptions import ClientError, TwoFactorRequired

class InstagramService:
    def __init__(self):
        self.client = Client()

    def authenticate(self, username, password, otp=None):
        try:
            print(f"Tentative d'authentification pour l'utilisateur : {username}")  # Debug
            if otp:
                print("Étape : Connexion avec OTP")  # Debug
                login_response = self.client.login(username, password, verification_code=otp)
                if not login_response:
                    print("Erreur : Code OTP incorrect ou échec d'authentification")  # Debug
                    raise ValueError("Code OTP incorrect ou échec d'authentification.")
            else:
                print("Étape : Connexion normale")  # Debug
                self.client.login(username, password)

            # Récupérer les informations utilisateur après connexion réussie
            user_info = self.client.account_info()
            print(f"Connexion réussie. Utilisateur connecté : {user_info.username}")  # Debug
            print(f"Informations de l'utilisateur : {user_info}")  # Debug

            return {
                "username": user_info.username,
                "profile_picture": str(user_info.profile_pic_url),
                "bio": user_info.biography,
                "bio_link": str(user_info.external_url) if user_info.external_url else None,
                "is_authenticated": True,
            }
        except TwoFactorRequired:
            print("Erreur : Code OTP requis ou incorrect pour l'authentification.")  # Debug
            raise ValueError("Code OTP requis ou incorrect pour l'authentification.")
        except ClientError as e:
            print(f"Erreur ClientError : {e}")  # Debug
            raise ValueError(f"Erreur de connexion avec Instagram : {e}")
        except Exception as e:
            print(f"Erreur générale : {e}")  # Debug
            raise ValueError(f"Erreur générale lors de l'authentification : {e}")
