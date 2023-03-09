from main.models import Region, Sensors, Results
from django.forms import ModelForm, TextInput, DateInput, TimeInput

class RegionForm(ModelForm):
    class Meta:
        model = Region
        fields = ('name',)

class SensorForm(ModelForm):
    class Meta:
        model = Sensors
        fields = ['senname', 'region', 'longitude', 'dolgitude', ]

class ResultForm(ModelForm):
    class Meta:
        model = Results
        fields = ['temp', 'sensor', 'date', 'time', ]

        widgets = {
            'date': DateInput,
            'time': TimeInput
        }