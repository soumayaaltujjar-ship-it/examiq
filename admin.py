from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # الحقول اللي تظهر في صفحة قائمة المستخدمين
    list_display = ('username', 'email', 'full_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('-created_at',)

    # الحقول اللي تظهر في صفحة تعديل المستخدم (النموذج الكامل)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('معلومات شخصية', {'fields': ('full_name', 'email', 'role')}),
        ('الصلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تواريخ مهمة', {'fields': ('last_login', 'date_joined')}),
    )

    # الحقول اللي تظهر في صفحة إضافة مستخدم جديد (اللي كنت تبحث عنها!)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

# سجل النموذج مع الإعدادات المخصصة
admin.site.register(User, CustomUserAdmin)