from django import forms
from cms.models import Schedule, Content, Piece


# constants to hold valid choice field values
STATUS_CHOICES = (
    ('NOT ACTIVE', 'NOT ACTIVE'),
    ('ACTIVE', 'ACTIVE'),
)
PAGE_SECTION_CHOICES = (
    ('Banner', 'Banner'),
    ('Rotator', 'Rotator'),
    ('NavAd', 'NavAd'),
    ('FeaturedAd', 'FeaturedAd'),
    ('TextAd', 'TextAd'),
)
CONTENT_TYPE_CHOICES = (
    ('IMAGE', 'IMAGE'),
    ('TEXT', 'TEXT'),
)


class ScheduleForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)

        # define last selected company var
        self.company = request['company']

        # set the initial company form settings / hide control
        self.fields['company'].initial = self.company
        self.fields['company'].widget.attrs['hidden'] = True
        self.fields['company'].label = ''

        # add the bootstrap form control class to each widget
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'

    class Meta:
        model = Schedule
        # fields = ['name', 'start_time', 'end_time', 'status', 'company']
        fields = '__all__'
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES),
        }
        labels = {
            'start_time': 'Start Date (yyyy-mm-dd) Time (24hr)',
            'end_time': 'End Date (yyyy-mm-dd) Time (24hr)'
        }


class ContentForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['content_type'].widget.attrs['hidden'] = True
            self.fields['content_type'].label = ''

        # define last selected company var
        self.company = request['company']

        # set the initial company form settings / hide control (we don't want this editable)
        self.fields['company'].initial = self.company
        self.fields['company'].widget.attrs['hidden'] = True
        self.fields['company'].label = ''

        # set the schedules form data and label only grabbing schedules for the session stored company
        self.fields['schedules'].queryset = Schedule.objects.filter(company=self.company)
        self.fields['schedules'].label = str(self.company).upper() + ' SCHEDULES'

        # add the bootstrap form control class to each widget
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'

    class Meta:
        model = Content
        # fields = ['name', 'page_url', 'page_section', 'priority', 'status', 'company', 'schedules']
        fields = '__all__'
        widgets = {
            'page_section': forms.Select(choices=PAGE_SECTION_CHOICES),
            'status': forms.Select(choices=STATUS_CHOICES),
            'content_type': forms.Select(choices=CONTENT_TYPE_CHOICES),
        }


PieceFormset = forms.modelformset_factory(
    Piece,
    fields=('key', 'value', 'upload'),
    extra=0,
    widgets={
        'key': forms.TextInput(attrs={'class': 'form-control mb-2', 'readonly': True}),
        'value': forms.Textarea(attrs={'class': 'form-control mb-2', 'rows': 3}),
    }
)
