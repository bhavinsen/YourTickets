from django.template.defaulttags import register
from django.utils.safestring import mark_safe

@register.simple_tag(name='ga')
def ga(section):

    if section == 'head':
     return mark_safe("""<!-- Google Tag Manager -->
            <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer','GTM-TFR3HM7');</script>
            <!-- End Google Tag Manager -->""")

    elif section == 'body':
        return mark_safe("""<!-- Google Tag Manager (noscript) -->
                <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TFR3HM7"
                height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
                <!-- End Google Tag Manager (noscript) -->""")