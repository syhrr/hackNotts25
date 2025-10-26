# hackNotts25
Our first hackathon

# ⚔️ Medieval D&D Chatbot

A medieval fantasy Dungeon & Dragons chatbot powered by OpenAI GPT-4 and FastAPI. Experience interactive storytelling with dice rolls, combat, character progression, and more!

## 🎮 Features

- **AI Dungeon Master**: GPT-4 powered narrative and decision-making
- **Real-time Character Stats**: Track HP, XP, inventory, and attributes
- **Dice Rolling System**: Automatic D&D dice notation (1d20+3, 2d6, etc.)
- **Combat System**: Dynamic damage calculation for players and NPCs
- **Persistent State**: Save/load game sessions
- **Beautiful Medieval UI**: Scroll-themed interface with golden accents
- **Responsive Design**: Works on desktop and mobile

## 📁 Project Structure

```
medieval-dnd-chatbot/
├── backend/
│   ├── main.py              # FastAPI backend with OpenAI integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables (create this)
│   └── session_state.json   # Auto-generated save file
│
├── frontend/
│   └── index.html           # Complete frontend (HTML/CSS/JS)
│
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- Modern web browser

### Backend Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd medieval-dnd-chatbot
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Navigate to backend and install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

4. **Create `.env` file:**
```bash
# Windows (Command Prompt)
copy .env.example .env

# Mac/Linux or Windows (PowerShell)
cp .env.example .env
```

> **Note:** The current version uses a **Mock DM** (no API needed)! If you want to use real GPT-4, add your OpenAI API key to the `.env` file.

5. **Run the backend:**
```bash
python main.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

1. **Open `frontend/index.html` in your browser**
   - Simply double-click the file, or
   - Use a local server (recommended):
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Then visit `http://localhost:8080`

2. **Start playing!** Type actions like:
   - "I enter the tavern and look around"
   - "I attack the goblin with my sword"
   - "I try to persuade the guard"
   - "I search for treasure"

## 🎲 Game Mechanics

### Dice Rolling
The system automatically handles D&D dice notation:
- `1d20+3` - Roll 1 20-sided die, add 3
- `2d6` - Roll 2 6-sided dice
- `1d8+2` - Roll 1 8-sided die, add 2

### Character Stats
- **HP**: Health points (damage reduces this)
- **XP**: Experience points (gain from completing quests)
- **Inventory**: Items you collect
- **Attributes**: STR, DEX, CON, INT, WIS, CHA

### Combat
The DM automatically calculates:
- Attack rolls
- Damage dealt to enemies
- Damage taken by player
- Enemy behavior and tactics

## 🛠️ API Endpoints

### `GET /`
Health check for the backend

### `POST /action`
Send player action, get DM response
```json
{
  "command": "I attack the goblin"
}
```

Response:
```json
{
  "dm_text": "You swing your sword...",
  "game_action": {"action": "roll", "expr": "1d20+3"},
  "result": {"roll": 15},
  "player": {...}
}
```

### `GET /status`
Get current game state

### `POST /new-game`
Start new game with custom character
```json
{
  "name": "Thorin",
  "race": "Dwarf",
  "char_class": "Warrior"
}
```

### `POST /reset`
Reset game to initial state

### `GET /inventory`
Get player inventory

### `GET /stats`
Get player attributes

## 🎨 Customization

### Change Character Starting Stats
Edit the `new_state()` function in `backend/main.py`:
```python
"player": {
    "name": "Hero",
    "race": "Human",
    "class": "Fighter",
    "hp": 30,  # Change starting HP
    "max_hp": 30,
    "xp": 0,
    "inventory": ["sword", "shield"],  # Custom items
}
```

### Modify DM Personality
Edit the `DM_PROMPT` in `backend/main.py` to change how the DM responds

### Style the Frontend
Edit the CSS in `frontend/index.html` to customize colors, fonts, and layout

## 🐛 Troubleshooting

### CORS Errors
Make sure CORS is enabled in `backend/main.py` (already included)

### API Key Issues
- Verify `.env` file exists in backend folder
- Check API key is valid at https://platform.openai.com
- Ensure no extra spaces in the `.env` file

### Frontend Not Connecting
- Check backend is running on port 8000
- Update `API_URL` in `frontend/index.html` if using different port
- Check browser console for errors (F12)

### State Not Saving
- Ensure backend has write permissions in its directory
- Check `session_state.json` is being created

## 📚 Technologies Used

- **Backend**: FastAPI, Python 3.8+
- **AI**: OpenAI GPT-4
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Custom medieval theme with gradients and animations

##  License

MIT License - feel free to use for your hackathon!

##  Credits



---

**Good luck with your hackathon! May the dice roll in your favor!** 🎲⚔️
