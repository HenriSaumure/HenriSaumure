import requests
import os
import sys
from playwright.sync_api import sync_playwright
import pytesseract
from PIL import Image
import re
from datetime import datetime
import base64
import random
from dateutil.relativedelta import relativedelta

# GitHub API settings
github_username = "HenriSaumure"
api_token = "Your_API_Token"
headers = {"Authorization": f"token {api_token}"}

# URL for screenshot
profile_url = f"https://github.com/{github_username}"

# Folder for screenshots
screenshots_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "screenshots")
if not os.path.exists(screenshots_folder):
    os.makedirs(screenshots_folder)

def get_github_profile_info():
    """Get GitHub profile information using the API"""
    base_url = "https://api.github.com"
    
    # Get user profile info
    user_url = f"{base_url}/users/{github_username}"
    user_response = requests.get(user_url, headers=headers)
    
    if user_response.status_code != 200:
        print(f"Error fetching profile: {user_response.status_code}")
        return None
    
    user_data = user_response.json()
    
    # Get repositories data
    repos_url = f"{base_url}/users/{github_username}/repos"
    repos_response = requests.get(repos_url, headers=headers)
    repos = []
    if repos_response.status_code == 200:
        repos = repos_response.json()
    
    # Get commit count via search API
    search_url = f"{base_url}/search/commits?q=author:{github_username}"
    search_headers = headers.copy()
    search_headers["Accept"] = "application/vnd.github.cloak-preview"
    
    search_response = requests.get(search_url, headers=search_headers)
    if search_response.status_code != 200:
        print(f"Error fetching commit count: {search_response.status_code}")
        commit_count = "Non disponible"
    else:
        commit_count = search_response.json().get("total_count", 0)
    
    return {
        "user": user_data,
        "repos": repos,
        "commit_count": commit_count
    }

def capture_screenshot(url, screenshot_path):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_timeout(5000)
            
            # Focus on the contributions section
            contribution_section = page.query_selector(".js-yearly-contributions")
            if contribution_section:
                contribution_section.screenshot(path=screenshot_path)
                return True
            else:
                page.screenshot(path=screenshot_path)
                return True
            
            browser.close()
    except Exception as e:
        print(f"Error capturing screenshot: {str(e)}")
        return False

def extract_contributions_count(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        # Look specifically for the contributions pattern
        pattern = r'(\d+)\s+contributions?\s+in\s+the\s+last\s+year'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1)  # Return just the number
        else:
            return "Non trouvé"
    except Exception as e:
        return f"Erreur d'extraction du texte: {str(e)}"

