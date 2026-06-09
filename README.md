# Eyeball Portfolio

Fabrice Klohoun's portfolio, creator network and video library, deployed with
Streamlit Community Cloud.

## Run locally

```bash
python3 -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Sign in at <https://share.streamlit.io/>.
2. Select **Create app**.
3. Choose the GitHub repository containing this project.
4. Set the branch to `main`.
5. Set the main file path to `streamlit_app.py`.
6. Open **Advanced settings** and add the email secrets below.
7. Deploy the app.

Every push to `main` will automatically update the live Streamlit site.

## Contact form email

The contact form reads SMTP credentials from Streamlit secrets. In Streamlit
Community Cloud, open the app's **Settings > Secrets** and add:

```toml
[email]
host = "smtp.gmail.com"
port = 465
username = "klohounfabrice@gmail.com"
password = "YOUR_GMAIL_APP_PASSWORD"
recipient = "klohounfabrice@gmail.com"
```

Use a Google app password, not the normal Gmail account password. Google
requires two-step verification before an app password can be created.

Never commit `.streamlit/secrets.toml`; it is intentionally ignored by Git.
