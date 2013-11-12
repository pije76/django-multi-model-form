from django import forms

def get_model_form(Model):
    class ModelForm(forms.ModelForm):
        class Meta:
            model = Model
    return ModelForm

def getattr2(obj, attr):
    for attr_part in attr.split("."):
        obj = getattr(obj, attr_part)
        if not obj:
            raise AttributeError
    return obj

def hasattr2(obj, attr):
    try:
        getattr2(obj, attr)
        return True
    except:
        return False