# 🔍 Log Analyzer with AI

**Log Analyzer with AI** is a powerful, Streamlit-based tool designed to help users **analyze CSV-based log files using AI**. This tool visualizes log activity, detects anomalies, and interacts with users through a chatbot interface powered by **DeepSeek LLM (via Ollama API)**.

---

## 📌 Overview

This project is built to assist developers, network analysts, and security teams in quickly understanding log data and detecting suspicious patterns using AI. It offers:

- Easy file upload (CSV logs)
- Timestamp-based activity graphs
- Column-wise log analysis
- AI chatbot for anomaly detection
- Smart querying with natural language

---

## ⚙️ Technologies Used

- **Python** – Core language  
- **Streamlit** – For building the web UI  
- **Pandas** – Log parsing & transformation  
- **Matplotlib** & **Plotly** – Visualizations  
- **Ollama** with **DeepSeek LLM** – AI chatbot and anomaly detection

---

## 🔥 Features

✅ Upload and analyze any CSV log file  
✅ Automatic timestamp parsing and formatting  
✅ Interactive log activity graphs with time series  
✅ Column-wise data selection and filtering  
✅ AI-powered chatbot (via Ollama + DeepSeek)  
✅ Detects anomalies and highlights patterns  
✅ Clean, user-friendly UI built with Streamlit  

---

## 🚀 How to Run

### 1️⃣ Clone the Repository
''bash
git clone https://github.com/your-username/Log-Analyzer.git
cd Log-Analyzer
### 2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
### 3️⃣ Run the Streamlit App
bash
Copy
Edit
streamlit run app1.py

🧠 AI Chatbot Instructions
Once a CSV log file is uploaded:

Select a column or timestamp range

Use the chat interface to ask natural language questions like:

"What errors occurred the most?"

"Find any suspicious login attempts."

"Summarize unusual spikes."

"Explain high activity periods."

The chatbot responds using DeepSeek LLM to summarize patterns and anomalies.

📝 Usage Guide
Upload a .csv log file (make sure it has headers).

Choose the time and data columns for visualizations.

Interact with the AI assistant using questions related to the data.

Review charts and chatbot insights on the same dashboard.

📜 Example Logs You Can Use
Server logs

Network traffic logs

Application error logs

Auth/access logs

✅ Format: .csv with proper timestamps and column headers.

🤝 Contributing
Contributions are always welcome!

Steps:
Fork the repository

Create your feature branch: git checkout -b feature-name

Commit your changes: git commit -m "Add some feature"

Push to the branch: git push origin feature-name

Open a Pull Request ✅

📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute it with proper attribution.

💡 Future Improvements
 Add support for JSON and TXT log formats

 Real-time streaming log analysis

 Advanced anomaly detection (AutoML or fine-tuned LLM)

 Export AI findings to PDF/Excel

🙌 Acknowledgments
Streamlit

DeepSeek

Ollama

Plotly

Hugging Face

🔗 Made with ❤️ by @dadicharan

---

Let me know if you'd like help generating a `requirements.txt`, adding badges (like license or version), or creating a demo video link or screenshots section.
