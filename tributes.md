---
layout: default
title: Shared Tributes to {{ site.memorial_settings.deceased_name }}
permalink: /tributes.html 
---

## Shared Tributes & Memories

Here are the heartfelt tributes and memories shared by family and friends. New tributes typically appear here shortly after being submitted and reviewed. If you believe a tribute needs attention, please contact the site administrator.

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
            
            // Split CSV text into rows. Google Sheets CSV often uses \r\n or \n.
            const rows = csvText.trim().split(/\r\n|\n|\r/).slice(1); // Remove header row

            if (rows.length === 0 || (rows.length === 1 && rows[0].trim() === '')) {
                tributesContainer.innerHTML = "<p>No tributes have been shared yet, or they are pending review. Please check back soon.</p>";
                return;
            }

            rows.forEach((rowStr, index) => {
                if (rowStr.trim() === '') return; // Skip empty rows

                // Basic CSV parsing: Split by comma. 
                // This assumes commas are not within fields, or if they are, fields are quoted.
                // Google Sheets usually handles quoting well for its CSV export.
                // A more robust solution would use a proper CSV parsing library if needed.
                const columns = rowStr.split(',').map(field => {
                    // Trim quotes if field is quoted
                    if (field.startsWith('"') && field.endsWith('"')) {
                        return field.substring(1, field.length - 1).replace(/""/g, '"'); // Handle escaped quotes "" as "
                    }
                    return field;
                });

                if (columns.length >= 3) {
                    // Assuming Timestamp in col 0, Name in col 1, Comment in col 2
                    // As per: =QUERY('All Submissions'!A:C, "SELECT A, B, C ...", 1)
                    const timestamp = columns[0].trim();
                    const name = columns[1].trim();
                    const comment = columns[2].trim();

                    if (name && comment) { // Only proceed if name and comment are not empty
                        const article = document.createElement('article');
                        article.className = 'tribute-item';

                        const commentParagraph = document.createElement('p');
                        // Preserve line breaks from the comment.
                        // Newlines from Sheets/CSV are typically \n.
                        // CSS `white-space: pre-wrap;` on `.tribute-item p` handles display.
                        // For safety, escape HTML in comment text before setting textContent.
                        // Or, if you trust the source and want HTML, set innerHTML carefully.
                        commentParagraph.textContent = `"${comment}"`; // Using textContent is safer. CSS will handle line breaks.

                        const footer = document.createElement('footer');
                        const nameStrong = document.createElement('strong');
                        nameStrong.className = 'tribute-name';
                        nameStrong.textContent = name;
                        footer.appendChild(nameStrong);

                        if (timestamp) {
                            const dateEm = document.createElement('em');
                            dateEm.className = 'tribute-date';
                            let formattedDate = 'Date not available';
                            try {
                                const dateObj = new Date(timestamp);
                                // Check if dateObj is valid
                                if (!isNaN(dateObj.getTime())) {
                                    formattedDate = dateObj.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) + ' ' +
                                                    dateObj.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', hour12: true });
                                } else {
                                    formattedDate = timestamp; // Fallback to raw timestamp if parsing fails
                                }
                            } catch (e) {
                                formattedDate = timestamp; // Fallback if Date object creation fails
                                console.warn("Could not parse date:", timestamp, e);
                            }
                            dateEm.textContent = ` - ${formattedDate}`;
                            footer.appendChild(dateEm);
                        }
                        
                        article.appendChild(commentParagraph);
                        article.appendChild(footer);
                        tributesContainer.appendChild(article);

                        // Add <hr class="tribute-divider"> after each item, except the last one
                        if (index < rows.length - 1) {
                             // Check if the next row is not empty to avoid trailing hr for potentially empty last lines
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