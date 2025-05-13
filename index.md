---
layout: default
title: Welcome
permalink: /
---

## Welcome to the Memorial for {{ site.memorial_settings.deceased_name }}

This space is dedicated to celebrating the life and cherishing the memories of {{ site.memorial_settings.deceased_name }}.
{% if site.memorial_settings.welcome_message %}
{{ site.memorial_settings.welcome_message }}
{% else %}
Here, family and friends can share stories, photos, and videos, creating a lasting tribute.
{% endif %}

We invite you to explore:
* [Read more About {{ site.memorial_settings.deceased_name | split: " " | first }}]({{ '/about.html' | relative_url }})
* [Visit the Memorial Wall]({{ '/memorial-wall.html' | relative_url }}) to see shared tributes.
* [Learn How to Share Your Own Memory]({{ '/share-memory.html' | relative_url }})


{% if site.memorial_settings.birth_date and site.memorial_settings.passing_date %}
<p style="margin-top: 1.5em; font-style: italic;">
    {{ site.memorial_settings.deceased_name }}
    <br>
    {{ site.memorial_settings.birth_date }} – {{ site.memorial_settings.passing_date }}
</p>
{% endif %}