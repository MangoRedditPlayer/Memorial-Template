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
    // The following Liquid tag will be replaced by Jekyll with the actual URL from your _config.yml
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
    if (true) { 
        document.getElementById('tributes-container').innerHTML = "<p>Diagnostic Mode: Check browser developer console (F12) for 'Raw fetched text'.</p>";
        return; // Stop the script here
    }
    // ---- END OF NEW DIAGNOSTIC CODE ----
            tributesContainer.innerHTML = ''; // Clear "Loading..." message
            
            // Split CSV text into rows. Google Sheets CSV often uses \r\n or \n.
            // .trim() removes leading/trailing whitespace from the whole CSV text.
            // .split(/\r\n|\n|\r/) splits by any common newline sequence.
            // .slice(1) removes the header row from the CSV.
            const rows = csvText.trim().split(/\r\n|\n|\r/).slice(1); 

            if (rows.length === 0 || (rows.length === 1 && rows[0].trim() === '')) {
                tributesContainer.innerHTML = "<p>No tributes have been shared yet. Please check back soon.</p>";
                return;
            }

            rows.forEach((rowStr, index) => {
                if (rowStr.trim() === '') return; // Skip any completely empty rows

                // Basic CSV parsing: Split by comma. 
                // This simple parser assumes commas are not within fields, 
                // or if they are, fields are properly quoted by Google Sheets.
                const columns = rowStr.split(',').map(field => {
                    // Trim quotes if field is quoted (e.g., "field data")
                    if (field.startsWith('"') && field.endsWith('"')) {
                        // Remove leading/trailing quotes and replace escaped double quotes ("") with a single double quote (")
                        return field.substring(1, field.length - 1).replace(/""/g, '"'); 
                    }
                    return field.trim(); // Trim whitespace from unquoted fields
                });

                if (columns.length >= 3) { // Expecting at least Timestamp, Name, Comment
                    const timestamp = columns[0]; // Already trimmed
                    const name = columns[1];      // Already trimmed
                    const comment = columns[2];   // Already trimmed

                    if (name && comment) { // Only proceed if name and comment are not empty
                        const article = document.createElement('article');
                        article.className = 'tribute-item';

                        // 1. Name
                        const nameHeader = document.createElement('h4'); 
                        nameHeader.className = 'tribute-name';
                        nameHeader.textContent = name;
                        article.appendChild(nameHeader);

                        // 2. Comment (Memory/Tribute)
                        const commentParagraph = document.createElement('p');
                        commentParagraph.className = 'tribute-comment';
                        commentParagraph.textContent = comment; // Relies on CSS `white-space: pre-wrap;` for line breaks
                        article.appendChild(commentParagraph);

                        // 3. Timestamp (Date)
                        if (timestamp) {
                            const dateParagraph = document.createElement('p');
                            dateParagraph.className = 'tribute-date';
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
                            dateParagraph.textContent = formattedDate;
                            article.appendChild(dateParagraph);
                        }
                        
                        tributesContainer.appendChild(article);

                        // Add <hr class="tribute-divider"> after each item, except the last one effectively
                        if (index < rows.length - 1) {
                            // Check if the next row is not just whitespace to avoid trailing hr
                            let nextRowIsNotEmpty = false;
                            for (let i = index + 1; i < rows.length; i++) {
                                if (rows[i].trim() !== '') {
                                    nextRowIsNotEmpty = true;
                                    break;
                                }
                            }
                            if (nextRowIsNotEmpty) {
                                const hr = document.createElement('hr');
                                hr.className = 'tribute-divider';
                                tributesContainer.appendChild(hr);
                            }
                        }
                    }
                } else {
                    console.warn("Skipping malformed CSV row (not enough columns):", rowStr);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching or processing tributes CSV:', error);
            tributesContainer.innerHTML = "<p><em>Could not load tributes at this time. There might be an issue with the data source or network. Please try again later.</em></p>";
        });
});
</script>