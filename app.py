from flask import Flask, request, render_template
from scripts.send_mail import send_email
from scripts.archive_files import create_rar
from scripts.download_images import download_imgs
import os

app = Flask(__name__,
            static_folder=r"scripts/static",
            template_folder=r"scripts/templates")

@app.route('/', methods=['GET','POST'])

def index():
    if request.method == 'POST':
        query = request.form['keyword']
        count = int(request.form['num_items'])
        email = request.form['email_id']
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        images_folder = os.path.join(current_directory, 'images')
        
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        
        download_imgs(query, count)
        
        output_rar = os.path.join(current_directory, "images_archive.rar")
        create_rar(images_folder, output_rar)
                
        subject = "Downloaded images"
        body = "Hey there! Kindly see your requested images in the given attachment."
        send_email(email, subject, body, output_rar)
        
        return "Images downloaded and archived! Please check your mail"
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)