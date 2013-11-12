from django import forms

from helpers import get_model_form, getattr2, hasattr2


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
                print ">>>>", model_name
                if hasattr2(self.instance, model_name.replace("__", ".")):
                    obj = getattr2(self.instance, model_name.replace("__", "."))
                    print obj.__class__
                    if obj:
                        for field_name, field in zip(form.fields.keys(), form.fields.values()):
                            self.fields["%s__%s"%(model_name, field_name)].initial = getattr(obj, field_name)
            try:
                if self.Meta.fields:
                    for field in self.fields.keys():
                        if not field in self.Meta.fields:
                            self.fields.pop(field)
            except AttributeError:
                pass
        def save(self, *args, **kwargs):
            for model_name, Model in related:
                print model_name
                if hasattr2(self.instance, model_name.replace("__", ".")) and getattr2(self.instance, model_name.replace("__", ".")):
                    obj = getattr2(self.instance, model_name.replace("__", "."))
                else:
                    obj = Model()
                form = get_model_form(Model)()
                for field_name, field in zip(form.fields.keys(), form.fields.values()):
                    try:
                        print field_name, model_name, self.cleaned_data["%s__%s"%(model_name, field_name)]
                        setattr(obj, field_name, self.cleaned_data["%s__%s"%(model_name, field_name)])
                    except KeyError:
                        pass
                obj.save()
                setattr(self.instance, model_name, obj)
            return super(MultiModelForm, self).save(*args, **kwargs)
        class Meta:
            model = main_model
            exclude = [field_name for field_name, field in related]
    return MultiModelForm

