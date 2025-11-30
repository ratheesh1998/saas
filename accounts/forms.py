from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import RailwaySettings, Template

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'hx-post': '/accounts/check-email/',
            'hx-trigger': 'blur',
            'hx-target': '#email-error',
            'hx-swap': 'innerHTML'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'auth-form'
        self.helper.layout = Layout(
            Field('email', css_class='form-control'),
            Field('password1', css_class='form-control'),
            Field('password2', css_class='form-control'),
            Submit('submit', 'Sign Up', css_class='btn btn-primary w-100')
        )
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'auth-form'
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('password', css_class='form-control'),
            Submit('submit', 'Sign In', css_class='btn btn-primary w-100')
        )


class RailwaySettingsForm(forms.ModelForm):
    """Form for Railway settings"""
    
    class Meta:
        model = RailwaySettings
        fields = ['railway_template_id', 'railway_workspace_id', 'railway_token']
        widgets = {
            'railway_template_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Railway Template ID',
            }),
            'railway_workspace_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Railway Workspace ID',
            }),
            'railway_token': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Railway API Token (leave blank to keep existing)',
                'autocomplete': 'new-password',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'railway-settings-form'
        
        # Make token field optional (users can update other fields without changing token)
        self.fields['railway_token'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # If token field is empty but instance already exists with a token, keep the existing one
        if not self.cleaned_data.get('railway_token'):
            if instance.pk:
                # Get the original token from database
                try:
                    original = RailwaySettings.objects.get(pk=instance.pk)
                    if original.railway_token:
                        instance.railway_token = original.railway_token
                except RailwaySettings.DoesNotExist:
                    pass
        if commit:
            instance.save()
        return instance


class TemplateCreationForm(forms.ModelForm):
    """Form for creating Railway templates"""
    
    class Meta:
        model = Template
        fields = ['name', 'description', 'template_config']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter template name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter template description',
                'rows': 4,
            }),
            'template_config': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter template configuration as JSON',
                'rows': 10,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'template-creation-form'
        
        # Set initial JSON format if instance exists
        if self.instance and self.instance.pk and self.instance.template_config:
            self.fields['template_config'].initial = self._format_json(self.instance.template_config)
    
    def _format_json(self, data):
        """Format JSON data for display"""
        import json
        try:
            return json.dumps(data, indent=2)
        except:
            return str(data)
    
    def clean_template_config(self):
        """Validate and parse JSON template config"""
        import json
        config = self.cleaned_data.get('template_config', {})
        
        # Handle both string and dict/list inputs
        # Django's JSONField may already parse it, or it might still be a string
        if isinstance(config, str):
            try:
                config = json.loads(config)
            except json.JSONDecodeError as e:
                raise forms.ValidationError(f"Invalid JSON format: {str(e)}")
        
        # Ensure we have a dict or list
        if not isinstance(config, (dict, list)):
            raise forms.ValidationError("Template config must be a valid JSON object or array")
        
        return config
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

