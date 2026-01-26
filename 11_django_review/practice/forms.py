from django import forms
from .models import Project, File


class ReuploadFileForm(forms.ModelForm):
    uploaded_file = forms.FileField(required=True, label="Choose File")

    # Optional: select existing project
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label="Select Existing Project",
        empty_label="-- None --",
    )

    # Optional: create new project
    new_project_name = forms.CharField(
        max_length=255,
        required=False,
        label="New Project Name",
        help_text="If provided, this will create a new project.",
    )

    class Meta:
        model = File
        fields = ["uploaded_file", "project", "new_project_name"]

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get("project")
        new_project_name = cleaned_data.get("new_project_name")

        if project and new_project_name:
            raise forms.ValidationError(
                "You cannot select an existing project and create a new project at the same time."
            )
        return cleaned_data