def get_random_coding_phrase():
    """Generate a random funny phrase about coding in French"""
    phrases = [
    "Le langage Rust permet une gestion de la mémoire sans garbage collection, minimisant les risques de fuites de mémoire.",
    "Les architectures serverless permettent de déployer des applications sans gérer de serveurs, réduisant ainsi la complexité et les coûts.",
    "CockroachDB est une base de données distribuée ultra-scalable, conçue pour résister aux pannes et garantir la haute disponibilité.",
    "TensorFlow 2.0 a simplifié le machine learning, avec un déploiement rapide sur des appareils mobiles et des systèmes embarqués.",
    "WebAssembly permet d'exécuter des langages compilés directement dans les navigateurs, offrant des performances presque natives pour le web.",
    "La blockchain est utilisée pour créer des contrats intelligents, éliminant les intermédiaires et rendant les transactions plus transparentes.",
    "Kubernetes est l'outil dominant pour orchestrer des containers Docker, rendant le déploiement d'applications microservices plus facile.",
    "La 5G permet des vitesses de téléchargement incroyablement rapides, ouvrant la voie à des applications IoT ultra-réactives.",
    "GitHub Actions simplifie les pipelines CI/CD, rendant l’intégration et le déploiement continu plus fluides.",
    "L'Edge computing réduit la latence en traitant les données à proximité de la source, idéal pour les applications en temps réel.",
    "Les microservices offrent une architecture modulaire permettant de déployer des fonctionnalités indépendantes sans impacter l'ensemble du système.",
    "La réalité augmentée permet d’interagir avec des objets virtuels en temps réel, modifiant les expériences dans des domaines comme l’éducation et la santé.",
    "Les assistants vocaux alimentés par l'IA, comme Alexa et Siri, utilisent des algorithmes de traitement du langage naturel pour mieux comprendre les utilisateurs.",
    "Les systèmes autonomes, comme les voitures sans conducteur, reposent sur des réseaux neuronaux pour comprendre et interpréter leur environnement.",
    "Les frameworks comme React et Vue.js permettent de créer des interfaces utilisateur dynamiques avec des mises à jour ultra-rapides.",
    "Les technologies de reconnaissance faciale permettent d'améliorer la sécurité des appareils et des applications bancaires.",
    "Le machine learning automatisé (AutoML) permet de générer des modèles de machine learning performants sans expertise approfondie en data science.",
    "Les bases de données NoSQL, comme Cassandra, sont conçues pour gérer des volumes massifs de données non structurées et pour être hautement scalables.",
    "Le cryptage quantique est une technologie en développement qui pourrait rendre les données inviolables face aux ordinateurs quantiques du futur.",
    "Les réseaux de neurones récurrents (RNN) sont utilisés dans la reconnaissance vocale et la traduction automatique, permettant des interactions plus naturelles.",
    "L'intelligence artificielle générative crée du contenu original, de l'art à la musique, en s'inspirant des données d'entraînement existantes.",
    "La réalité virtuelle (VR) immerge les utilisateurs dans des environnements simulés, souvent utilisée dans les simulations d’entraînement ou les jeux.",
    "Les robots collaboratifs (cobots) sont utilisés dans les usines pour travailler côte à côte avec les humains, améliorant l'efficacité de la production.",
    "L'informatique quantique promet de révolutionner le traitement des données, résolvant des problèmes complexes en quelques secondes là où les superordinateurs prennent des années.",
    "Les langages comme Go sont particulièrement conçus pour le développement d'applications cloud-native, optimisant la concurrence et la performance.",
    "Les solutions de cloud hybride permettent de combiner les avantages des clouds publics et privés, offrant une flexibilité maximale.",
    "Les modèles d'IA pour la vision par ordinateur peuvent détecter des anomalies dans des images médicales, accélérant le diagnostic des maladies.",
    "Les technologies de compression vidéo comme HEVC réduisent la taille des fichiers sans sacrifier la qualité, permettant un streaming plus rapide.",
    "Les plateformes de développement low-code permettent aux utilisateurs non techniques de créer des applications simples sans écrire de code."
]

    return random.choice(phrases)




