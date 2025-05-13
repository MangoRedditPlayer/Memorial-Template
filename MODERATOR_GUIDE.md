## Adding New Tributes (Text Memories)

Visitors will submit their memories, names, and optional contact information via the Google Form on the "Share Your Memory" page. These submissions will automatically appear as new rows in the Google Sheet you linked to your form.

To make these tributes appear on the "Tributes" page of the website, you'll need to manually copy the information from the Google Sheet into a special file in the website's code called `_data/comments.yml`.

**Steps to Add a New Tribute:**

1.  **Open Your Google Sheet:** Find the Google Sheet that collects responses from your "Share a Memory" form. New submissions will appear as new rows at the bottom. Each row will have a "Timestamp" (when it was submitted), the person's "Name," their "Memory or Tribute," and any optional information they provided (links, email, phone).

2.  **Review the Submission:** Read the memory and ensure it's appropriate for the memorial site.

3.  **Access `_data/comments.yml` File:**
    * This file is part of the website's code. The easiest way to edit it if you're not using Git on your desktop is through the GitHub website:
        * Go to your memorial website's repository on GitHub (e.g., `https://github.com/YOUR-USERNAME/Memorial-Template`).
        * You should see a list of files and folders. Click on the `_data` folder.
        * Inside the `_data` folder, click on the `comments.yml` file.
        * Click the pencil icon (✏️) near the top right of the file view to edit the file.

4.  **Add the New Tribute to `comments.yml`:**
    * `comments.yml` is a text file formatted in a specific way called YAML. Each tribute starts with a hyphen (`-`) and has indented lines for `name`, `date`, and `comment`.
    * Scroll to the bottom of the `comments.yml` file.
    * **On a new line**, add a new entry for the tribute. **Indentation is important! Use two spaces for each level of indentation. Do not use tabs.**

    * **Here's the format for each new entry:**
        ```yaml
        - name: "Full Name from Google Sheet"
          date: "Timestamp from Google Sheet (e.g., 5/13/2025 14:30:15)"
          comment: |
            The full text of the memory goes here.
            If the memory is multiple paragraphs, just make sure each new line
            of the comment starts with the same indentation (usually 4 spaces,
            meaning 2 spaces more than the word 'comment:'). The `|` symbol helps
            preserve line breaks.
          email: "Email from Google Sheet (optional, for your reference only)"
          phone: "Phone from Google Sheet (optional, for your reference only)"
        ```

    * **Example:** Let's say your Google Sheet has a new row:
        * Timestamp: `5/14/2025 09:15:22`
        * Your Name: `Alice Wonderland`
        * Your Memory or Tribute: `I will always remember their wonderful laugh. It could light up any room. We shared so many happy moments at the lake house.`
        * Your Email: `alice@example.com`
        * Your Phone: `(blank)`

    * You would add this to the end of `_data/comments.yml`:
        ```yaml
        # (previous entries in the file would be above this)
        - name: "Alice Wonderland"
          date: "5/14/2025 09:15:22"
          comment: |
            I will always remember their wonderful laugh. It could light up any room. 
            We shared so many happy moments at the lake house.
          email: "alice@example.com" 
          # phone is blank, so we can omit the phone line or leave it blank:
          # phone: "" 
        ```

    * **Important Notes for Formatting:**
        * Each new tribute starts with a `-` followed by a space.
        * `name:`, `date:`, `comment:`, `email:`, `phone:` must be indented with **two spaces** under the hyphen.
        * For the `comment:`, if it's a long or multi-paragraph memory, using `comment: |` (the pipe symbol) is recommended. Then, each line of the actual comment text should be indented with **four spaces** (two more than `comment:`).
        * Make sure the text for `name`, `date`, and `comment` is enclosed in quotes (`"..."`) if it contains special characters like colons (`:`), hyphens (`-`), or apostrophes (`'`) that might confuse YAML. Usually, it's safest to just use quotes for all text values. (Though for simple text as in the example, quotes are often not strictly needed for `name` and `date` if they don't contain special YAML characters). For `comment: |`, quotes are not needed around the block of text that follows.

5.  **Save the Changes:**
    * If editing on GitHub: Scroll to the bottom of the page. You'll see a "Commit changes" section.
    * Type a brief description of your change (e.g., "Add new tribute from Alice W.").
    * Click the "Commit changes" button.

6.  **Site Rebuild:** After you commit the changes, GitHub Pages will automatically rebuild your website (this might take 1-3 minutes).
7.  **Check the Live Site:** Once rebuilt, visit the "Tributes" page on your live memorial site. The new tribute should appear! Tributes are usually shown with the newest ones first.

**Tips:**
* It's a good idea to copy an existing entry in `comments.yml` and then modify it with the new information to ensure your formatting and indentation are correct.
* If the site doesn't update or shows an error after your changes, double-check `comments.yml` for any YAML syntax errors (indentation is the most common culprit).