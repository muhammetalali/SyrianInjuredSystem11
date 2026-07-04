from django import forms
from .models import Patient, MedicalEvaluation, Activation


class PatientIntakeForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'is_medical_evaluation',
            'is_ministry_sent',
            'is_extinct_factions',
            'full_name',
            'nickname',
            'phone',
            'national_id',
            'date_of_birth',
            'extinct_faction_name',
            'current_residence',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'placeholder': 'مثال: 0912345678',
                'pattern': r'09[0-9]{8}',
                'title': 'رقم الهاتف يجب أن يبدأ بـ 09 وأن يتكوّن من 10 خانات فقط',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.required = False
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.required = True
                field.widget.attrs.update({'class': 'form-control'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            raise forms.ValidationError('رقم الهاتف مطلوب.')

        if not phone.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')

        if not phone.startswith('09'):
            raise forms.ValidationError('رقم الهاتف يجب أن يبدأ بـ 09.')

        if len(phone) != 10:
            raise forms.ValidationError('رقم الهاتف يجب أن يتكوّن من 10 خانات فقط.')

        return phone


class MedicalEvaluationForm(forms.ModelForm):
    is_eligible = forms.TypedChoiceField(
        label='مستحق',
        choices=(
            ('True', 'نعم'),
            ('False', 'لا'),
        ),
        coerce=lambda value: value == 'True',
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = MedicalEvaluation
        fields = [
            'injury_date',
            'injury_type',
            'injury_category',
            'injury_details',
            'considered_injury_type',
            'considered_injury_category',
            'cause_and_location',
            'is_eligible',
            'doctor_name',
        ]

        widgets = {
            'injury_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'injury_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.required = False
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': 'radio-list'})
            else:
                field.required = True
                field.widget.attrs.update({'class': 'form-control'})


class ActivationForm(forms.ModelForm):
    OPTIONAL_FIELDS = [
        'witness_1_name',
        'witness_1_phone',
        'witness_1_id',
        'witness_2_name',
        'witness_2_phone',
        'witness_2_id',
    ]

    class Meta:
        model = Activation
        exclude = ['patient']

        widgets = {
            'witness_1_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'placeholder': 'اختياري - مثال: 0912345678',
                'pattern': r'09[0-9]{8}',
            }),
            'witness_2_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'placeholder': 'اختياري - مثال: 0912345678',
                'pattern': r'09[0-9]{8}',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.required = False
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

                if field_name in self.OPTIONAL_FIELDS:
                    field.required = False
                    field.widget.attrs.update({
                        'placeholder': field.widget.attrs.get('placeholder', 'اختياري')
                    })
                else:
                    field.required = True

    def clean_witness_1_phone(self):
        phone = self.cleaned_data.get('witness_1_phone')

        # الحقل اختياري، إذا تُرك فارغًا لا يظهر خطأ
        if not phone:
            return phone

        if not phone.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')

        if not phone.startswith('09'):
            raise forms.ValidationError('رقم الهاتف يجب أن يبدأ بـ 09.')

        if len(phone) != 10:
            raise forms.ValidationError('رقم الهاتف يجب أن يتكوّن من 10 خانات فقط.')

        return phone

    def clean_witness_2_phone(self):
        phone = self.cleaned_data.get('witness_2_phone')

        # الحقل اختياري، إذا تُرك فارغًا لا يظهر خطأ
        if not phone:
            return phone

        if not phone.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')

        if not phone.startswith('09'):
            raise forms.ValidationError('رقم الهاتف يجب أن يبدأ بـ 09.')

        if len(phone) != 10:
            raise forms.ValidationError('رقم الهاتف يجب أن يتكوّن من 10 خانات فقط.')

        return phone