from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import TutorialUploadForm,LevelSelectionForm,RatingForm
from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Avg
from django.utils import formats
from django.urls import reverse_lazy #https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse-lazy
import datetime
from . models import *
import os
import unicodedata
import zipfile
from . views import base_function


def thanks(request):
    context = base_function(request)
    context.update({'tutorial_name':"tutorial.pdf", 'tutorial_screenshot':"screenshot.png", 'tutorial_resources':"resources.zip"})
    return render(request, "coderdojomobile/thanks_tutorial.html", context)

def thanks_rating(request):
    context = base_function(request)
    return render(request, "coderdojomobile/thanks_rating.html", context)

def rating_error(request):
    context = base_function(request)
    return render(request, "coderdojomobile/rating_error.html", context)


def handle_uploaded_file(uploaded,description):
    files = {}
    with zipfile.ZipFile(uploaded, 'r') as z:
        # we need to extract:
        # The tutorial file.
        # The screenshot file
        # The resources file
        # Save all of them to media folder (not the original zip file!)
        # Save data on the DB
        # TODO handle malformed zip
        resource_entity = None
        tutorial_entity = None
        project_name = None
        for f in z.namelist():
            info = z.getinfo(f)
            if info.is_dir():
                project_name = f.split('/')[0]
            if f.endswith('pdf'):
                with z.open(f) as pdfFileInZip:
                    pdfFile = File(pdfFileInZip)
                    tutorial_entity = GenericUserFile(title=f, file = pdfFile)
                    # now g.file is a FieldFile object https://docs.djangoproject.com/en/2.0/ref/models/fields/#filefield-and-fieldfile
                    tutorial_entity.file.field.upload_to="tutorial/" # We need to set the base folder as generic files have no base folder
                    tutorial_entity.save() # This automatically saves the file
            if f.endswith('png'):
                with z.open(f) as pdfFileInZip:
                    pngFile = File(pdfFileInZip)
                    screenshot_entity = GenericUserFile(title=f, file = pngFile)
                    screenshot_entity.file.field.upload_to="tutorial/"
                    screenshot_entity.save()
            if f.endswith('zip'):
                with z.open(f) as pdfFileInZip:
                    resourceFile = File(pdfFileInZip)
                    resource_entity = GenericUserFile(title=f, file = resourceFile)
                    resource_entity.file.field.upload_to="tutorial/"
                    resource_entity.save()
        # Now save the tutorial
        learningMaterial = LearningMaterial()
        learningMaterial.title = project_name
        learningMaterial.description = description       
        learningMaterial.tutorial = tutorial_entity
        learningMaterial.screenshot = screenshot_entity
        learningMaterial.save()
        learningMaterial.resources.add(resource_entity)
        learningMaterial.save()
        # For now just save the file to GenericUserFiles
        #g = GenericUserFile(title="tutorial.pdf", file = pdfFile)
        #g.save()
        
    return files


def tutorials(request,topic_id,material_level=None):
    context = base_function(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TutorialUploadForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            files = handle_uploaded_file(request.FILES['tutorial_file'],request.POST['tutorial_description'])
            return HttpResponseRedirect(reverse_lazy('coderdojomobile:thanks'))
    # if a GET (or any other method) we'll create a blank form
    else:
        # but still we have to filter checking whether a specific level was requested by url or by form
        # Average rating is retrieved using Django powerful model query api
        try:
            requested_material_level = request.GET['level'] # read from form get
        except KeyError:
            requested_material_level = None
        if requested_material_level is None or requested_material_level == LevelSelectionForm.LEVEL_ALL:
            projects=LearningMaterial.objects.all().filter(topic_id=topic_id,is_active=True).order_by('level','title').annotate(avg_rating=Avg('rating__value'))
        else:
            projects=LearningMaterial.objects.all().filter(topic_id=topic_id,is_active=True,level=requested_material_level).order_by('level','title').annotate(avg_rating=Avg('rating__value'))
        form = TutorialUploadForm()
        search_form = LevelSelectionForm()
        context.update({'projects': projects, 
                    'form' : form,
                    'topic_id': topic_id,
                    'search_form' : search_form})
        return render(request, 'coderdojomobile/tutorials.html', context)

def handle_learning_material_rating(request,tutorial):
    # create a form instance and populate it with data from the request:
    form = RatingForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        rating = Rating()
        rating.value = form.cleaned_data['value']
        rating.comment = form.cleaned_data['comment']
        rating.material = tutorial
        rating.rating_date = datetime.date.today()
        rating.rating_source = request.META['REMOTE_ADDR']
        rating.rating_author = form.cleaned_data['rating_author']
        rating.save()
        return HttpResponseRedirect(reverse_lazy('coderdojomobile:rating_thanks'))
    else:
        return HttpResponseRedirect(reverse_lazy('coderdojomobile:rating_error'))

def tutorial(request, tutorial_id):
    context = base_function(request)
    tutorial=LearningMaterial.objects.get(id=tutorial_id)
    form = RatingForm()
    ratings=Rating.objects.all().filter(material_id=tutorial_id)
    context.update({'form': form})
    for r in ratings:
        r.date_formatted = formats.date_format(r.rating_date, 'DATE_FORMAT')
    if request.method == 'POST':
        return handle_learning_material_rating(request,tutorial)
    else:
        context.update({'project': tutorial,
                'project_resources' : tutorial.resources.all(),
                'ratings':ratings})
    return render(request, "coderdojomobile/tutorial.html", context)


