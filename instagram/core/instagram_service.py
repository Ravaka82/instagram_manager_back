import os
from instagrapi import Client
from instagrapi.exceptions import ClientError, TwoFactorRequired
from instagram.models import InstagramUser

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
                "is_master": False,
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
        
    def insert_count_master(self, username, profile_picture=None, bio=None, bio_link=None):
        try:
            # Vérifiez si un compte maître existe déjà
            if InstagramUser.objects.filter(is_master=True).exists():
                raise ValueError("Un compte maître existe déjà.")

            # Créez un compte maître en incluant les champs optionnels
            master_user = InstagramUser.objects.create(
                username=username,
                profile_picture=profile_picture,  # Enregistrer ici l'URL du fichier, pas le fichier lui-même
                bio=bio,                          # Peut être None
                bio_link=bio_link,                # Peut être None
                is_master=True,                 
            )

            print(f"Compte maître '{username}' inséré avec succès.")
            return {
                "message": "Compte maître inséré avec succès.",
                "username": master_user.username,
                "profile_picture": master_user.profile_picture,  # URL du fichier
                "bio": master_user.bio,
                "bio_link": master_user.bio_link,
                "is_master": master_user.is_master,
            }

        except Exception as e:
            print(f"Erreur lors de l'insertion du compte maître : {str(e)}")
            raise ValueError(f"Erreur lors de l'insertion du compte maître : {str(e)}")


    def get_all_count(self):
        try:
            instagram_users = InstagramUser.objects.all()
            user_data = []
            for user in instagram_users:
                user_data.append({
                    "username": user.username,
                    "profile_picture": user.profile_picture,
                    "bio": user.bio,
                    "bio_link": user.bio_link,
                     "is_master":False,
                })
            return user_data

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs Instagram : {str(e)}")
            raise ValueError(f"Erreur lors de la récupération des utilisateurs Instagram : {str(e)}")
        
    
    def update_user(self, username, password, new_full_name=None, new_bio=None, new_bio_link=None, new_profile_picture_path=None):
        try:
            print("🔑 Connexion à Instagram...")
            self.client.login(username, password)

            user_info = self.client.account_info()

            updated_name = new_full_name if new_full_name is not None else user_info.full_name
            updated_bio = new_bio if new_bio is not None else user_info.biography
            updated_bio_link = new_bio_link if new_bio_link is not None else user_info.external_url

            
            print("🛠️ Mise à jour des informations du profil Instagram...")
            self.client.account_edit(
                full_name=updated_name,
                biography=updated_bio,
                external_url=updated_bio_link
            )
            print("✅ Nom d'affichage, bio et lien mis à jour sur le compte réel Instagram.")


            if new_profile_picture_path:
                if os.path.exists(new_profile_picture_path):
                    print(f"📸 Changement de la photo de profil depuis : {new_profile_picture_path}")
                    result = self.client.account_change_picture(new_profile_picture_path)
                    if result:
                        print("✅ Photo de profil mise à jour avec succès.")
                    else:
                        raise ValueError("❌ Échec du changement de la photo de profil.")
                else:
                    raise FileNotFoundError(f"❌ Le fichier '{new_profile_picture_path}' est introuvable.")

            # 🔄 Récupération des informations mises à jour
            print("🔄 Récupération des nouvelles informations du compte Instagram...")
            updated_user_info = self.client.account_info()
            
            return {
                "username": updated_user_info.username,
                "name": updated_user_info.full_name,
                "profile_picture": str(updated_user_info.profile_pic_url),
                "bio": updated_user_info.biography,
                "bio_link": str(updated_user_info.external_url) if updated_user_info.external_url else None,
            }

        except FileNotFoundError as e:
            raise ValueError(str(e))
        except ClientError as e:
            raise ValueError(f"❌ Erreur Instagram : {e}")
        except Exception as e:
            raise ValueError(f"❌ Erreur inconnue : {e}")
