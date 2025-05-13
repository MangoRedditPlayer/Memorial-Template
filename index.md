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