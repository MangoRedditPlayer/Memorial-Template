---
# memorial-wall.md
layout: default
title: Memorial Wall for {{ site.memorial_settings.deceased_name }}
permalink: /memorial-wall.html # Or /memorial-wall/ if you prefer that URL structure
---

## Shared Memories of {{ site.memorial_settings.deceased_name }}

Welcome to the Memorial Wall. This is a special place for family and friends to share heartfelt tributes, stories, photos, and videos. Your contributions help build a beautiful and lasting testament to the life of {{ site.memorial_settings.deceased_name }}.

---

<div class="disqus-instructions" markdown="1">

<h3 style="margin-top: 0;">Sharing Your Memory Below: A Quick Guide</h3>

We're using the Disqus system (the box below this guide) to gather memories. These instructions are primarily for **posting as a GUEST** (without creating a Disqus account), which we recommend for simplicity. If you already have a Disqus account and prefer to use it, the steps will be similar.

1.  **Start Typing:** Click into the box below that says something like "Join the discussion..." or "Start the discussion..." and begin typing your memory.
2.  **Add Your Name:** After you type your memory, Disqus will show some new fields. In the **"Name"** field, please type the name you'd like to appear with your memory.
    * *(Heads up: As you type your name, a "Password" box might also appear. If you intend to post as a guest, you can simply **ignore this password box**.)*
3.  **Your Email:** You'll also be asked for an email address. This is generally for Disqus's system and isn't usually shown publicly with your guest comment.
4.  **Post as Guest (Important!):** Look carefully for a checkbox that says **"I'd rather post as a guest"**. Please **CHECK THIS BOX**. This ensures you don't accidentally create a Disqus account.
5.  **"I'm not a robot":** You might need to check a box or solve a simple puzzle (a CAPTCHA) to confirm you're human. This is a standard step to prevent spam.
6.  **Submit Your Memory:** Click the **submit button** (it often looks like a right-pointing arrow or says "Post").

**Sharing Photos or Videos (Easy with Links!):**

* The best way to share media is to upload it to a service first:
    * **Photos:** Google Photos (create a shareable link), Imgur, Flickr, a public Facebook photo, etc.
    * **Videos:** YouTube, Vimeo, a public Facebook video, etc.
* Once uploaded, get the **shareable link (URL)** for your photo or video.
* **Paste that link directly into the text of your memory** in the Disqus box. Disqus is pretty smart and will often automatically turn the link into a viewable image or an embedded video player!

*Your memories are precious to us. They usually appear right after you post. The site administrator can review all shared content.*

</div>

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