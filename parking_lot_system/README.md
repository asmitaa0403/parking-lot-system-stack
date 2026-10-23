# 🅿️ SmartPark — Stack-Based Parking Management System

A parking lot management system built with **Python**, **Streamlit**, and fundamental **Data Structures and Algorithms (DSA)** using the **Stack (Last-In-First-Out / LIFO)** paradigm.

---

## 📌 Project Overview & Stack Concept

In real-world parking lots with dead-end lanes or single-lane driveways (valet stacks, ferries, train shuttles):
- **Stack Representation**: Each lane is a Stack with a fixed capacity.
- **Entry & Exit Gate**: The open end of the lane corresponds to the **Top of the Stack**.
- **PUSH Operation**: When a car arrives, it enters the lane and is pushed onto the top of the stack.
- **Direct POP Operation ($O(1)$)**: When the car parked at the top of the stack wants to leave, it exits immediately.
- **Arbitrary Retrieval via Auxiliary Stack**:
  - If a car parked deeper inside the stack needs to depart:
    1. All blocking vehicles above it are popped onto a **Temporary Buffer Stack** (auxiliary stack).
    2. The target car is popped from the main stack and departs.
    3. The displaced vehicles in the buffer stack are popped and pushed back into the main lane stack in their exact original order.
  - Demonstrates stack manipulation, operation move tracking, and extra handling fee calculations!

---

## 🚀 Features

- **Real-Time Visual Stack Lanes**: Visually observe vehicles entering, queuing up, and leaving from the exit gate at the top of each lane.
- **Dynamic Configuration**: Adjust the number of lanes (stacks), lane capacities, and hourly billing rates in real time via the sidebar.
- **One-Click Demo Loader**: Instant test population with realistic vehicles, colors, and timestamps.
- **Direct $O(1)$ LIFO Exit**: Quickly pop the top vehicle from any lane.
- **Auxiliary Stack Algorithm Simulation**: Select any buried vehicle, view the preview of required stack operations, and execute with live step-by-step console logs.
- **Checkout & Billing**: Computes parking duration, base fee, handling fee for auxiliary stack moves, and prints receipts.
- **Vehicle Locator & Search**: Search by plate number or owner to locate lane and depth from exit.
- **Audit Logs & Export**: Review transaction logs and download CSV receipts.

---

## 🛠️ Local Installation & Running

### 1. Prerequisites
- Python 3.9+ installed.

### 2. Setup
Clone or navigate into the project directory:
```bash
cd parking_lot_system
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
Run the Streamlit app:
```bash
python -m streamlit run app.py
```
Or if `streamlit` is in your system PATH:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Community Cloud (Free)

Deploying this app online so anyone can use it is easy:

1. **Push to GitHub**:
   - Create a new public or private repository on [GitHub](https://github.com).
   - Push this project folder (`parking_lot_system`) to your GitHub repository:
     ```bash
     git init
     git add .
     git commit -m "Initial commit of Stack Parking Lot System"
     git branch -M main
     git remote add origin https://github.com/<your-username>/<your-repo-name>.git
     git push -u origin main
     ```

2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
   - Click **"New app"**.
   - Select your repository, branch (`main`), and set the main file path to:
     ```text
     app.py
     ```
   - Click **"Deploy!"**.

3. **Live App**:
   Streamlit will automatically detect `requirements.txt`, install dependencies, and launch your live public URL (e.g., `https://your-app-name.streamlit.app`).

---

## 📂 Project Structure

```
parking_lot_system/
├── app.py                   # Main Streamlit web application & UI tabs
├── models.py                # Vehicle, ParkingStack, and ParkingManager DSA classes
├── styles.py                # Visual styling and responsive HTML/CSS stack renderers
├── requirements.txt         # Required Python packages (streamlit, pandas)
├── .streamlit/
│   └── config.toml          # Custom dark UI terminal theme configuration
└── README.md                # Documentation & deployment guide
```
