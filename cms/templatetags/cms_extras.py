from django import template
register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='addreadonly')
def addreadonly(field):
    return field.as_widget(attrs={"readonly": True})


@register.filter(name='addhidden')
def addhidden(field):
    return field.as_widget(attrs={"hidden": True})
