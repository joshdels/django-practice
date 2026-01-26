from django import forms

from .models import File, FileVersion


class ReuploadFileForm(forms.ModelForm):
    file_object = forms.ModelChoiceField(
        queryset=File.objects.none(),
        required=False,
        label="Select File",
    )

    new_file_name = forms.CharField(
        max_length=255, required=False, label="New File Name"
    )

    class Meta:
        model = FileVersion
        fields = ["uploaded_file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file_object"].queryset = File.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        file_obj = cleaned_data.get("file_object")
        new_name = cleaned_data.get("new_file_name")

        if not file_obj and not new_name:
            raise forms.ValidationError(
                "You must either select an existing file or provide a new file name."
            )

        return cleaned_data
