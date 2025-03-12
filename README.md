# <p align="center">Capstone</p>

## <p align="center">Summary</p>
Our Health and Wellness Tracker App enables users to log their food and water intake, workouts, and sleep. 
Users can set and track personal wellness goals, participate in community events, and share their progress with others. 
Our team will deliver a dynamic yet user-friendly experience by utilizing a web-based front end and a Python-powered backend.

---
## <p align="center">Setup Instructions</p>

### 1. Clone The Repository
```
git clone https://github.com/LoganPickell/Capstone.git
```
### 2. Create a Virtual Environment (Optional/Recommended, not required)
```
python -m venv venv
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Change Directories
```
cd capstoneproject
```
### 5. Fix .env file
Use the following command in the terminal to copy .env.sample into a .env file.
```
cp capstoneproject/.env.sample capstoneproject/.env
```
Change the variable DJANGO_SECRET_KEY to a value with 10-15 random characters.
Save the file.

In the file in 'capstoneproject/capstoneproject/.env' add the following at the bottom:
```
DB_USER=collaborator
DB_PASSWORD=CollabPW321!
```

### 6. Run Server
```
python manage.py runserver
```
### 7. Are you on a MAC? Getting a MYSQL Error?
This error occurs because macOS does not come with MySQL development headers by default, which are required to install mysqlclient (the underlying library that Django’s MySQL backend uses).
Windows often handles this differently due to bundled MySQL support in some environments.

Use the following commands to fix the error
```
brew install pkg-config
brew install mysql-client
pip install mysql
```
### 8. Access the App
Once the server is running, see terminal for link to port to enter in your browser.

---


## <p align="center">Entity Relationship Diagram </p>

```mermaid

erDiagram
    USER ||--o{ ACTIVITY : logs
    USER ||--o{ GOAL : sets
    USER ||--o{ LEADERBOARD : participates
    
    ACTIVITY ||--o{ WORKOUT_ACTIVITY : is
    ACTIVITY ||--o{ MEAL_ACTIVITY : is
    ACTIVITY ||--o{ WATER_ACTIVITY : is
    ACTIVITY ||--o{ SLEEP_ACTIVITY : is

    GOAL ||--o{ FITNESS_GOAL : is
    GOAL ||--o{ NUTRITION_GOAL : is
    GOAL ||--o{ SLEEP_GOAL : is
    GOAL ||--o{ WATER_GOAL : is

    USER {
        int userID PK
        string username
        string email
        string password
    }
    
     ACTIVITY {
        int activityID PK
        int userID FK
        string activityType "Workout, Meal, Water, Sleep"
        date dateLogged
    }

    WORKOUT_ACTIVITY {
    int activityID PK, FK
    string exerciseType "Running, Weightlifting, etc."
    float duration "Minutes for cardio"
    float distance "Miles/km for running"
    float weightLifted "For strength training"
    int reps 
    int sets 
    }
    
     MEAL_ACTIVITY {
        int activityID PK, FK
        float calories
        float protein
        float carbs
        float fat
        string mealType "Breakfast, Lunch, Dinner, Snack"
    }
    
        WATER_ACTIVITY {
        int activityID PK, FK
        float amount "Liters or ounces"
    }
    
    
    SLEEP_ACTIVITY {
        int activityID PK, FK
        float duration "Hours slept"
        time bedtime
        time wakeTime
    }
    
    GOAL {
        int goalID PK
        int userID FK
        string goalType "Fitness, Nutrition, Sleep, Water"
        float targetValue
        date targetDate
        string status "Active, Completed, Failed"
    }

    FITNESS_GOAL {
        int goalID PK, FK
        float targetWeightLifted
        float targetDistance
        float targetDuration
    }

    NUTRITION_GOAL {
        int goalID PK, FK
        float dailyCalorieIntake
        float proteinGoal
        float sugarLimit
    }
    
        WATER_GOAL {
        int goalID PK, FK
        float dailyWaterIntakeTarget
    }

    SLEEP_GOAL {
        int goalID PK, FK
        float targetHours
    }

    LEADERBOARD {
        int leaderboardID PK
        string challengeName
        date startDate
        date endDate
        int userID FK
        int rank
        float score "Points earned"
    }

```
---

## <p align="center">User Flow Diagram</p>
```mermaid
flowchart TD
    A[Start] -->|New User| B[Sign Up]
    A -->|Existing User| C[Log In]
    
    B --> D[Dashboard]
    C --> D

    D -->|Log Activities| E[Choose Activity Type]
    E -->|Workout| F[Log Workout]
    E -->|Meal| G[Log Meal]
    E -->|Water Intake| H[Log Water]
    E -->|Sleep| I[Log Sleep]

    D -->|Set Goals| J[Choose Goal Type]
    J -->|Fitness| K[Set Fitness Goal]
    J -->|Nutrition| L[Set Nutrition Goal]
    J -->|Sleep| M[Set Sleep Goal]

    D -->|Join Challenges| N[Choose Challenge Type]
    N -->|Leaderboard| O[Join Leaderboard]
    N -->|Community Event| P[Join Event]

    D -->|View Progress| Q[Check Stats & Goals]
    
    Q --> R[End Flow]
    F --> R
    G --> R
    H --> R
    I --> R
    K --> R
    L --> R
    M --> R
    O --> R
    P --> R



```
---

## <p align="center">System Architecture Diagram</p>

```mermaid

graph TD
    User["👤 User"] -->|Logs activity & sets goals| Frontend["🖥️ Frontend (Web Framework)"]
    
    Frontend -->|API Calls| Backend["🖥️ Backend (Python)"]
    Backend -->|Stores & Retrieves Data| Database["🛢️ Relational Database"]

    Backend -->|Updates & Fetches| Leaderboard["🏆 Leaderboard"]
    Backend -->|Handles Authentication| AuthService["🔐 Auth Service (OAuth/Hashed Passwords)"]

    Frontend -->|Fetches Leaderboard Data| Leaderboard

    Backend -->|Sends Notifications| NotificationService["📢 Notification Service"]
    Backend -->|Integrates with External APIs| ExternalAPIs["🌍 Health APIs (e.g., Fitbit, Apple Health)"]


```