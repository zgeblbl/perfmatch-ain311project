# 🏐 PerfMatch - Volleyball Match Prediction Backend (AIN311 Project)

This repository contains the **backend** of the PerfMatch project, developed as part of the AIN311 course. The goal is to **predict volleyball match outcomes** and **analyze individual player contributions** using machine learning models trained on historical data.

The frontend (in a separate repository) allows users to select a team of players and displays:
1. **Match prediction**: Will the selected team win or lose?
2. **Player contributions**: Individual contribution scores in categories like passes, assists, blocks, etc.

---

## 🔍 Project Overview

This backend focuses on:

- Preprocessing raw volleyball match data
- Engineering player-level and team-level features
- Computing contribution metrics for each player
- Training and evaluating several ML models to predict match results
- Saving models to be used in the frontend prediction interface

---
## 🧠 Models Implemented

We experimented with and compared multiple supervised learning algorithms:

| Model               | Status         | Notes                              |
|--------------------|----------------|-------------------------------------|
| Logistic Regression | ✅ Completed   | Baseline model                     |
| SVM (Support Vector Machine) | ✅ Completed | Better accuracy with tuned kernel |
| Random Forest Classifier | ✅ Completed | Used for robustness and interpretability |
| Linear Regression  | ✅ (for contribution estimation) | Not for win/loss classification |

Models were saved using `joblib` for reuse in the prediction service.

---
## 🌐 Frontend Integration
The backend exposes endpoints used by the frontend UI, which lets users:

- Select players to form a team
- Receive predicted outcome: win or lose
- View individual contribution scores
Note: The frontend is maintained in a separate repository. You can access the frontend repository [here](https://github.com/zgeblbl/perfmatch-frontend).

---
## 👨‍💻 Team
Project developed for AIN311 Course

Contributors: Özge Bülbül - Sümeyra Koç - Zeynep Yıldız
