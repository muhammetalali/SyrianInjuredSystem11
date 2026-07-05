from django.db import models
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^09\d{8}$',
    message='رقم الهاتف يجب أن يبدأ بـ 09 وأن يتكوّن من 10 خانات فقط.'
)

# 1. إضافة جدول جديد لأعضاء اللجنة الطبية
class Doctor(models.Model):
    name = models.CharField(
        max_length=150, 
        unique=True, 
        verbose_name='اسم الطبيب / عضو اللجنة'
    )

    def __str__(self):
        return self.name


class Patient(models.Model):
    STATUS_CHOICES = [
        ('UNDER_MEDICAL_REVIEW', 'قيد التقييم الطبي'),
        ('READY_FOR_ACTIVATION', 'قيد التفعيل'),
        ('ACCEPTED', 'مقبول'),
    ]

    is_medical_evaluation = models.BooleanField(
        default=False,
        verbose_name='تقييم طبي'
    )

    is_ministry_sent = models.BooleanField(
        default=False,
        verbose_name='مرسل وزارة'
    )

    is_extinct_factions = models.BooleanField(
        default=False,
        verbose_name='فصائل مندثرة'
    )

    tracking_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name='الرقم التسلسلي'
    )

    full_name = models.CharField(
        max_length=150,
        default='',
        verbose_name='الاسم الثلاثي'
    )

    nickname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='اللقب'
    )

    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[phone_validator],
        verbose_name='رقم الهاتف'
    )

    national_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name='الرقم الذاتي'
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ الميلاد'
    )

    extinct_faction_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='الفصيل المندثر'
    )

    current_residence = models.CharField(
        max_length=200,
        default='',
        verbose_name='السكن الحالي'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='UNDER_MEDICAL_REVIEW',
        verbose_name='حالة الملف'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.tracking_number:
            self.tracking_number = f"INJ-{self.pk:06d}"
            super().save(update_fields=['tracking_number'])

    def __str__(self):
        return self.full_name


class MedicalEvaluation(models.Model):
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_evaluation',
        verbose_name='المصاب'
    )

    injury_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ الإصابة'
    )

    injury_type = models.CharField(
        max_length=200,
        default='',
        verbose_name='نوع الإصابة'
    )

    injury_category = models.CharField(
        max_length=200,
        default='',
        verbose_name='فئة الإصابة'
    )

    injury_details = models.TextField(
        default='',
        verbose_name='تفاصيل الإصابة'
    )

    considered_injury_type = models.CharField(
        max_length=200,
        default='',
        verbose_name='نوع الإصابة المعتبرة'
    )

    considered_injury_category = models.CharField(
        max_length=200,
        default='',
        verbose_name='فئة الإصابة المعتبرة'
    )

    cause_and_location = models.CharField(
        max_length=255,
        default='',
        verbose_name='سبب ومكان الإصابة'
    )

    is_eligible = models.BooleanField(
        default=False,
        verbose_name='مستحق'
    )

    # 2. تغيير هذا الحقل ليكون قائمة منسدلة مرتبطة بجدول الأطباء
    doctor_name = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        verbose_name='اسم عضو اللجنة الطبية',
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ التقييم'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.patient.status = 'READY_FOR_ACTIVATION'
        self.patient.save(update_fields=['status'])

    def __str__(self):
        return f"تقييم طبي - {self.patient.full_name}"


class Activation(models.Model):
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='activation',
        verbose_name='المصاب'
    )

    is_mandatory = models.BooleanField(
        default=False,
        verbose_name='تفعيل إلزامي'
    )

    desired_work = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='العمل الذي ترغب به'
    )

    witness_1_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='اسم شاهد أول'
    )

    witness_1_phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[phone_validator],
        verbose_name='رقم هاتف الشاهد الأول'
    )

    witness_1_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الرقم الذاتي للشاهد الأول'
    )

    witness_2_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='اسم شاهد ثاني'
    )

    witness_2_phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[phone_validator],
        verbose_name='رقم هاتف الشاهد الثاني'
    )

    witness_2_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الرقم الذاتي للشاهد الثاني'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ التفعيل'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.patient.status = 'ACCEPTED'
        self.patient.save(update_fields=['status'])

    def __str__(self):
        return f"تفعيل - {self.patient.full_name}"