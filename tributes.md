---
layout: default
title: Shared Tributes to {{ site.memorial_settings.deceased_name }}
permalink: /tributes.html 
---

## Shared Tributes & Memories

Here are the heartfelt tributes and memories shared by family and friends. New tributes typically appear here shortly after being submitted. If you believe a tribute needs attention, please contact the site administrator.

<div class="tributes-list" id="tributes-container">
    <p>Loading tributes...</p>
    </div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const tributesContainer = document.getElementById('tributes-container');
    const csvUrl = "{{ site.memorial_settings.published_tributes_csv_url | escape }}";

    if (!csvUrl || csvUrl === "" || csvUrl === "YOUR_PUBLISHED_GOOGLE_SHEET_CSV_URL_HERE") {
        tributesContainer.innerHTML = "<p><em>The tributes feed is not yet configured by the site administrator. Please check back later.</em></p>";
        console.error("Published Tributes CSV URL is not configured in _config.yml or is still the placeholder value.");
        return;
    }

    fetch(csvUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status + ' ' + response.statusText);
            }
            return response.text();
        })
        .then(csvText => {
            tributesContainer.innerHTML = ''; // Clear "Loading..." message
            
            const rows = csvText.trim().split(/\r\n|\n|\r/).slice(1); // Remove header row

            if (rows.length === 0 || (rows.length === 1 && rows[0].trim() === '')) {
                tributesContainer.innerHTML = "<p>No tributes have been shared yet. Please check back soon.</p>";
                return;
            }

            rows.forEach((rowStr, index) => {
                if (rowStr.trim() === '') return; 

                const columns = rowStr.split(',').map(field => {
                    if (field.startsWith('"') && field.endsWith('"')) {
                        return field.substring(1, field.length - 1).replace(/""/g, '"');
                    }
                    return field;
                });

                if (columns.length >= 3) {
                    const timestamp = columns[0].trim();
                    const name = columns[1].trim();
                    const comment = columns[2].trim();

                    if (name && comment) { 
                        const article = document.createElement('article');
                        article.className = 'tribute-item';

                        // 1. Name
                        const nameHeader = document.createElement('h4'); // Using h4 for the name
                        nameHeader.className = 'tribute-name';
                        nameHeader.textContent = name;
                        article.appendChild(nameHeader);

                        // 2. Comment (Memory/Tribute)
                        const commentParagraph = document.createElement('p');
                        commentParagraph.className = 'tribute-comment';
                        commentParagraph.textContent = comment; // CSS `white-space: pre-wrap;` will handle line breaks
                        article.appendChild(commentParagraph);

                        // 3. Timestamp (Date)
                        if (timestamp) {
                            const dateParagraph = document.createElement('p');
                            dateParagraph.className = 'tribute-date';
                            let formattedDate = 'Date not available';
                            try {
                                const dateObj = new Date(timestamp);
                                if (!isNaN(dateObj.getTime())) {
                                    formattedDate = dateObj.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) + ' ' +
                                                    dateObj.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', hour12: true });
                                } else {
                                    formattedDate = timestamp; 
                                }
                            } catch (e) {
                                formattedDate = timestamp; 
                                console.warn("Could not parse date:", timestamp, e);
                            }
                            dateParagraph.textContent = formattedDate;
                            article.appendChild(dateParagraph);
                        }
                        
                        tributesContainer.appendChild(article);

                        if (index < rows.length - 1) {
                            if (rows[index+1] && rows[index+1].trim() !== '') {
                                const hr = document.createElement('hr');
                                hr.className = 'tribute-divider';
                                tributesContainer.appendChild(hr);
                            }
                        }
                    }
                } else {
                    console.warn("Skipping malformed row:", rowStr, columns);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching or processing tributes CSV:', error);
            tributesContainer.innerHTML = "<p><em>Could not load tributes at this time. There might be an issue with the data source or network. Please try again later.</em></p>";
        });
});
</script>