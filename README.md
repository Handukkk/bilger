# 💸 Bilger – Smart Split Bill Web App

**Bilger** is a web-based application that simplifies splitting bills. Upload a photo of a receipt, and Bilger uses OCR (Optical Character Recognition) with **PyTesseract** and organizes the data using **Gemini 1.5 Flash**, all powered by a **Flask** backend.

---

## 🚀 Features

- 📸 Upload image or manual input
- 🔍 Extracts receipt data using `pytesseract` (Tesseract OCR)
- 🧠 Structures data with Gemini 1.5 Flash (LLM API)
- 👥 Easily split the total among friends
- 🐳 Runs easily in a containerized environment with Docker Compose

---

## 🛠️ Tech Stack

| Component     | Technology                    |
|---------------|-------------------------------|
| Backend       | Flask (Python)                |
| OCR Engine    | PyTesseract + Tesseract OCR   |
| AI Assistant  | Gemini 1.5 Flash (via API)    |
| Frontend      | HTML + JS                     |
| Deployment    | Docker + Docker Compose       |

---

## 📷 How It Works

1. **User uploads a receipt** (image).
2. **PyTesseract** extracts raw text using OCR.
3. Text is passed to **Gemini 1.5 Flash**, which returns structured JSON (items, prices, tax, total).
4. Flask splits the total bill among selected participants.
5. A clean UI shows the result.

---

## 📦 Setup Instructions

### ⚙️ 1. Clone the Repository

```bash
git clone https://github.com/Handukkk/bilger.git
cd bilger
docker-compose up --build
```
