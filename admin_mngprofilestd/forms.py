from django import forms
from login_std.models import profile_std


#form tìm kiếm profile của sinh viên
class CustomSearchForm(forms.Form):
    search_query = forms.CharField(label='Tìm kiếm', max_length=100)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = profile_std
        fields = '__all__'