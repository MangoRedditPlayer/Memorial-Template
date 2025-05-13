---
layout: default
title: Photo Gallery for {{ site.memorial_settings.deceased_name }}
permalink: /photos.html # Ensures it generates as photos.html
---

## Photo Memories

A collection of cherished photos shared by family and friends, curated by the site administrator. Click on an image to view it (behavior depends on how links are set up).

<div class="photo-gallery">
{% if site.data.photos and site.data.photos.size > 0 %}
    {% for photo in site.data.photos %}
    <figure class="photo-item">
        <a href="{{ photo.image_url }}" target="_blank" rel="noopener noreferrer">
            <img src="{{ photo.image_url }}" alt="{{ photo.caption | default: 'Photo submitted by' | append: ' ' | append: photo.submitter_name | default: 'Shared photo' | escape }}">
        </a>
        {% if photo.caption %}
        <figcaption>{{ photo.caption | escape }} {% if photo.submitter_name %}<em>(Shared by {{ photo.submitter_name | escape }})</em>{% endif %}</figcaption>
        {% elsif photo.submitter_name %}
        <figcaption><em>Shared by {{ photo.submitter_name | escape }}</em></figcaption>
        {% endif %}
    </figure>
    {% endfor %}
{% else %}
    <p>No photos have been added to the gallery yet, or they are pending review. Please check back soon.</p>
{% endif %}
</div>