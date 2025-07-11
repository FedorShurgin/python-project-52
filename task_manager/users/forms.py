from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required=True
        self.fields['last_name'].required=True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class CustomUserUpdateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
        
    #clean_username