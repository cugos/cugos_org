from django import template
from django.conf import settings

register = template.Library()

def urchin():
    if settings.GOOGLE_ANALYTICS_CODE:
        code = """
        <script type="text/javascript">
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
        document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
        </script>"""
        
        code += """
        <script type="text/javascript">
        try {
        var pageTracker = _gat._getTracker("%s");
        pageTracker._trackPageview();
        } catch(err) {}</script>
        """ % settings.GOOGLE_ANALYTICS_CODE
        
        return code
    else:
        return '<!-- No Tracking Installed -->'

register.simple_tag(urchin)