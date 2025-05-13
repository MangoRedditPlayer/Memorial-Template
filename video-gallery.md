---
layout: default
title: Video Tributes for {{ site.memorial_settings.deceased_name }}
permalink: /videos.html # Ensures it generates as videos.html
---

## Video Memories

A collection of video tributes and memories shared by family and friends, curated by the site administrator.

<div class="video-gallery">
{% if site.data.videos and site.data.videos.size > 0 %}
    {% for video in site.data.videos %}
    <article class="video-item">
        {% if video.caption %}<h4>{{ video.caption | escape }}</h4>{% endif %}
        <div class="video-embed-container">
            <iframe 
                src="{{ video.video_url }}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen
                title="Embedded video {{ video.caption | default: 'tribute' | escape }}">
            </iframe>
        </div>
        {% if video.submitter_name %}<p><em>Shared by {{ video.submitter_name | escape }}</em></p>{% endif %}
    </article>
    {% endfor %}
{% else %}
    <p>No videos have been added to the gallery yet, or they are pending review. Please check back soon.</p>
{% endif %}
</div>