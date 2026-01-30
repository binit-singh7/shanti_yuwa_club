# 🚀 Quick Start: Deploy to Render

Follow these steps to deploy your site in ~1 hour!

## ✅ Prerequisites Checklist

Before starting, make sure you have:

- [ ] GitHub account
- [ ] Render account (sign up at render.com)
- [ ] Gmail app password ready (or will create one)
- [ ] Code pushed to GitHub

---

## 📋 Step-by-Step Guide

### 1️⃣ Generate Secret Key (2 minutes)

Open terminal and run:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** - you'll need it later!

---

### 2️⃣ Get Gmail App Password (5 minutes)

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already)
3. Search for "App passwords"
4. Create new app password:
   - App: Mail
   - Device: Other (Custom name): "Shanti Yuwa Club"
5. **Copy the 16-character password**

---

### 3️⃣ Push to GitHub (5 minutes)

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Production ready deployment"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/shanti_yuwa_club.git
git branch -M main
git push -u origin main
```

> ⚠️ **Important:** Verify `.env` is NOT in your GitHub repo!

---

### 4️⃣ Create Render Account (2 minutes)

1. Go to: https://render.com
2. Click **"Get Started"**
3. Sign up with GitHub (easiest)
4. Authorize Render to access your repos

---

### 5️⃣ Create PostgreSQL Database (5 minutes)

1. In Render Dashboard: **New +** → **PostgreSQL**
2. Settings:
   - **Name:** `shanti-yuwa-db`
   - **Database:** `shanti_yuwa_club`
   - **Region:** Singapore (closest to Nepal)
   - **Plan:** Free
3. Click **"Create Database"**
4. Wait for it to provision (~2 min)
5. **Copy "Internal Database URL"** (starts with `postgresql://`)

---

### 6️⃣ Create Web Service (10 minutes)

1. In Render Dashboard: **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure:

   **Basic Info:**
   - Name: `shanti-yuwa-club`
   - Region: Singapore
   - Branch: `main`
   - Runtime: Python 3

   **Build & Deploy:**
   - Build Command: `./build.sh`
   - Start Command: `gunicorn shanti_yuwa_club.wsgi:application`

   **Plan:**
   - Free (or $7/month for always-on)

4. **DON'T click Create yet!** → Go to "Advanced" first

---

### 7️⃣ Set Environment Variables (5 minutes)

In the "Environment Variables" section, add these:

| Key                      | Value                            |
| ------------------------ | -------------------------------- |
| `DJANGO_SECRET_KEY`      | Paste from Step 1                |
| `DJANGO_DEBUG`           | `False`                          |
| `DJANGO_SETTINGS_MODULE` | `shanti_yuwa_club.settings_prod` |
| `DATABASE_URL`           | Paste from Step 5                |
| `EMAIL_HOST_USER`        | `shantiyuwac@gmail.com`          |
| `EMAIL_HOST_PASSWORD`    | Paste from Step 2                |
| `ALLOWED_HOSTS`          | `.onrender.com`                  |
| `PYTHON_VERSION`         | `3.12.0`                         |

---

### 8️⃣ Deploy! (10 minutes)

1. Click **"Create Web Service"**
2. Watch the build logs (this is exciting! 🎉)
3. Wait for deployment to complete (~5-10 min)
4. You'll see: **"Your service is live 🎉"**

---

### 9️⃣ Create Admin Account (3 minutes)

1. In your Render service, go to **"Shell"** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter:
   - Username: (your choice)
   - Email: (your email)
   - Password: (strong password)

---

### 🔟 Test Your Site! (5 minutes)

Visit: `https://shanti-yuwa-club.onrender.com`

**Test checklist:**

- [ ] Homepage loads correctly
- [ ] CSS/images work
- [ ] Admin panel works: `/admin`
- [ ] Try registering a test member
- [ ] Send a test contact form

---

## 🎉 You're Live!

Your website is now live at:
**https://shanti-yuwa-club.onrender.com**

---

## 🔄 Updating Your Site

To update your site after making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Render will automatically redeploy! ✨

---

## 📱 Adding Custom Domain (Later)

When you get a domain:

1. In Render: Settings → Custom Domains → Add
2. Follow DNS instructions
3. Update environment variable:
   ```
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,.onrender.com
   ```

---

## ⚠️ Troubleshooting

**Build fails?**

- Check build logs for errors
- Verify all environment variables are set
- Ensure `build.sh` has correct permissions

**Site not loading?**

- Check if service is "Live" in Render dashboard
- View logs for errors
- Verify DATABASE_URL is correct

**Static files missing?**

- Check if `collectstatic` ran in build logs
- Verify STATIC_ROOT in settings

**Need help?**

- Check full guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Render docs: https://render.com/docs
- Django docs: https://docs.djangoproject.com

---

## 💰 Free Tier Info

**Limitations:**

- Sleeps after 15 min inactivity
- Wakes in ~30 seconds
- 750 hours/month (enough for 1 service)

**Upgrade to $7/month for:**

- Always-on (no sleeping)
- Faster performance
- Priority support

---

**Questions?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide!

**Good luck! 🚀**
