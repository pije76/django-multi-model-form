django-multi-model-form
=======================

Joining multiple ModelForm

### Authors
*  Ondrej Sika, <http://ondrejsika.com>, <ondrej@ondrejsika.com>

### Source
* Python Package Index: <http://pypi.python.org/pypi/django-multi-model-form>
* GitHub: <https://github.com/sikaondrej/django-multi-model-form>


Documentation
-------------

### Instalation
Instalation is very simple over pip.

    pip install django-multi-model-form


### Usage
settings.py

    INSTALLED_APPS += ("multi_model_form", )

myapp/models.py

    from django.db import models

    class RelatedModel(models.Model):
        a = models.IntegerField()
        b = models.IntegerField()
        c = models.IntegerField()

    class MainModel(models.Model):
        name = models.CharField(max_length=32)
        related = models.OneToOneField(RelatedModel)

myapp/forms.py

    from django import forms
    from multi_model_form import multi_model_form_generator
    from models import MainModel, RelatedModel

    MultiForm = multi_model_form_generator(MainModel, (("related", RelatedModel), ))

MultiForm contains all fields from related model.
