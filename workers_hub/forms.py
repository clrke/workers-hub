from django import forms


class UploadFileForm(forms.Form):
    user = forms.IntegerField()
    tags = forms.MultipleChoiceField()
    images = forms.MultipleChoiceField()
    subject = forms.CharField(max_length=255)
    description = forms.Textarea()
    range_min = forms.IntegerField()
    range_max = forms.IntegerField()

