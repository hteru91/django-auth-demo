from django import template
from django.utils.html import conditional_escape
from django.conf import settings
register = template.Library()

def user_display(user):
    func = getattr(settings, "ACCOUNT_USER_DISPLAY", lambda user: user.username)
    return func(user)

class UserDisplayNode(template.Node):
    
    def __init__(self, user, as_var=None):
        self.user_var = template.Variable(user)
        self.as_var = as_var
    
    def render(self, context):
        user = self.user_var.resolve(context)
        
        display = user_display(user)
        
        if self.as_var:
            context[self.as_var] = display
            return ""
        return conditional_escape(display)


@register.tag(name="user_display")
def do_user_display(parser, token):
    """
    Example usage::
    
        {% user_display user %}
    
    or if you need to use in a {% blocktrans %}::
    
        {% user_display user as user_display}
        {% blocktrans %}{{ user_display }} has sent you a gift.{% endblocktrans %}
    
    """
    bits = token.split_contents()
    
    if len(bits) == 2:
        user = bits[1]
        as_var = None
    elif len(bits) == 4:
        user = bits[1]
        as_var = bits[3]
    else:
        raise template.TemplateSyntaxError("'%s' takes either two or four arguments" % bits[0])
    
    return UserDisplayNode(user, as_var)
