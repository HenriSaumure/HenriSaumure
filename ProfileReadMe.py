import requests
import random
import re
from datetime import datetime
import os
from github import Github

# Configuration pour les tests locaux et GitHub Actions
def get_github_token():
    """Récupère le token GitHub depuis l'environnement ou utilise un token de test"""
    # 1. Essayer de récupérer depuis la variable d'environnement (pour GitHub Actions)
    token = os.environ.get("GITHUB_TOKEN")
    
    # 2. Si pas de token dans l'environnement, utiliser un token codé en dur pour les tests
    # ATTENTION: Ce token devrait être retiré avant de pousser le code dans un dépôt
    if not token:
        # POUR LES TESTS UNIQUEMENT - À SUPPRIMER AVANT DE POUSSER SUR GITHUB
        token = "Github_Token" # Utilisez un nouveau token ici pour le test
    
    return token

# Informations utilisateur
GITHUB_USERNAME = "HenriSaumure"
REPOSITORY_NAME = "HenriSaumure"

def get_github_stats():
    """Obtenir les vraies statistiques GitHub en utilisant l'API"""
    try:
        # Obtenir le token
        token = get_github_token()
        if not token:
            raise Exception("Token GitHub non disponible")
            
        # Créer une instance Github avec le token
        g = Github(token)
        
        # Récupérer les informations de l'utilisateur
        user = g.get_user(GITHUB_USERNAME)
        
        # Récupérer les statistiques réelles
        stats = {
            'public_repos': user.public_repos,
            'followers': user.followers,
            'following': user.following,
            'name': user.name if user.name else GITHUB_USERNAME,
        }
        return stats
    except Exception as e:
        print(f"Erreur lors de la récupération des statistiques: {e}")
        # En cas d'erreur, utiliser des valeurs par défaut
        return {
            'public_repos': 0,
            'followers': 0,
            'following': 0,
            'name': GITHUB_USERNAME,
        }

def generate_phrase():
    """Générer une phrase aléatoire avec les vraies statistiques en français"""
    stats = get_github_stats()
    
    # Format de date conforme à votre exemple
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    phrases = [
        f"👋 Bonjour! Je possède {stats['public_repos']} dépôts publics et {stats['followers']} abonnés.",
        f"🚀 Je maintiens actuellement {stats['public_repos']} projets publics avec une communauté de {stats['followers']} abonnés formidables!",
        f"💻 Consultez mes {stats['public_repos']} dépôts si vous êtes intéressé par ce que je développe.",
        f"📊 Statistiques actuelles: {stats['public_repos']} dépôts publics, {stats['followers']} abonnés, {stats['following']} abonnements.",
        f"🌟 Merci aux {stats['followers']} personnes qui suivent mon travail sur mes {stats['public_repos']} projets!",
        f"📆 Aujourd'hui ({current_date}), je compte {stats['followers']} abonnés et {stats['public_repos']} projets.",
    ]
    
    return random.choice(phrases)

def update_readme():
    """Mettre à jour le README avec le nouveau contenu en utilisant l'API GitHub"""
    try:
        # Obtenir le token
        token = get_github_token()
        if not token:
            print("⚠️ Erreur: Token GitHub non disponible!")
            return
            
        # Connexion à GitHub
        g = Github(token)
        repo = g.get_repo(f"{GITHUB_USERNAME}/{REPOSITORY_NAME}")
        
        try:
            # Obtenir le contenu actuel du README
            contents = repo.get_contents("README.md")
            readme_content = contents.decoded_content.decode("utf-8")
        except:
            # Si le README n'existe pas encore, créer un contenu par défaut
            readme_content = f"""# Bienvenue sur mon profil!

<!-- SECTION_DYNAMIQUE_DEBUT -->
<!-- Cette section sera automatiquement mise à jour par le script -->
<!-- SECTION_DYNAMIQUE_FIN -->

## Mes Projets
N'hésitez pas à explorer mes dépôts pour découvrir mes projets!
"""
        
        # Générer le nouveau contenu
        new_phrase = generate_phrase()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Mettre à jour la section dynamique
        pattern = r"<!-- SECTION_DYNAMIQUE_DEBUT -->.*<!-- SECTION_DYNAMIQUE_FIN -->"
        replacement = f"<!-- SECTION_DYNAMIQUE_DEBUT -->\n{new_phrase}\n\n*Dernière mise à jour: {current_time}*\n<!-- SECTION_DYNAMIQUE_FIN -->"
        
        if re.search(pattern, readme_content, re.DOTALL):
            # Si les marqueurs existent, mettre à jour la section
            updated_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
        else:
            # Si les marqueurs n'existent pas, ajouter la section au début
            updated_content = f"""# Bienvenue sur mon profil!

{replacement}

## Mes Projets
N'hésitez pas à explorer mes dépôts pour découvrir mes projets!
"""
        
        # Vérifier si le README existe déjà
        try:
            # Mettre à jour le fichier existant
            repo.update_file(
                path="README.md",
                message="Mise à jour du README avec un nouveau contenu dynamique",
                content=updated_content,
                sha=contents.sha
            )
            print("✅ README mis à jour avec succès!")
        except:
            # Créer le fichier s'il n'existe pas
            repo.create_file(
                path="README.md",
                message="Création du README avec contenu dynamique",
                content=updated_content
            )
            print("✅ README créé avec succès!")
            
    except Exception as e:
        print(f"⚠️ Erreur lors de la mise à jour du README: {e}")

def preview_update():
    """Aperçu de la mise à jour sans toucher au dépôt"""
    phrase = generate_phrase()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    print("\n=== APERÇU DE LA MISE À JOUR ===")
    print(f"{phrase}")
    print(f"\nDernière mise à jour: {current_time}")
    print("===================================\n")

if __name__ == "__main__":
    # Si nous sommes dans GitHub Actions, mettre à jour le README
    if os.environ.get("GITHUB_ACTIONS") == "true":
        update_readme()
    else:
        # Sinon, afficher un aperçu et demander confirmation
        preview_update()
        response = input("Voulez-vous mettre à jour le README maintenant? (o/n): ")
        if response.lower() in ('o', 'oui', 'y', 'yes'):
            update_readme()
        else:
            print("Mise à jour annulée.")