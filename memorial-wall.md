---
# memorial-wall.md
layout: default
title: Memorial Wall for {{ site.memorial_settings.deceased_name }}
permalink: /memorial-wall.html # Or /memorial-wall/
---

## Shared Memories of {{ site.memorial_settings.deceased_name }}

Welcome to the Memorial Wall. Here, family and friends can share heartfelt tributes, stories, photos, and videos.

**Sharing Memories:**
* Use the comment section below to add your memory.
* Guest commenting is enabled, so you shouldn't need to log in (you might be asked for a name/email).
* To share photos or videos, please upload them to a sharing service (like Google Photos, YouTube, Imgur, etc.), get a public share link (URL), and **paste that link** into your comment text. Disqus will often automatically create a preview or embed the media.

*Your contributions help build a beautiful and lasting tribute. Comments appear below, and the site administrator can review them.*

---

{% if site.disqus_shortname %}
<div id="disqus_thread"></div>
<script>
    /**
    * RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
    * LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables    */

    var disqus_config = function () {
        // Replace PAGE_URL with your page's canonical URL variable
        this.page.url = "{{ page.url | absolute_url }}";  
        // Replace PAGE_IDENTIFIER with your page's unique identifier variable
        // Using page.url is a common default if you don't have other unique IDs
        this.page.identifier = "{{ page.url | relative_url }}"; 
        // Optional: Replace PAGE_TITLE with the page's title variable
        this.page.title = "{{ page.title | escape }}";
    };

    (function() { // DON'T EDIT BELOW THIS LINE
    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
    // Use the shortname from _config.yml
    dsq.src = '//{{ site.disqus_shortname }}.disqus.com/embed.js'; 
    dsq.setAttribute('data-timestamp', +new Date());
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
{% else %}
<p><em>Disqus comments are not configured. Please set the `disqus_shortname` in `_config.yml`.</em></p>
{% endif %}