from PIL import ImageTk, Image

def animate_images():
    # Chemin des images
    image_path1 = "assets/mort.png"
    image_path2 = "assets/arriere.png"

    # Charger les images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # Redimensionner les images si nécessaire
    image1 = image1.resize((200, 200), Image.ANTIALIAS)
    image2 = image2.resize((200, 200), Image.ANTIALIAS)

    # Créer une liste d'images pour l'animation
    images = [image1, image2]

    # Index de l'image actuellement affichée
    current_image_index = 0

    # Fonction récursive pour mettre à jour l'affichage à intervalles réguliers
    def update_image(image_label, root):
        nonlocal current_image_index

        # Afficher l'image actuelle dans le label
        current_image = images[current_image_index]
        photo = ImageTk.PhotoImage(current_image)
        image_label.configure(image=photo)
        image_label.image = photo

        # Passer à l'image suivante
        current_image_index = (current_image_index + 1) % len(images)

        # Planifier la prochaine mise à jour après 0.5 seconde
        root.after(500, update_image)

    # Lancer l'animation en appelant la fonction update_image pour la première fois
    update_image()
