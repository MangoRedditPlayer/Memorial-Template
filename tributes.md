---
layout: default
title: Tribute Data Test
permalink: /tributes.html 
---

## Tribute Data Fetch Test

<div id="test-container">
    <p>Attempting to fetch data. Check the browser console (F12).</p>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const testContainer = document.getElementById('test-container');
    const csvUrl = "{{ site.memorial_settings.published_tributes_csv_url | escape }}";

    if (!csvUrl || csvUrl === "" || csvUrl === "YOUR_PUBLISHED_GOOGLE_SHEET_CSV_URL_HERE") {
        testContainer.innerHTML = "<p><strong>Error:</strong> Published Tributes CSV URL is not configured in _config.yml or is still the placeholder value.</p>";
        console.error("Published Tributes CSV URL is not configured or is placeholder.");
        return;
    }

    console.log("Attempting to fetch CSV from URL:", csvUrl);
    testContainer.innerHTML = "<p>Fetching data from: " + csvUrl + "<br>Check console for raw response text.</p>";

    fetch(csvUrl)
        .then(response => {
            console.log("Fetch response status:", response.status);
            console.log("Fetch response ok:", response.ok);
            // Log all response headers to see content-type etc.
            console.log("Response Headers:");
            response.headers.forEach((value, name) => {
                console.log(`${name}: ${value}`);
            });
            return response.text(); // Get the response body as text
        })
        .then(rawText => {
            console.log("-------------------------------------------");
            console.log("RAW TEXT RECEIVED (first 2000 characters):");
            console.log(rawText.substring(0, 2000));
            console.log("-------------------------------------------");
            console.log("Full raw text length:", rawText.length);

            if (rawText.toLowerCase().includes("<html") || rawText.toLowerCase().includes("<body") || rawText.toLowerCase().includes("<script")) {
                testContainer.innerHTML += "<p><strong>Warning: Fetched data appears to be HTML/JavaScript, not plain CSV.</strong> Please verify the 'Publish to web' settings in Google Sheets ensure it's outputting raw CSV and the correct URL is used.</p>";
                console.warn("Warning: Fetched data appears to be HTML/JavaScript!");
            } else if (rawText.trim().startsWith("Timestamp,Your Name,Your Memory or Tribute")) { // Or your actual header
                testContainer.innerHTML += "<p><strong>Success: Fetched data appears to be CSV.</strong> See console for raw text.</p>";
                console.log("Success: Fetched data appears to be CSV.");
            } else {
                testContainer.innerHTML += "<p><strong>Notice: Fetched data is not clearly CSV or HTML.</strong> See console for raw text.</p>";
                console.warn("Notice: Fetched data format is undetermined from this quick check.");
            }
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
            testContainer.innerHTML = "<p><strong>Fetch Error:</strong> " + error.message + ". Could not load data. Check console and ensure the CSV URL is correct and publicly accessible.</p>";
        });
});
</script>