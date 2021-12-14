"""
Routes and views for the flask application.
"""
import os
from datetime import datetime
from PIL import Image, ImageEnhance
from flask import render_template, request, url_for, flash, redirect
from Histogram import app
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt

#Определяем цвета гистограммы  RGB
def getRed(redVal):

    return '#%02x%02x%02x' % (redVal, 0, 0)

def getGreen(greenVal):

    return '#%02x%02x%02x' % (0, greenVal, 0)

def getBlue(blueVal):

    return '#%02x%02x%02x' % (0, 0, blueVal)

#Создание гистограммы изображения
def histogramImage(histogramURL, figura, imageURL):  
    #Создание гистограммы
    image = Image.open(imageURL)
    histogram = image.histogram()

    #Список счетчиков пикселей для краснояго канала
    l1 = histogram[0:256]

    #Список счетчиков пикселей для синего канала
    l2 = histogram[256:512]

    #Список счетчиков пикселей для зелёного канала
    l3 = histogram[512:768]

    for i in range(0, 256):
       plt.title("Гистограмма RGB")
       plt.bar(i, l1[i], color = getRed(i), edgecolor=getRed(i), alpha=0.3)
       plt.bar(i, l2[i], color = getGreen(i), edgecolor=getGreen(i),alpha=0.3)
       plt.bar(i, l3[i], color = getBlue(i), edgecolor=getBlue(i),alpha=0.3)
    figura.savefig('Histogram/' + histogramURL)  
    


#Изменить контраст изображения
def Contrast(numContrast):
    image = Image.open("Histogram/static/img/test.jpg")
    enhancer = ImageEnhance.Contrast(image)
    factor = float(numContrast)
    im_output = enhancer.enhance(factor) 
    im_output.save("Histogram/static/imgNew/test.jpg") 


UPLOAD_FOLDER = 'Histogram/static/img/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Визуализация
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        numContrast = request.form['select']
        filename = 'test.jpg'
        # проверим, передается ли в запросе файл 
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        
        
        
        if file and allowed_file(file.filename):
            # сохраняем файл
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            histogramImage('static/histogram/test.jpg', plt.figure(), 'Histogram/static/img/test.jpg')
            Contrast(numContrast)  
            histogramImage('static/histogramNew/test.jpg', plt.figure(), 'Histogram/static/imgNew/test.jpg')
            return redirect(url_for('index'))
        
    return render_template(
        'index.html',
        image_name = 'static/img/test.jpg',
        image_nameNew='static/imgNew/test.jpg',
        histogram='static/histogram/test.jpg',
        histogramNew='static/histogramNew/test.jpg',
        title='Гистограмма RGB'
    )