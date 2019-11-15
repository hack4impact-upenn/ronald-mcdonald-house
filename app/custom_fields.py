from wtforms.fields import Field
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets import HiddenInput, TextArea
from wtforms.compat import text_type

from .models import Hospital

class CustomSelectField(Field):
    widget = HiddenInput()

    def __init__(self, label='', validators=None, multiple=False,
                 choices=[], allow_custom=True, **kwargs):
        super(CustomSelectField, self).__init__(label, validators, **kwargs)
        self.multiple = multiple
        self.choices = choices
        self.allow_custom = allow_custom

    def _value(self):
        return self.data if self.data is not None else ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[1]
            self.raw_data = [valuelist[1]]
        else:
            self.data = ''


class CustomModelSelectField(Field):
    widget = HiddenInput()

    def __init__(self, label=None, validators=None, model=None, order_column=None, **kwargs):
        super(CustomModelSelectField, self).__init__(label, validators, **kwargs)
        query = model.query.order_by(order_column) if order_column else model.query
        self.choices = [str(data) for data in query.all()]

    def _value(self):
        return self.data if self.data is not None else ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[1]
            self.raw_data = [valuelist[1]]
        else:
            self.data = ''


class HospitalListField(Field):
    widget = TextArea()

    def _value(self):
        if self.data:
            return u'\n'.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split('\n')]
        else:
            self.data = []
