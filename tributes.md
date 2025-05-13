---
layout: default
title: Shared Tributes to {{ site.memorial_settings.deceased_name }}
permalink: /tributes.html # Ensures it generates as tributes.html
---

## Shared Tributes & Memories

Here are some of the heartfelt tributes and memories shared by family and friends, reviewed and curated by the site administrator.

<div class="tributes-list">
{% if site.data.comments and site.data.comments.size > 0 %}
    {% for item in site.data.comments reversed %} {# Show newest first if moderator adds to end of YAML #}
    <article class="tribute-item">
        <p>"{{ item.comment | nl2br | markdownify }}"</p>
        <footer>
            <strong class="tribute-name">{{ item.name | escape }}</strong>
            {% if item.date %}<em class="tribute-date"> - {{ item.date | escape }}</em>{% endif %}
        </footer>
    </article>
    <hr class="tribute-divider">
    {% endfor %}
{% else %}
    <p>No tributes have been shared yet, or they are pending review. Please check back soon.</p>
{% endif %}
</div>