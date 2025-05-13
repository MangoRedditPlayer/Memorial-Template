# Moderator Guide for Memorial Template

This guide helps you set up and manage your memorial website using this template.

## Initial Setup

1.  **Configure `_config.yml`:**
    * Open `_config.yml`.
    * Under `memorial_settings:`, change `deceased_name:` to your loved one's full name.
    * **CRITICAL:** Change `site_password:` to a unique, secure password for accessing the site. Remember this password!
    * Under `site:`, update `url:` to the final URL where the site will be hosted (e.g., `https://yourusername.github.io/your-repo-name`). Ensure `baseurl:` is correct (`/your-repo-name` if it's a GitHub project page, or `""` for a root domain).
    * *(Optional)* Fill in other details like `birth_date`, `passing_date` under `memorial_settings` if desired.

2.  **Set Up Disqus for Comments (Memorial Wall):**
    * Go to [disqus.com](https://disqus.com) and sign up for a free account.
    * Choose "I want to install Disqus on my site".
    * Register your site: Give it a name (e.g., "Memorial for [Loved One's Name]") and choose a **unique shortname** (e.g., `memorial-for-[loved-one]`). **Write this shortname down.**
    * Select the Free plan.
    * Go to your Disqus Admin panel for the site you just registered.
    * Find the settings (e.g., Community -> Settings -> General).
    * **ENABLE Guest Commenting:** Check the box for "Allow guests to comment". Configure guest requirements (Name/Email).
    * **(Optional but Recommended):** Review other settings like enabling media attachments (if available), default sorting, profanity filters, etc.
    * Go back to your `_config.yml` file.
    * Find the line `disqus_shortname: ""` and paste **your unique Disqus shortname** between the quotes.

3.  **Deploy Site:** Commit and push your changes to GitHub. Follow GitHub Pages instructions to ensure it's building from the correct branch (`main`).

## Managing Content

* **Editing Site Pages (About, etc.):** Edit the Markdown files (`about.md`, `index.md`) directly, commit, and push changes.
* **Moderating Memorial Wall Comments:**
    * Log in to your Disqus account ([disqus.com/admin](https://disqus.com/admin)).
    * Select your memorial site.
    * Go to the "Moderate Comments" section.
    * Here you can approve, delete, mark as spam, or sometimes edit comments left by visitors. You will also receive email notifications for new comments if configured.
	
## Customizing Site Appearance (in `_config.yml`)

You can change the main colors of your memorial site by editing the `site_look:` section in `_config.yml`:

* `site_background_color:` Sets the overall background color for the site. Uses hex color codes (e.g., `"#333333"` for dark grey, `"#ffffff"` for white).
* `site_text_color:` Sets the main text color. Choose a color that contrasts well with your `site_background_color`.
* `link_color:` Sets the color for clickable links.
* `link_hover_color:` Sets the color for links when a mouse hovers over them.

**Example:**
```yaml
site_look:
  site_background_color: "#2c3e50"
  site_text_color: "#ecf0f1"
  link_color: "#3498db"
  link_hover_color: "#2980b9"

## Important Notes

* **Site Password:** The `site_password` in `_config.yml` provides basic privacy, not high security. If your GitHub repository is public, the password is technically visible in the config file.
* **Disqus Ads:** The free Disqus plan shows advertisements. Paid plans remove ads.
* **Media Sharing:** Remind users to share media by pasting links into their Disqus comments.