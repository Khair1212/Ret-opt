from django.contrib import admin
from .models import User, OTP
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'is_analyst', 'DOB', 'gender', 'city_code')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'is_analyst', 'DOB', 'gender', 'city_code', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'is_active', 'is_admin', 'is_analyst')
    list_filter = ('is_active', 'is_admin', 'is_analyst')
    search_fields = ('email', 'name')
    ordering = ('email',)


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
#admin.site.register(OTP)

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'has_used', 'task_type')

