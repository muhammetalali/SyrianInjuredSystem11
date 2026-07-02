from django import forms
from .models import Patient, MedicalEvaluation, PersonalQuestionnaire


class PatientIntakeForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['status', 'created_at', 'updated_at']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'injury_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'health_condition': forms.Textarea(attrs={'rows': 3}),
            'previous_details': forms.Textarea(attrs={'rows': 3}),
            'other_documents': forms.Textarea(attrs={'rows': 3}),
            'reception_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class MedicalEvaluationForm(forms.ModelForm):
    class Meta:
        model = MedicalEvaluation
        exclude = ['patient', 'created_at']

        widgets = {
            'committee_members': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 4}),
            'medical_notes': forms.Textarea(attrs={'rows': 3}),
            'decision_reason': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PersonalQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = PersonalQuestionnaire
        exclude = ['patient', 'created_at']

        widgets = {
            'service_start_date': forms.DateInput(attrs={'type': 'date'}),
            'marital_details': forms.Textarea(attrs={'rows': 3}),
            'participated_battles': forms.Textarea(attrs={'rows': 4}),
            'injury_circumstances': forms.Textarea(attrs={'rows': 4}),
            'previous_injuries': forms.Textarea(attrs={'rows': 3}),
            'surgeries': forms.Textarea(attrs={'rows': 3}),
            'chronic_diseases': forms.Textarea(attrs={'rows': 3}),
            'current_medications': forms.Textarea(attrs={'rows': 3}),
            'psychological_condition': forms.Textarea(attrs={'rows': 3}),
            'rehabilitation_need': forms.Textarea(attrs={'rows': 3}),
            'family_support': forms.Textarea(attrs={'rows': 3}),
            'requested_support': forms.Textarea(attrs={'rows': 3}),
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})