from django import forms

from Cats.models import FormForAdopt, FormForGive, FormForGuardianship


class AdoptForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat_name'].empty_label = 'Котик не выбран'

    class Meta:
        model = FormForAdopt
        fields = ['name', 'phone', 'email', 'social', 'cat_name', 'why_this_cat', 'children', 'has_pet', 'pets']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(000) 000-0000', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш адрес электронной почты'}),
            'social': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Оставьте здесь ссылку на вашу страницу'}),
            'cat_name': forms.Select(attrs={'class': "form-select"}),
            'why_this_cat': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Расскажите почему выбрали именно этого кота'}),
            'children': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_pet': forms.CheckboxInput(attrs={'class': 'form-check-input', 'name': 'has_pet'}),
            'pets': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Расскажите какие у вас есть еще животные'})
        }


class GiveForm(forms.ModelForm):
    class Meta:
        model = FormForGive
        fields = ['name', 'phone', 'email', 'social', 'cat_name', 'birthday', 'character', 'features', 'gender', 'type_of_help', 'reason', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'cat_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите имя вашего котика'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(000) 000-0000', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш адрес электронной почты'}),
            'social': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Оставьте здесь ссылку на вашу страницу'}),
            'birthday': forms.DateInput(attrs={'class': "form-control", 'type': 'date'}),
            'character': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опишите характер котика'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Расскажите есть ли у котика какие-то особенности, '
                                                                                      'о которых мы должны знать'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'type_of_help': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Напишите по какой причине вы решили отдать нам котика'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Добавьте фотографию котика'})
        }


class GuardianshipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat_name'].empty_label = 'Котик не выбран'

    class Meta:
        model = FormForGuardianship
        fields = ['name', 'phone', 'email', 'social', 'cat_name', 'amount_of_money', 'interval']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(000) 000-0000', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш адрес электронной почты'}),
            'social': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Оставьте здесь ссылку на вашу страницу'}),
            'cat_name': forms.Select(attrs={'class': "form-select"}),
            'amount_of_money': forms.Select(attrs={'class': 'form-select'}),
            'interval': forms.Select(attrs={'class': 'form-select'})
        }