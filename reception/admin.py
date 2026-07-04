from django.contrib import admin
from .models import Patient, MedicalEvaluation, Activation


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_number',
        'full_name',
        'national_id',
        'phone',
        'status',
        'created_at',
    )

    search_fields = (
        'tracking_number',
        'full_name',
        'national_id',
        'phone',
    )

    list_filter = (
        'status',
        'created_at',
    )

    readonly_fields = (
        'tracking_number',
        'created_at',
    )


@admin.register(MedicalEvaluation)
class MedicalEvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'is_eligible',
        'doctor_name',
        'created_at',
    )

    search_fields = (
        'patient__tracking_number',
        'patient__full_name',
        'doctor_name',
        'injury_type',
        'injury_category',
    )

    list_filter = (
        'is_eligible',
        'created_at',
    )


@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'desired_work',
        'is_mandatory',
        'created_at',
    )

    search_fields = (
        'patient__tracking_number',
        'patient__full_name',
        'desired_work',
        'witness_1_name',
        'witness_2_name',
    )

    list_filter = (
        'is_mandatory',
        'created_at',
    )