def generate_readme(profile_data, contributions):
    """Generate the README.md content for the GitHub profile in French"""
    user = profile_data["user"]
    repos = profile_data["repos"]
    commit_count = profile_data["commit_count"]
    
    # Convert contributions to an integer (if it is a string)
    contributions = int(contributions) + 1

    # Format the dates
    created_at = datetime.strptime(user.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
    created_date = created_at.strftime('%d %B %Y').replace("January", "Janvier").replace("February", "Février").replace("March", "Mars").replace("April", "Avril").replace("May", "Mai").replace("June", "Juin").replace("July", "Juillet").replace("August", "Août").replace("September", "Septembre").replace("October", "Octobre").replace("November", "Novembre").replace("December", "Décembre")
    
    # Calculate the number of months since account creation
    today = datetime.today()
    delta = relativedelta(today, created_at)
    months_since_creation = delta.years * 12 + delta.months

    # Calculate average contributions per month
    if months_since_creation > 0:
        avg_contributions_per_month = contributions / months_since_creation
    else:
        avg_contributions_per_month = 0  # Avoid division by zero if account is less than a month old
    
    # Format the average contributions per month
    avg_contributions_per_month_str = f"{avg_contributions_per_month:.2f}"

    # Get random coding phrase
    phrase_of_the_day = get_random_coding_phrase()
    
    # Get current date for "generated on" timestamp
    current_date = datetime.now().strftime("%d %B %Y").replace("January", "Janvier").replace("February", "Février").replace("March", "Mars").replace("April", "Avril").replace("May", "Mai").replace("June", "Juin").replace("July", "Juillet").replace("August", "Août").replace("September", "Septembre").replace("October", "Octobre").replace("November", "Novembre").replace("December", "Décembre")

    # Create the README content in French
    readme = f"""

## 💭 Info du jour
> *"{phrase_of_the_day}"*

---

## À propos de moi
- 🌍 **Localisation**: {user.get('location') or 'Non spécifié'}
- 🎓 **Étudiant au CÉGEP Édouard-Montpetit**
- 🌐 **Langues**: FR / EN

---

## Statistiques GitHub
- 🧮 **Contributions totales**: {contributions}.  
  Cela fait **{avg_contributions_per_month_str} commits par mois** 😎
- 📂 **Projets publics**: {user.get('public_repos')}  
  Partagez, c'est mieux 🤝
- 👥 **Abonnés**: {user.get('followers')}
- 👀 **Abonnements**: {user.get('following')}
- 🗓️ **Compte créé le**: {created_date}

---

## Contact
N'hésitez pas à me contacter via GitHub ou à explorer mes projets !  
**Mon Portfolio** -> [saumure.com](https://saumure.com)

---

*README généré pour la dernière fois le {current_date} par un bot Python* -> [GitHub Profile](https://github.com/HenriSaumure/HenriSaumure)
"""
    
    return readme



def update_github_readme(readme_content):
    """Update the README.md file in the GitHub profile repository"""
    base_url = "https://api.github.com"
    repo_name = f"{github_username}/{github_username}"
    
    # First, check if README.md exists and get its SHA if it does
    contents_url = f"{base_url}/repos/{repo_name}/contents/README.md"
    contents_response = requests.get(contents_url, headers=headers)
    
    if contents_response.status_code == 200:
        # README.md exists, get its SHA for updating
        file_sha = contents_response.json().get('sha')
        
        # Update the file
        update_data = {
            "message": "Mise à jour du profil README",
            "content": base64.b64encode(readme_content.encode()).decode(),
            "sha": file_sha
        }
        
        update_response = requests.put(contents_url, json=update_data, headers=headers)
        
        if update_response.status_code == 200:
            print("README.md mis à jour avec succès!")
            return True
        else:
            print(f"Erreur lors de la mise à jour du README.md: {update_response.status_code}")
            print(update_response.json())
            return False
    
    elif contents_response.status_code == 404:
        # README.md doesn't exist, create it
        create_data = {
            "message": "Création du profil README",
            "content": base64.b64encode(readme_content.encode()).decode()
        }
        
        create_response = requests.put(contents_url, json=create_data, headers=headers)
        
        if create_response.status_code == 201:
            print("README.md créé avec succès!")
            return True
        else:
            print(f"Erreur lors de la création du README.md: {create_response.status_code}")
            print(create_response.json())
            return False
    
    else:
        print(f"Erreur lors de la vérification du README.md: {contents_response.status_code}")
        return False

def main():
    try:
        # Get profile information from GitHub API
        print(f"Récupération des informations GitHub pour {github_username}...")
        profile_data = get_github_profile_info()
        
        if profile_data:
            user_data = profile_data["user"]
            
            # Format dates
            created_at = datetime.strptime(user_data.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
            updated_at = datetime.strptime(user_data.get('updated_at'), "%Y-%m-%dT%H:%M:%SZ")
            
            # Display the basic profile info
            print("\nInformations du profil GitHub:")
            print("-" * 40)
            print(f"Projets publics: {user_data.get('public_repos')}")
            print(f"Abonnés: {user_data.get('followers')}")
            print(f"Abonnements: {user_data.get('following')}")
            print(f"Compte créé le: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Dernière mise à jour: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Localisation: {user_data.get('location') or 'Non spécifié'}")
            
            # Get contributions count from screenshot
            print("\nCapture d'écran pour extraire le nombre de contributions...")
            screenshot_path = os.path.join(screenshots_folder, "github_contributions.png")
            
            contributions = "Non trouvé"
            if capture_screenshot(profile_url, screenshot_path):
                contributions = extract_contributions_count(screenshot_path)
                print(f"Contributions dans la dernière année: {contributions}")
            else:
                print("Impossible de capturer l'écran pour le nombre de contributions.")
            
            # Generate README content
            print("\nGénération du contenu README.md...")
            readme_content = generate_readme(profile_data, contributions)
            
            # Preview the README content
            print("\nAperçu du contenu README.md:")
            print("-" * 40)
            print(readme_content)
            print("-" * 40)
            

            update_github_readme(readme_content)

            
        else:
            print("Impossible de récupérer les informations du profil.")
            
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")

if __name__ == "__main__":
    main()
