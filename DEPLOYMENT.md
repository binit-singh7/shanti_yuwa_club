# Deploying Shanti Yuwa Club to Render

This guide walks you through deploying your Django application to Render.com with PostgreSQL.

## Prerequisites

- [ ] GitHub account
- [ ] Render account (free tier is fine)
- [ ] Your code pushed to GitHub

---

## Step 1: Push Code to GitHub

1. **Initialize Git** (if not already done):

   ```bash
   git init
   git add .
   git commit -m "Initial commit - production ready"
   ```

2. **Create GitHub repository** and push:
   ```bash
   git remote add origin https://github.com/yourusername/shanti_yuwa_club.git
   git branch -M main
   git push -u origin main
   ```

> **Important:** Make sure `.env` is in `.gitignore` and NOT committed!

---

## Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (easiest option)
3. Authorize Render to access your repositories

---

## Step 3: Create PostgreSQL Database

1. From Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `shanti-yuwa-db`
   - **Database:** `shanti_yuwa_club`
   - **User:** (auto-generated)
   - **Region:** Singapore (closest to Nepal)
   - **Plan:** Free
3. Click **"Create Database"**
4. **Save the Internal Database URL** (you'll need this)

---

## Step 4: Create Web Service

1. From Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

   **Basic Settings:**
   - **Name:** `shanti-yuwa-club`
   - **Region:** Singapore
   - **Branch:** `main`
   - **Root Directory:** (leave blank)
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn shanti_yuwa_club.wsgi:application`

   **Plan:**
   - Select **Free** (or $7/month for always-on)

---

## Step 5: Set Environment Variables

In the Render web service settings, go to **"Environment"** tab and add:

```bash
DJANGO_SECRET_KEY=<generate-new-secret-key>
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=shanti_yuwa_club.settings_prod
DATABASE_URL=<paste-internal-database-url-from-step-3>
EMAIL_HOST_USER=shantiyuwac@gmail.com
EMAIL_HOST_PASSWORD=<your-gmail-app-password>
ALLOWED_HOSTS=.onrender.com
PYTHON_VERSION=3.12.0
```

### Generate SECRET_KEY:

Run this locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Get Gmail App Password:

1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Search "App passwords"
4. Generate password for "Mail"
5. Copy the 16-character password

---

## Step 6: Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start the server

3. **Wait 5-10 minutes** for first deployment

---

## Step 7: Create Superuser

After deployment, you need to create an admin account:

1. Go to your Render service → **"Shell"** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts to create admin account

---

## Step 8: Test Your Site

1. Visit your site: `https://shanti-yuwa-club.onrender.com`
2. Test:
   - [ ] Homepage loads
   - [ ] Static files (CSS/JS) work
   - [ ] Admin panel: `/admin`
   - [ ] Forms work
   - [ ] Email functionality

---

## Adding Custom Domain (Later)

When you get a domain:

1. **In Render:**
   - Go to Settings → Custom Domains
   - Add your domain (e.g., `shantiyuwaclub.org`)
   - Copy the CNAME record

2. **In your domain registrar:**
   - Add CNAME record pointing to Render

3. **Update environment variables:**
   ```bash
   ALLOWED_HOSTS=shantiyuwaclub.org,www.shantiyuwaclub.org,.onrender.com
   CUSTOM_DOMAIN=shantiyuwaclub.org
   ```

---

## Troubleshooting

### Build fails

- Check build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `build.sh` has execute permissions

### Static files not loading

- Check `STATIC_ROOT` in settings
- Verify `collectstatic` ran in build logs
- Check browser console for errors

### Database connection errors

- Verify `DATABASE_URL` is correct
- Check PostgreSQL database is running
- Ensure migrations ran successfully

### 500 errors

- Check application logs in Render
- Verify all environment variables are set
- Check `DEBUG=False` is set

---

## Maintenance

### View Logs

Go to Render Dashboard → Your Service → Logs

### Backup Database

Run locally (with production DATABASE_URL):

```bash
./backup_db.sh
```

### Update Code

Just push to GitHub:

```bash
git add .
git commit -m "Update message"
git push
```

Render auto-deploys!

---

## Free Tier Limitations

- Sleeps after 15 minutes of inactivity
- Wakes up in ~30 seconds on first request
- 750 hours/month free (enough for one service)
- Upgrade to $7/month for always-on

---

## Support

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- Community: https://community.render.com/

**Your site will be live at:** `https://shanti-yuwa-club.onrender.com` 🎉
