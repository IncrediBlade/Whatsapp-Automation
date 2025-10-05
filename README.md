# WhatsApp Automation - AI-Powered Bot
### *by IncrediBlade*

![GitHub Stars](https://img.shields.io/github/stars/IncrediBlade/Whatsapp-Automation?style=social) ![GitHub Forks](https://img.shields.io/github/forks/IncrediBlade/Whatsapp-Automation?style=social) ![GitHub Issues](https://img.shields.io/github/issues/IncrediBlade/Whatsapp-Automation) ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

An **AI-powered WhatsApp Automation bot** that responds to people on your behalf, keeps track of past conversations, and even sets reminders for you. Built with **Mistral AI, Selenium, NLP, and Python**.

> **Created by IncrediBlade** - Automating WhatsApp conversations with intelligent AI responses!

---

## 📋 Table of Contents
- [Features](#features)
- [Use Cases](#use-cases)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Contributing](#contributing)
- [Support](#support)

---

## ✨ Features

✅ **AI-Powered Responses** - Responds to selected contacts with customized behavior (rude, humble, formal, etc.)

✅ **Conversation Memory** - AI remembers past conversations and continues naturally

✅ **Smart Reminders** - Users can set reminders like: `"Remind Dev to call me once free"` (Uses NLP to understand and store reminders)

✅ **Multi-Contact Support** - AI can talk to multiple people at once

✅ **Personalized Profiles** - Uses profile creation for personalized interactions

✅ **Automated WhatsApp Web** - Seamlessly integrates with WhatsApp Web using Selenium automation

---

## 🎯 Use Cases

- **Busy Professionals**: Auto-respond to messages when you're in meetings or unavailable
- **Customer Support**: Handle basic customer inquiries automatically
- **Personal Assistant**: Set reminders and manage conversations intelligently
- **Multi-tasking**: Keep multiple conversations going simultaneously
- **Custom Personalities**: Set different tones for different contacts (professional, casual, friendly)

---

## 🔧 How It Works?

The bot creates a separate folder for each contact inside the People/ directory. Each folder contains:

• **main.txt** → Full conversation history

• **submain.txt** → Limited chat history for AI memory efficiency

• **temp_reference.txt** → Future use for fetching specific chat parts

• **basicR.txt** → Stores reminders (AI understands reminders using NLP)

---

## 🛠️ Technologies Used

• **Python** - Core programming language

• **Selenium** - Web automation for WhatsApp Web

• **Mistral AI API** - Intelligent AI responses

• **NLP** - Natural Language Processing for understanding reminders

• **Web Scraping** - Extracting and processing WhatsApp messages

---

## 📦 Setup Instructions

### **1️⃣ Get Mistral AI API Key**

- Go to [Mistral AI](https://mistral.ai/) and create an account
- Get your API key for free

### **2️⃣ Download WebDriver for Your Browser**

The bot controls WhatsApp via WhatsApp Web, so you need the right WebDriver:

- **Edge** → Download [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

- **Chrome** → Download [Chrome WebDriver](https://chromedriver.chromium.org/downloads)

- **Firefox** → Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

• Place the WebDriver inside your project folder or set it in System PATH

### **3️⃣ Update Code for Your Browser**

- The current code is optimized for Microsoft Edge
- If you're using Chrome or Firefox, update the WebDriver path & options accordingly in the script

### **4️⃣ Set the Correct File Locations**

- Wherever file locations are mentioned in the code, update them according to your system

### **5️⃣ Login to WhatsApp Web (Required Only Once!)**

- Open WhatsApp Web in your browser and scan the QR code to log in
- Once logged in, your session stays active even if your laptop shuts down

### **6️⃣ Set Your Browser's User Data Directory**

- To avoid logging in repeatedly, specify your browser's user data directory in the script
- For Edge (default in this code):
  - `C:\Users\ADMIN\AppData\Local\Microsoft\Edge\User Data`
- Find yours if using a different browser and update the path in the script

### **🚀 Running the Bot**

Once everything is set up, run these commands:

```bash
# Install dependencies
pip install -r requirements.txt

# Create user profiles
python profile_creation.py

# Start the AI WhatsApp Automation Bot
python whatsapp_automation.py
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- ⭐ Star this repository
- 🍴 Fork and improve

---

## 💬 Support

If you encounter any issues or have questions:

- Open an [Issue](https://github.com/IncrediBlade/Whatsapp-Automation/issues)
- Star ⭐ this repository if you find it useful!
- Share with others who might benefit from WhatsApp Automation

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🏷️ Keywords

`#whatsapp` `#automation` `#bot` `#python` `#selenium` `#ai` `#nlp` `#mistral` `#chatbot` `#messaging` `#whatsapp-bot` `#whatsapp-automation` `#ai-bot` `#automated-responses` `#selenium-automation`

---

### 🌟 Created by [IncrediBlade](https://github.com/IncrediBlade)

*If you found this project helpful, please consider giving it a ⭐ star!*
