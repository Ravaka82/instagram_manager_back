from instagrapi import Client
from instagrapi.exceptions import ClientError, TwoFactorRequired

class InstagramService:
    def __init__(self):
        self.client = Client()

    def authenticate(self, username, password, otp=None):
        try:
            print(f"Tentative de récupérer les informations pour l'utilisateur : {username}")
            if otp:
                print("Étape : Connexion avec OTP")
                # Connexion avec mot de passe et OTP
                login_response = self.client.login(username, password, verification_code=otp)
                if not login_response:
                    raise ValueError("Échec de la connexion avec le code OTP")
            else:
                print("Étape : Connexion normale")
                self.client.login(username, password)

            user_info = self.client.account_info()
            print(f"Informations de l'utilisateur récupérées avec succès : {user_info}")

            return {
                "username": user_info.username,
                "profile_picture": str(user_info.profile_pic_url),
                "bio": user_info.biography,
                "bio_link": str(user_info.external_url) if user_info.external_url else None,
            }

        except TwoFactorRequired:
            print("Erreur : Code OTP requis ou incorrect.")
            raise ValueError("Code OTP requis ou incorrect.")
        except ClientError:
            print("Erreur : Nom d'utilisateur ou mot de passe incorrect.")
            raise ValueError("Nom d'utilisateur ou mot de passe incorrect.")
        except Exception as e:
            print(f"Erreur générale : {e}")
            raise ValueError(f"{e}")
