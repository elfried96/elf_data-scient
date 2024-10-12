import gradio as gr
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Fonctions de traitement d'image
def load_image(image):
    return image

def apply_negative(image):
    img_np = np.array(image)
    negative = 255 - img_np
    return Image.fromarray(negative)

def binarize_image(image, threshold):
    img_np = np.array(image.convert('L'))
    _, binary = cv2.threshold(img_np, threshold, 255, cv2.THRESH_BINARY)
    return Image.fromarray(binary)

def resize_image(image, width, height):
    try:
        width = int(width)
        height = int(height)  
        return image.resize((width, height))
    except Exception as e:
        print(f"Erreur lors du redimensionnement : {e}")
        return image 

def rotate_image(image, angle):
    return image.rotate(angle)

def show_histogram(image):
    img_np = np.array(image.convert('L'))  # Conversion en niveaux de gris
    plt.hist(img_np.ravel(), bins=256, range=(0, 256))
    plt.title("Histogramme des niveaux de gris")
    plt.xlabel("Valeur des pixels")
    plt.ylabel("Fréquence")
    plt.savefig('histogram.png')  # Sauvegarde de l'histogramme
    plt.close()
    return 'histogram.png'

def apply_filter(image, filter_type):
    img_np = np.array(image)
    if filter_type == "Filtre Moyen":
        return Image.fromarray(cv2.blur(img_np, (5, 5)))
    elif filter_type == "Filtre Gaussien":
        return Image.fromarray(cv2.GaussianBlur(img_np, (5, 5), 0))

def sobel_edges(image):
    img_np = np.array(image.convert('L'))
    sobelx = cv2.Sobel(img_np, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img_np, cv2.CV_64F, 0, 1, ksize=5)
    sobel = np.hypot(sobelx, sobely)
    return Image.fromarray(np.uint8(sobel))

def morphological_ops(image, operation_type):
    img_np = np.array(image.convert('L'))
    kernel = np.ones((5,5), np.uint8)
    if operation_type == "Érosion":
        return Image.fromarray(cv2.erode(img_np, kernel, iterations=1))
    elif operation_type == "Dilatation":
        return Image.fromarray(cv2.dilate(img_np, kernel, iterations=1))

def save_image(image):
    image.save("output_image.png")
    return "Image sauvegardée sous 'output_image.png'"

# Interface Gradio
def image_processing(image_input, webcam_image, operation, threshold=128, width=100, height=100, angle=0, filter_type=None, morph_op=None):
    # Choisir l'image à traiter (upload ou webcam)
    if webcam_image is not None:
        image = webcam_image  # Utiliser l'image de la webcam
    else:
        image = image_input  # Utiliser l'image téléchargée

    if operation == "Négatif":
        return apply_negative(image)
    elif operation == "Binarisation":
        return binarize_image(image, threshold)
    elif operation == "Redimensionner":
        return resize_image(image, width, height)
    elif operation == "Rotation":
        return rotate_image(image, angle)
    elif operation == "Histogramme":
        return show_histogram(image)
    elif operation == "Filtre":
        return apply_filter(image, filter_type)
    elif operation == "Sobel":
        return sobel_edges(image)
    elif operation == "Morphologie":
        return morphological_ops(image, morph_op)
    return image

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='color: white;'>Projet de Traitement d'Image - PSVO 2024</h1>")
    
    with gr.Row():
        image_input = gr.Image(type="pil", label="Charger Image", tool="editor", source="upload")
        webcam_input = gr.Image(type="pil", label="Prendre Photo avec Webcam", source="webcam")
        operation = gr.Radio(
            ["Négatif", "Binarisation", "Redimensionner", "Rotation", "Histogramme", "Filtre", "Sobel", "Morphologie"],
            label="Opération"
        )

    with gr.Row():
        threshold = gr.Slider(0, 255, 128, label="Seuil de binarisation", visible=False)
        width = gr.Slider(minimum=50, maximum=1000, step=1, value=100, label="Largeur", visible=False)
        height = gr.Slider(minimum=50, maximum=1000, step=1, value=100, label="Hauteur", visible=False)
        angle = gr.Number(value=0, label="Angle de Rotation", visible=False)
        filter_type = gr.Radio(["Filtre Moyen", "Filtre Gaussien"], label="Type de Filtre", visible=False)
        morph_op = gr.Radio(["Érosion", "Dilatation"], label="Opération Morphologique", visible=False)
    
    image_output = gr.Image(label="Image Modifiée")
    submit_button = gr.Button("Appliquer")
    save_button = gr.Button("Sauvegarder Image")

    # Mise à jour des composants visibles selon l'opération choisie
    def update_visibility(operation):
        return {
            threshold: gr.update(visible=operation == "Binarisation"),
            width: gr.update(visible=operation == "Redimensionner"),
            height: gr.update(visible=operation == "Redimensionner"),
            angle: gr.update(visible=operation == "Rotation"),
            filter_type: gr.update(visible=operation == "Filtre"),
            morph_op: gr.update(visible=operation == "Morphologie"),
        }

    operation.change(fn=update_visibility, inputs=[operation], outputs=[threshold, width, height, angle, filter_type, morph_op])

    submit_button.click(image_processing, inputs=[image_input, webcam_input, operation, threshold, width, height, angle, filter_type, morph_op], outputs=image_output)
    save_button.click(save_image, inputs=[image_output], outputs=None)

# Lancer l'application Gradio
demo.launch()
