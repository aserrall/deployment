from django.contrib import admin
from .models import *
from .forms import RegisterForm, UserEditorForm

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = UserEditorForm
        else:
            self.form = RegisterForm
        return super(UserAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(User, UserAdmin)
