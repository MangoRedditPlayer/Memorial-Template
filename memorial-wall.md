---
# memorial-wall.md
layout: default
title: Memorial Wall for {{ site.memorial_settings.deceased_name }}
permalink: /memorial-wall.html # Or /memorial-wall/
---

## Shared Memories of {{ site.memorial_settings.deceased_name }}

Welcome to the Memorial Wall. This is a special place for family and friends to share heartfelt tributes, stories, photos, and videos. Your contributions help build a beautiful and lasting testament to the life of {{ site.memorial_settings.deceased_name }}.

---

**How to Share Your Memory Below:**

We use the Disqus commenting system to collect memories. To post as a guest (without creating a Disqus account), please follow these steps in the box below:

1.  **Click into the "Start the discussion..." or "Join the discussion..." box.**
2.  **Type your memory.**
3.  **Enter Your Name:** Type the name you'd like to appear with your memory in the "Name" field.
4.  **Enter Your Email:** You'll also need to provide an email address (this is usually just for verification/notification and not publicly displayed by default with guest comments).
5.  **IMPORTANT - Post as Guest:**
    * Look for a checkbox that says something like **"I'd rather post as a guest"**. Make sure this box is **CHECKED**.
6.  **"I'm not a robot":** You may need to complete a simple CAPTCHA (like checking a box) to confirm you're human. This helps prevent spam.
7.  **Submit:** Click the arrow button (or similar "Post" button) to submit your memory.

**Sharing Photos or Videos:**
* Please upload your photos or videos to a sharing service first (like Google Photos, YouTube, Imgur, Facebook with public sharing, etc.).
* Copy the **share link (URL)** for your photo or video.
* **Paste that link directly into your comment text.** Disqus will often automatically create a preview or embed the media.

*Your contributions are deeply appreciated. Comments typically appear immediately below. The site administrator can review all shared content.*

---

{% if site.disqus_shortname %}
<div id="disqus_thread"></div>
<script>
    var disqus_config = function () {
        this.page.url = "{{ page.url | absolute_url }}";  
        this.page.identifier = "{{ page.url | relative_url }}"; 
        this.page.title = "{{ page.title | escape }}";
    };
    (function() { 
    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
    dsq.src = '//{{ site.disqus_shortname }}.disqus.com/embed.js'; 
    dsq.setAttribute('data-timestamp', +new Date());
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
{% else %}
<p><em>Disqus comments are not configured. Please set the `disqus_shortname` in `_config.yml`.</em></p>
{% endif %}