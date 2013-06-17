from django import forms

from helpers import get_model_form


def multi_model_form_generator(main_model, related=[]):
    class MultiModelForm(forms.ModelForm):
        for model_name, Model in related:
            form = get_model_form(Model)()
            for field_name, field in zip(form.fields.keys(), form.fields.values()) + [(None, None)]:
                if field_name:
                    exec "%s = field" % ("%s__%s"%(model_name, field_name))
                else:
                    exec "pass"
        def __init__(self, *args, **kwargs):
            super(MultiModelForm, self).__init__(*args, **kwargs)
            for model_name, Model in related:
                form = get_model_form(Model)()
                if hasattr(self.instance, model_name):
                    obj = getattr(self.instance, model_name)
                    if obj:
                        for field_name, field in zip(form.fields.keys(), form.fields.values()):
                            self.fields["%s__%s"%(model_name, field_name)].initial = getattr(obj, field_name)
        def save(self, *args, **kwargs):
            for model_name, Model in related:
                if hasattr(self.instance, model_name) and getattr(self.instance, model_name):
                    obj = getattr(self.instance, model_name)
                else:
                    obj = Model()
                form = get_model_form(Model)()
                for field_name, field in zip(form.fields.keys(), form.fields.values()):
                    setattr(obj, field_name, self.cleaned_data["%s__%s"%(model_name, field_name)])
                obj.save()
                setattr(self.instance, model_name, obj)
            return super(MultiModelForm, self).save(*args, **kwargs)
        class Meta:
            model = main_model
            exclude = [field_name for field_name, field in related]
    return MultiModelForm
