# 🚀 DEPLOY IN 2 MINUTES

## Option 1: Render (Recommended - FREE)

### Step 1: Go to Render
Visit: https://dashboard.render.com/

### Step 2: Sign In
- Click "Get Started for Free"
- Sign in with GitHub

### Step 3: Create Web Service
1. Click "New +" → "Web Service"
2. Connect GitHub: Select `iamvishno/ai-chatbot`
3. Click "Connect"

### Step 4: Configure (Auto-filled from render.yaml)
- **Name**: `ai-chatbot` (or any name you want)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free

### Step 5: Add Environment Variable
Click "Advanced" → "Add Environment Variable"
```
Key: OPENAI_API_KEY
Value: [PASTE YOUR OPENAI API KEY HERE]
```
**Important**: Use your actual OpenAI API key from https://platform.openai.com/api-keys

### Step 6: Deploy!
Click "Create Web Service"

**Your app will be live in ~2 minutes at:**
```
https://ai-chatbot-xxxx.onrender.com
```

---

## Option 2: Railway (Also FREE)

### Step 1: Go to Railway
Visit: https://railway.app/

### Step 2: New Project
1. Click "Start a New Project"
2. Select "Deploy from GitHub repo"
3. Connect GitHub and select `iamvishno/ai-chatbot`

### Step 3: Add Environment Variables
In the Railway dashboard:
1. Click "Variables" tab
2. Add:
   - `OPENAI_API_KEY` = your API key
   - `ENVIRONMENT` = production

### Step 4: Deploy
Railway automatically deploys!

**Your app will be live at:**
```
https://ai-chatbot-production.up.railway.app
```

---

## Option 3: Docker (Any Cloud)

### Build & Run Locally
```bash
docker build -t ai-chatbot .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e ENVIRONMENT=production \
  ai-chatbot
```

### Deploy to Cloud
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean

---

## 🎯 After Deployment

1. Visit your deployment URL
2. Test the chatbot
3. Share your URL!
4. Monitor usage in OpenAI dashboard

---

## 💡 Tips

- **Free Tiers**: Both Render and Railway offer free tiers
- **Custom Domain**: Add your domain in platform settings
- **Monitoring**: Both platforms provide built-in logs
- **Auto-Deploy**: Push to GitHub = auto-deploy

---

**Choose Render or Railway and deploy NOW!** 🚀
