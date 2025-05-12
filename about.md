---
# about.md
layout: default
title: About {{ site.memorial_settings.deceased_name }}
permalink: /about.html # Or /about/ if you prefer clean URLs and server supports it
---

## About {{ site.memorial_settings.deceased_name }}

{% if site.memorial_settings.birth_date and site.memorial_settings.passing_date %}
**Born:** {{ site.memorial_settings.birth_date }}
**Departed:** {{ site.memorial_settings.passing_date }}
{% endif %}

---
*(Template user: Replace this section with a biography, cherished stories, and details about {{ site.memorial_settings.deceased_name }}. You can use Markdown for formatting, add photos, etc.)*

Some ideas for content:
* Early life and family background.
* Passions, hobbies, and significant life events.
* Career, accomplishments, or community involvement.
* Personal anecdotes that highlight their personality.
* What made them special to you and others.

You can structure this page with further subheadings using `### Subheading Title`.