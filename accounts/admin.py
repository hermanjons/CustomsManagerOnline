from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ClientProfile, ConsultantProfile
from .forms import ClientProfileForm, ConsultantProfileForm


# Kullanıcı modeli için özelleştirilmiş admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_superuser')}
         ),
    )

    search_fields = ('username', 'email')
    ordering = ('email',)




@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    form = ClientProfileForm
    list_display = ('company_name', 'authorized_person', 'phone', 'email')
    search_fields = ('company_name', 'authorized_person', 'email')


@admin.register(ConsultantProfile)
class ConsultantProfileAdmin(admin.ModelAdmin):
    form = ConsultantProfileForm
    list_display = ('full_name', 'company_name', 'phone', 'email')
    search_fields = ('full_name', 'company_name', 'email')
