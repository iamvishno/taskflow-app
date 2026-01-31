# 🤖 AI Chatbot - Production-Ready OpenAI Application

A modern, production-ready conversational AI chatbot built with FastAPI and OpenAI's GPT models. Features a beautiful responsive interface, rate limiting, security headers, and comprehensive error handling.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7)](https://render.com)

> **🚀 Quick Deploy**: Click the button above and deploy to Render in 2 minutes!

## 📱 Repository

**GitHub**: [https://github.com/iamvishno/ai-chatbot](https://github.com/iamvishno/ai-chatbot)

## Features

### Core Functionality
- **Modern Chat Interface**: Clean, responsive UI with real-time messaging
- **Multiple AI Models**: GPT-3.5 Turbo, GPT-4, GPT-4 Turbo, GPT-4o
- **Conversation History**: Maintains context throughout chat sessions
- **Token Usage Tracking**: Monitor API usage in real-time

### Production Features
- **Rate Limiting**: Prevents API abuse (configurable)
- **Security Headers**: HSTS, XSS protection, frame options
- **Error Handling**: Comprehensive error logging and user-friendly messages
- **Health Checks**: `/health` and `/api/status` endpoints for monitoring
- **CORS Configuration**: Secure cross-origin resource sharing
- **Request Validation**: Input sanitization and validation with Pydantic
- **Logging**: Structured logging for debugging and monitoring

## Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **AI**: OpenAI API (GPT models)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Server**: Uvicorn (ASGI)
- **Deployment**: Docker, Render, Railway, Vercel ready

## Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/iamvishno/ai-chatbot.git
cd ai-chatbot
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

5. **Run the application**
```bash
python main.py
```

6. **Open browser**
```
http://localhost:8000
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Yes |
| `ENVIRONMENT` | Environment mode | `development` | No |
| `PORT` | Server port | `8000` | No |
| `HOST` | Server host | `0.0.0.0` | No |
| `MAX_TOKENS` | Maximum tokens per request | `2048` | No |
| `RATE_LIMIT_REQUESTS` | Requests per period | `100` | No |
| `RATE_LIMIT_PERIOD` | Rate limit period (seconds) | `60` | No |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `*` | No |

## Deployment

### Deploy to Render

1. **Create account** at [render.com](https://render.com)

2. **Create new Web Service**
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` file

3. **Set environment variables**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - Other variables are pre-configured in `render.yaml`

4. **Deploy!**
   - Render will automatically build and deploy

**Render configuration**: `render.yaml` is included

### Deploy to Railway

1. **Create account** at [railway.app](https://railway.app)

2. **New Project** → **Deploy from GitHub repo**

3. **Add environment variables**:
   ```
   OPENAI_API_KEY=your_key_here
   ENVIRONMENT=production
   ```

4. **Railway will auto-deploy** using `railway.json`

### Deploy with Docker

1. **Build image**
```bash
docker build -t ai-chatbot .
```

2. **Run container**
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e ENVIRONMENT=production \
  ai-chatbot
```

3. **Using Docker Compose**
```yaml
version: '3.8'
services:
  chatbot:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=production
```

### Deploy to Vercel

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Set environment variables** in Vercel dashboard

**Note**: `vercel.json` is included for configuration

## API Endpoints

### `GET /`
Serves the chat interface

### `GET /health`
Health check for monitoring
```json
{
  "status": "healthy",
  "service": "AI Chatbot",
  "version": "1.0.0",
  "environment": "production"
}
```

### `GET /api/status`
API status and availability
```json
{
  "api_available": true,
  "environment": "production",
  "max_tokens": 2048
}
```

### `POST /api/chat`
Send messages to AI

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "model": "gpt-3.5-turbo",
  "max_tokens": 1024,
  "temperature": 1.0
}
```

**Response:**
```json
{
  "response": "Hello! How can I help you today?",
  "model": "gpt-3.5-turbo",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

## Project Structure

```
claud@test/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (local)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore rules
├── Dockerfile             # Docker configuration
├── .dockerignore          # Docker ignore rules
├── Procfile               # Heroku configuration
├── runtime.txt            # Python version for deployment
├── render.yaml            # Render deployment config
├── railway.json           # Railway deployment config
├── vercel.json            # Vercel deployment config
├── setup.py               # Setup verification script
├── README.md              # This file
└── static/                # Frontend files
    ├── index.html         # Main HTML
    ├── styles.css         # Styling
    └── app.js             # JavaScript logic
```

## Security Features

- **Rate Limiting**: Prevents API abuse and excessive costs
- **Input Validation**: All inputs validated with Pydantic
- **Security Headers**: XSS, clickjacking, and MIME-type sniffing protection
- **HTTPS Enforcement**: HSTS header for secure connections
- **Error Handling**: No sensitive information in error messages
- **CORS Configuration**: Configurable allowed origins

## Monitoring

### Health Checks
```bash
curl https://your-app.com/health
```

### API Status
```bash
curl https://your-app.com/api/status
```

### Logs
Application logs include:
- Request timestamps
- Client IPs
- Model usage
- Token consumption
- Error details

## Cost Management

### Tips to Reduce Costs
1. Use **GPT-3.5 Turbo** as default (cheaper than GPT-4)
2. Set **MAX_TOKENS** limit to prevent excessive usage
3. Implement **RATE_LIMIT** to control requests
4. Monitor usage in OpenAI dashboard
5. Set up billing alerts in OpenAI account

### Estimated Costs (as of 2024)
- GPT-3.5 Turbo: ~$0.002 per 1K tokens
- GPT-4: ~$0.03-$0.06 per 1K tokens
- GPT-4 Turbo: ~$0.01-$0.03 per 1K tokens

## Development

### Running in Development Mode
```bash
python main.py
```
Auto-reload is enabled in development mode.

### Running Tests
```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest
```

### Code Formatting
```bash
pip install black
black main.py
```

## Troubleshooting

### OpenAI API Key Issues
- Verify key is correct in `.env`
- Check billing in OpenAI dashboard
- Ensure API key has sufficient credits

### Rate Limit Errors (429)
- Wait for rate limit period to expire
- Adjust `RATE_LIMIT_REQUESTS` in environment

### Port Already in Use
- Change `PORT` in `.env`
- Stop existing process: `lsof -ti:8000 | xargs kill`

### CORS Errors
- Update `ALLOWED_HOSTS` in production
- Check browser console for specific errors

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI](https://openai.com/)
- Deployed on [Render](https://render.com/) / [Railway](https://railway.app/)

## Support

For issues or questions:
- Open an issue on GitHub
- Check [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review [OpenAI API documentation](https://platform.openai.com/docs)

---

**Built with ❤️ by iamvishno**

## 🌐 Live Demo

🚀 **Deployed on Render**: Deploy now at [render.com](https://render.com)

📦 **GitHub Repository**: https://github.com/iamvishno/ai-chatbot
