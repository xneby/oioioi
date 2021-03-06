import json
import urllib2

from django import forms
from django.core.validators import URLValidator
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from oioioi.problems.forms import ProblemUploadForm


class RemoteProblemForm(ProblemUploadForm):
    url = forms.CharField(
        label=_("Task URL"),
        widget=forms.TextInput(attrs={'class': 'input-xxlarge'}),
        validators=[URLValidator])

    def __init__(self, clients, *args, **kwargs):
        super(RemoteProblemForm, self).__init__(*args, **kwargs)
        self.clients = clients

        help_text = render_to_string('sharingcli/form-help.html',
            {'clients': clients})
        self.fields['url'].help_text = mark_safe(help_text)

    def clean_url(self):
        url = self.cleaned_data['url']
        for client in self.clients:
            if url.startswith(client.site_url):
                break
        else:
            raise forms.ValidationError("'%s'  %s"%(url, str([c.site_url for c in self.clients])))

        try:
            # pylint: disable=undefined-loop-variable
            response = client.make_request('taskinfo', {'query': url},
                timeout=10)
            response = json.loads(response.read())
            self.cleaned_data['client'] = client
            self.cleaned_data['task_id'] = response['id']
            return url
        except urllib2.HTTPError, e:
            raise forms.ValidationError('HTTP Error: %s'%(str(e)))
            if e.code == 404:
                raise forms.ValidationError(_("Not a task URL"))
            else:
                raise forms.ValidationError(_("Cannot connect to external "
                                              "site: %s") % (e,))
        except Exception, e:
            raise forms.ValidationError(_("Invalid server response: %s") %
                                        (e,))
