# WhatsApp AI Automation Bot  

An AI-powered WhatsApp bot that **responds to people on your behalf**, keeps track of past conversations, and even sets reminders for you. Built with **Mistral AI, Web Scraping, NLP, and Python**.  

## Features  
✅ AI **responds to selected contacts** with customized behavior (rude, humble, formal, etc.)  
✅ AI **remembers past conversations** and continues naturally  
✅ Users can set reminders like: `"Remind Dev to call me once free"` *(Uses NLP to understand and store reminders)*  
✅ AI can talk to **multiple people at once**  
✅ Uses **profile creation** for personalized interactions  

## How It Works?  
The bot creates a **separate folder for each contact** inside the `People/` directory. Each folder contains:  
- `main.txt` → Full conversation history  
- `submain.txt` → Limited chat history for AI memory efficiency  
- `temp_reference.txt` → Future use for fetching specific chat parts  
- `basicR.txt` → **Stores reminders (AI understands reminders using NLP)**  

## 🛠️ Technologies Used  
- Python 🐍  
- Web Scraping (for WhatsApp automation)  
- **NLP** for understanding reminders  
- Mistral AI API   

## 🔧 Setup Instructions  
### **1️⃣ Get Mistral AI API Key**  
- Go to **[Mistral AI](https://mistral.ai)** and create an account.  
- Get your **API key** for free.  

### **2️⃣ Download WebDriver for Your Browser**  
- The bot controls WhatsApp **via WhatsApp Web**, so you need the right **WebDriver**:  
  - **Edge** → Download [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)  
  - **Chrome** → Download [Chrome WebDriver](https://chromedriver.chromium.org/downloads)  
  - **Firefox** → Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases)  
- Place the **WebDriver** inside your project folder or set it in **System PATH**.  

### **3️⃣ Update Code for Your Browser**  
- The current code is **optimized for Microsoft Edge**.  
- If you're using **Chrome or Firefox**, update the **WebDriver path & options** accordingly in the script.  

### **4️⃣ Set the Correct File Locations**  
- Wherever **file locations** are mentioned in the code, **update them according to your system**.  

### **5️⃣ Login to WhatsApp Web** *(Required Only Once!)*  
- Open WhatsApp Web in your browser and **scan the QR code** to log in.  
- Once logged in, **your session stays active** even if your laptop shuts down.  

### **6️⃣ Set Your Browser's User Data Directory**  
- To **avoid logging in repeatedly**, specify your browser’s **user data directory** in the script.  
- **For Edge (default in this code)**:  
  - `C:\Users\ADMIN\AppData\Local\Microsoft\Edge\User Data`  
- **Find yours** if using a different browser and update the path in the script.  

### **🚀 Running the Bot**  
Once everything is set up, run these commands:  

```bash
# Install dependencies
pip install -r requirements.txt  

# Create user profiles
python profile_creation.py  

# Start the AI WhatsApp Bot
python whatsapp_automation.py  

