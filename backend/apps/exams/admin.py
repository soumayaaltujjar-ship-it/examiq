from django.contrib import admin
from .models import Subject, Lecture, Question, QuestionChoice, Exam, ExamQuestion, StudentSubject, StudentExam, StudentAnswer, ExamEvent, MedicalExcuse

admin.site.register(Subject)
admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(QuestionChoice)
admin.site.register(Exam)
admin.site.register(ExamQuestion)
admin.site.register(StudentSubject)
admin.site.register(StudentExam)
admin.site.register(StudentAnswer)
admin.site.register(ExamEvent)
admin.site.register(MedicalExcuse)