from django.forms import FileField, Form, ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from pretalx.schedule.models import Schedule


class ScheduleReleaseForm(ModelForm):
    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        self.fields['version'].required = True

    def clean_version(self):
        version = self.cleaned_data.get('version')
        if self.event.schedules.filter(version__iexact=version).exists():
            raise ValidationError(_('This schedule version was used already.'))
        return version

    class Meta:
        model = Schedule
        fields = ('version',)


class ScheduleImportForm(Form):
    upload = FileField()

    class Meta:
        fields = ('upload',)
