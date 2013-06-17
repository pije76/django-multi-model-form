from django import forms

def get_model_form(Model):
    class ModelForm(forms.ModelForm):
        class Meta:
            model = Model
    return ModelForm
