# 🚀 Startup Journey Simulator

An AI-powered decision intelligence platform that helps early-stage founders **simulate their startup journey**, understand stakeholder reactions, and make better decisions **before executing in the real world**.

---

## 🧠 Problem Statement

Early-stage innovators often face:

* ❌ Lack of execution experience
* ❌ Difficulty understanding stakeholder reactions
* ❌ Limited resources (time, money, team)
* ❌ No safe environment to test decisions
* ❌ Unawareness of government support schemes

👉 Result: High failure rates despite good ideas

---

## 💡 Solution

**Startup Journey Simulator** is a guided platform that:

* Simulates real-world startup decisions
* Shows stakeholder reactions dynamically
* Provides actionable insights
* Integrates government schemes intelligently
* Generates execution roadmaps

---

## 🔥 Key Features

### 🎯 1. AI-Driven Decision Simulation

* Generates 3–5 realistic decision points
* Context-aware (based on idea + stage)

---

### 👥 2. Stakeholder Reaction Engine

Simulates responses from:

* Customers
* Investors
* Government
* Partners (NGOs / Companies)
* Team

---

### 🏛 3. Government Policy Integration (Unique Feature)

* Suggests relevant schemes (e.g., Startup India, PMFME)
* Influences:

  * Risk
  * Financial score
  * Trust
* Embedded naturally (no UI clutter)

---

### 📊 4. Dynamic Scoring System

Tracks:

* Impact Score
* Financial Sustainability
* Risk Level
* Stakeholder Trust

---

### 🧭 5. Execution Roadmap Generator

* Step-by-step actionable plan
* Includes real-world strategies
* Suggests policy usage

---

### 🔁 6. Iterative Learning Loop

* Users can retry decisions
* Compare outcomes
* Learn through simulation

---

## 🧩 Supported Scenarios

### 🟢 Idea Stage

* Problem validation
* Market understanding
* Initial strategy

---

### 🔵 Prototype Stage

* Launch strategy
* Pricing decisions
* Growth & scaling

---

## ⚙️ Tech Stack

* **Frontend:** HTML, CSS, Bootstrap
* **Backend:** Flask (Python)
* **AI Engine:** Google Gemini API
* **Architecture:** Rule-based + AI hybrid

---

## 🤖 AI Usage

AI is used to dynamically generate:

* Decision points
* Stakeholder reactions
* Insights
* Execution roadmap

👉 Ensures:

* Personalized outputs
* Real-world relevance
* No hardcoding

---

## 🔄 API Failover System

To ensure reliability:

* Multiple API keys used
* Automatic retry on failure
* Model fallback:

  * Primary → Gemini Flash
  * Backup → Flash-8B / Pro

👉 Guarantees uninterrupted experience

---

## 🧠 System Architecture

```
User Input → Backend (Flask) → AI Engine (Gemini)
           → Decision Generation
           → Stakeholder Simulation
           → Score Calculation
           → Output (UI)
```

---

## 🧪 Example Use Case

**Startup:** AgriLink
**Idea:** Connect farmers directly to retailers

### Simulation Output:

* Farmers → High trust
* Investors → Moderate confidence
* Govt → Supportive (eligible for subsidy)

### Roadmap:

1. Run pilot in 1 district
2. Partner with NGO
3. Apply for Startup India
4. Scale gradually

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/startup-journey-simulator.git
cd startup-journey-simulator

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY_1=your_key_here
GEMINI_API_KEY_2=your_key_here
```

---

## 🏆 Why This Project Stands Out

* ✅ Combines simulation + real-world guidance
* ✅ Policy-aware decision making
* ✅ Dynamic AI-generated scenarios
* ✅ Practical execution focus
* ✅ Scalable architecture


## 📌 Future Enhancements

* Real-time market data integration
* Advanced financial modeling
* Multi-user collaboration
* Mobile app version

---

## 👨‍💻 Contributors
K. Deekshitha
J. Saivardhan
A. Srivardhan
M. Sree Bhuvan Mithra
Srija Guddati

---

## 📄 License

This project is for educational and hackathon purposes.
