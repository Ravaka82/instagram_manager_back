from instagrapi import Client
from instagrapi.exceptions import ClientError, TwoFactorRequired

class InstagramService:
    def _init_(self):
        self.client = Client()

    def authenticate(self, username, password, otp=None):
        try:
            if otp:
                # Si OTP est fourni, effectuer la connexion avec le code
                login_response = self.client.login(username, password, verification_code=otp)
                if not login_response:
                    raise ValueError("Code OTP incorrect ou échec d'authentification.")
            else:
                # Sinon, effectuer une connexion normale
                self.client.login(username, password)

            # Récupérer les informations utilisateur après connexion réussie
            user_info = self.client.account_info()

            return {
                "username": user_info.username,
                "profile_picture": str(user_info.profile_pic_url),
                "bio": user_info.biography,
                "bio_link": str(user_info.external_url) if user_info.external_url else None,
                "is_authenticated": True,
            }
        except TwoFactorRequired:
            # Gérer l'erreur si 2FA est requis mais non fourni ou incorrect
            raise ValueError("Code OTP requis ou incorrect pour l'authentification.")
        except ClientError as e:
            # Gérer les erreurs de connexion comme nom d'utilisateur ou mot de passe incorrect
            raise ValueError(f"Erreur de connexion avec Instagram : {e}")
        except Exception as e:
            # Gérer toute autre erreur généralesss
            raise ValueError(f"Erreur générale lors de l'authentification  : {e}")