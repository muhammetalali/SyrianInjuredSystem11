from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Patient
from .forms import PatientIntakeForm, MedicalEvaluationForm, ActivationForm


@login_required
def dashboard(request):
    context = {
        'under_review_count': Patient.objects.filter(status='UNDER_MEDICAL_REVIEW').count(),
        'ready_for_activation_count': Patient.objects.filter(status='READY_FOR_ACTIVATION').count(),
        'accepted_count': Patient.objects.filter(status='ACCEPTED').count(),
    }

    return render(request, 'reception/dashboard.html', context)


@login_required
def intake_create(request):
    if request.method == 'POST':
        form = PatientIntakeForm(request.POST)

        if form.is_valid():
            patient = form.save(commit=False)
            patient.status = 'UNDER_MEDICAL_REVIEW'
            patient.save()

            return redirect('reception:medical_queue')
    else:
        form = PatientIntakeForm()

    return render(request, 'reception/intake_form.html', {'form': form})


@login_required
def medical_queue(request):
    patients = Patient.objects.filter(
        status='UNDER_MEDICAL_REVIEW'
    ).order_by('-created_at')

    return render(request, 'reception/medical_queue.html', {'patients': patients})


@login_required
def medical_evaluation_create(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    try:
        medical_evaluation = patient.medical_evaluation
    except Exception:
        medical_evaluation = None

    if request.method == 'POST':
        form = MedicalEvaluationForm(request.POST, instance=medical_evaluation)

        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.patient = patient
            evaluation.save()

            # بعد اعتماد التقييم الطبي ينتقل إلى التفعيل سواء مستحق نعم أو لا
            return redirect('reception:activation_create', patient_id=patient.id)
    else:
        form = MedicalEvaluationForm(instance=medical_evaluation)

    return render(
        request,
        'reception/medical_evaluation_form.html',
        {
            'form': form,
            'patient': patient,
        }
    )


@login_required
def activation_list(request):
    patients = Patient.objects.filter(
        status='READY_FOR_ACTIVATION'
    ).order_by('-created_at')

    return render(request, 'reception/activation_list.html', {'patients': patients})


@login_required
def activation_create(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    try:
        activation = patient.activation
    except Exception:
        activation = None

    try:
        medical_evaluation = patient.medical_evaluation
    except Exception:
        medical_evaluation = None

    if request.method == 'POST':
        form = ActivationForm(request.POST, instance=activation)

        if form.is_valid():
            activation = form.save(commit=False)
            activation.patient = patient
            activation.save()

            # بعد حفظ التفعيل ينتقل الملف إلى قائمة المقبولين
            return redirect('reception:accepted_list')
    else:
        form = ActivationForm(instance=activation)

    return render(
        request,
        'reception/questionnaire_form.html',
        {
            'form': form,
            'patient': patient,
            'medical_evaluation': medical_evaluation,
        }
    )


@login_required
def accepted_list(request):
    patients = Patient.objects.filter(
        status='ACCEPTED'
    ).order_by('-created_at')

    return render(request, 'reception/accepted_list.html', {'patients': patients})


@login_required
def rejected_list(request):
    patients = Patient.objects.none()

    return render(request, 'reception/rejected_list.html', {'patients': patients})


@login_required
def suspended_list(request):
    patients = Patient.objects.none()

    return render(request, 'reception/suspended_list.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    try:
        medical_evaluation = patient.medical_evaluation
    except Exception:
        medical_evaluation = None

    try:
        activation = patient.activation
    except Exception:
        activation = None

    return render(
        request,
        'reception/patient_detail.html',
        {
            'patient': patient,
            'medical_evaluation': medical_evaluation,
            'activation': activation,
        }
    )


@login_required
def print_report(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    try:
        medical_evaluation = patient.medical_evaluation
    except Exception:
        medical_evaluation = None

    try:
        activation = patient.activation
    except Exception:
        activation = None

    return render(
        request,
        'reception/print_report.html',
        {
            'patient': patient,
            'medical_evaluation': medical_evaluation,
            'activation': activation,
        }
    )