# ---> https://pypi.org/project/bleach/

import bleach

bcs = bleach.clean('an <script>evil()</script> example')
u'an &lt;script&gt;evil()&lt;/script&gt; example'

bcl = bleach.linkify('an http://example.com url')
u'an <a href="http://example.com" rel="nofollow">http://example.com</a> url'

print(bcs)
print(bcl)

