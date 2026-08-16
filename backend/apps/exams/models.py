from django.db import models
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='lectures/', blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lectures')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title}"

class Question(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'اختيار من متعدد'),
        ('true_false', 'صح/خطأ'),
        ('short', 'إجابة قصيرة'),
    )
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    mark = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:20]} - {self.text[:20]}"

class Exam(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    duration_minutes = models.IntegerField(default=60)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_mark = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shuffle_questions = models.BooleanField(default=False)
    auto_proctoring = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default='draft')  # draft, published, active, ended
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    mark = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    class Meta:
        ordering = ['order']

class StudentSubject(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, accepted, rejected

    class Meta:
        unique_together = ('student', 'subject')

class StudentExam(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, default='in_progress')  # in_progress, submitted, graded
    last_activity_at = models.DateTimeField(auto_now=True)

class StudentAnswer(models.Model):
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionChoice, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(blank=True)
    mark_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_correct = models.BooleanField(default=False)

class ExamEvent(models.Model):
    EVENT_TYPES = (
        ('join', 'دخل الامتحان'),
        ('submit', 'سلم الامتحان'),
        ('tab_switch', 'فتح تبويب آخر'),
        ('camera_denied', 'رفض الكاميرا'),
        ('audio_denied', 'رفض الميكروفون'),
        ('copy_paste', 'محاولة نسخ/لصق'),
        ('warning', 'إنذار'),
        ('force_submit', 'تسليم إجباري'),
    )
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MedicalExcuse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    document = models.FileField(upload_to='medical_excuses/')
    reason = models.TextField()
    status = models.CharField(max_length=20, default='pending')  # pending, approved, rejected
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_excuses', limit_choices_to={'role': 'admin'})