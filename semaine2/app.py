import gradio as gr
from PIL import Image

# Simuler l'identification de la morphologie à partir de l'image de la personne
def detecter_morphologie(image_personne):
    # Ici, ton modèle de vision par ordinateur sera utilisé pour analyser la morphologie
    # On simule une réponse pour cet exemple
    morphologie_detectee = "Mésomorphe"  # Exemples possibles : Ectomorphe, Mésomorphe, Endomorphe
    return morphologie_detectee

# Fonction simulant l'analyse des vêtements et du reste des informations
def analyse_vetement(image_vetement, ethnie, style_prefere, morphologie_detectee):
    # Simuler la génération de recommandations de style
    recommandations = f"Pour une morphologie '{morphologie_detectee}' et une ethnie '{ethnie}', voici des recommandations basées sur le style '{style_prefere}' : \n"
    recommandations += "1. Choisissez des couleurs neutres\n"
    recommandations += "2. Préférez des coupes ajustées pour mettre en valeur vos formes\n"
    
    return recommandations, image_vetement

# Interface Gradio
with gr.Blocks() as demo:
    gr.Markdown(
        """
        ## Recommandations de styles basées sur votre morphologie et votre ethnie
        
        Soumettez une photo de vous, et notre système identifiera automatiquement votre morphologie. Ensuite, vous pourrez soumettre l'image d'un vêtement pour recevoir des recommandations personnalisées.
        """
    )
    
    with gr.Row():
        with gr.Column():
            # Première étape : Soumission de la photo pour détecter la morphologie
            image_personne = gr.Image(label="Télécharger une image de vous", type="pil")
            bouton_detecter = gr.Button("Détecter la morphologie")
            morphologie_detectee = gr.Textbox(label="Morphologie détectée", interactive=False)
        
        with gr.Column():
            # Après détection de la morphologie, le reste du formulaire s'affiche
            image_vetement = gr.Image(label="Télécharger une image du vêtement", type="pil")
            ethnie = gr.Radio(["Africaine", "Asiatique", "Caucasienne", "Latine", "Autre"], label="Votre ethnie")
            style_prefere = gr.Radio(["Classique", "Décontracté", "Chic", "Sportif"], label="Votre style préféré")
            bouton_analyser = gr.Button("Analyser")

    # Zone pour afficher les recommandations et l'aperçu du vêtement
    recommandation = gr.Textbox(label="Recommandations")
    image_resultat = gr.Image(label="Aperçu du vêtement", type="pil")

    # Détecter la morphologie en cliquant sur le bouton
    bouton_detecter.click(detecter_morphologie, inputs=image_personne, outputs=morphologie_detectee)
    
    # Une fois la morphologie détectée, l'utilisateur peut soumettre le reste des informations
    bouton_analyser.click(analyse_vetement, 
                          inputs=[image_vetement, ethnie, style_prefere, morphologie_detectee], 
                          outputs=[recommandation, image_resultat])

# Lancer l'application
demo.launch()
