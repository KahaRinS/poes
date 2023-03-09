from django.shortcuts import render
from users.forms import CustomUserCreationForm


def RegionView(request):
    error = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            error = ''
            form.save()
        else:
            error = 'plohie dannie'
    form = CustomUserCreationForm
    data = {
        'form': form,
        'name': 'Регистрация',
        'ern': error,
    }
    return render(request, 'main/region.html', data)