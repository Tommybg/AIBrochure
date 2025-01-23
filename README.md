# 🎙️ GovLab Voice Assistant

An AI-powered voice assistant for GovLab using OpenAI's Realtime API and LiveKit.

![GovLab Assistant](./assets/demo.gif)

## 🚀 Features

- Real-time speech-to-speech conversations
- Multilingual support (Spanish primary)
- Expert knowledge of GovLab's portfolio
- Low-latency responses
- WebRTC-powered reliability

## 🛠️ Tech Stack

- **Backend:** Python + LiveKit Agents Framework
- **Frontend:** Next.js + LiveKit Components
- **AI:** OpenAI Realtime API
- **Infrastructure:** LiveKit Cloud

## 📋 Prerequisites

- Python 3.9-3.12
- Node.js 20.17.0+
- OpenAI API key with Realtime API access
- LiveKit account

## 🚀 Quick Start

1. **Clone & Setup Agent**
```bash
git clone https://github.com/yourusername/govlab-assistant
cd govlab-assistant/agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
# .env.local
OPENAI_API_KEY=your_key
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
```

3. **Start Agent**
```bash
python agent.py dev
```

4. **Launch Frontend**
```bash
cd ../frontend
pnpm install
pnpm dev
```

## 📚 GovLab Portfolio

Our assistant is knowledgeable about:
- Data analysis automation tools
- PQRS management system
- Traffic counting solution
- Police assistance application
- Document comparison tool

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📄 License

MIT © GovLab
