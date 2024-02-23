from django.contrib import admin
from .models import UserInput, GPTResponse

@admin.register(UserInput)
class UserInputAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at']

@admin.register(GPTResponse)
class GPTResponseAdmin(admin.ModelAdmin):
    list_display = ['user_input', 'text', 'created_at']