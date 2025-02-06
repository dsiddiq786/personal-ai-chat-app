# 🧠 Personal AI Chat App
## By Dawood Siddiq

**Personal AI Chat App** is a **Windows desktop application** powered by **Google Cloud's Vertex AI (DeepSeek-R1 Model)**. It provides an intuitive **ChatGPT-like experience**, supporting **text-based chat** and **voice input** with **real-time AI responses**.

## 🚀 Features
- ✅ **Chat with AI** (Like ChatGPT, powered by Google Cloud Vertex AI)
- ✅ **Voice Input Support** (Speak instead of typing)
- ✅ **AI Voice Response** (Optional: AI can speak replies)
- ✅ **Light/Dark Mode Toggle**
- ✅ **User-Friendly GUI** (Built with PyQt6)
- ✅ **Standalone `.exe` for Windows**
- ✅ **Fully Secure** (Credentials are excluded from Git)

---

## 🛠️ **Installation & Setup**
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-username/personal-ai-chat-app.git
cd personal-ai-chat-app
```

### 2️⃣ **Set Up a Virtual Environment (Recommended)**
```sh
python -m venv env
source env/bin/activate    # macOS/Linux
env\Scripts\activate       # Windows
```

### 3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Set Up Google Cloud Credentials**
#### 🔹 **Step 1: Enable Vertex AI on Google Cloud**
1. Go to **Google Cloud Console** → [Vertex AI](https://console.cloud.google.com/vertex-ai/)
2. Create and deploy a model (DeepSeek-R1).
3. Copy the **Project ID, Endpoint ID, and Location**.

#### 🔹 **Step 2: Create a Service Account & API Key**
1. Go to **Google Cloud Console** → [IAM & Admin](https://console.cloud.google.com/iam-admin/)
2. Create a **new service account** with **Vertex AI access**.
3. Generate a **JSON Key File** and download it.

#### 🔹 **Step 3: Store Credentials in a Secure `.env` File**
1. Create a `.env` file in the **root of your project**:
   ```sh
   touch .env
   ```
2. Open `.env` and add:
   ```ini
   PROJECT_ID=your-google-cloud-project-id
   ENDPOINT_ID=your-vertex-ai-endpoint-id
   LOCATION=your-region (e.g., asia-southeast1)
   API_ENDPOINT=your-api-endpoint-url
   GOOGLE_APPLICATION_CREDENTIALS=gcp-key.json
   ```

3. Move the **downloaded JSON key** to the project folder and rename it to:
   ```
   gcp-key.json
   ```

---

## ▶️ **Run the Chat App**
Once everything is set up, run:
```sh
python chat.py
```

---

## 🔹 **Building the `.exe` File for Windows**
To create a **standalone `.exe` file**, run:
```sh
pyinstaller --onefile --windowed --name PersonalAIChat chat.py
```
Your `.exe` will be in the `dist/` folder.

---

## **🌟 Contributing**
If you'd like to improve this project, feel free to **fork the repo** and submit a pull request.

---

## 📜 **License**
This project is licensed under the **MIT License**.

---

## 🚀 **Enjoy Your Personal AI Chat App!** 🎉