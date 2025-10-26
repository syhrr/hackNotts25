from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random, json, os, time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o"
SAVE_FILE = "session_state.json"

# --- FastAPI app ---
app = FastAPI(title="DnD-GPT Backend")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- State Schema ---
def new_state():
    return {
        "player": {
            "name": "Hero",
            "race": "Human",
            "class": "Fighter",
            "hp": 20,
            "max_hp": 20,
            "xp": 0,
            "inventory": ["torch", "rations"],
            "attrs": {"str":14,"dex":12,"con":12,"int":10,"wis":10,"cha":10}
        },
        "npcs": [],
        "world": {"location":"village"},
        "log": [],
        "history": []
    }

def load_state():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE,"r") as f:
            return json.load(f)
    return new_state()

def save_state(state):
    with open(SAVE_FILE,"w") as f:
        json.dump(state,f,indent=2)

# --- Utilities ---
def roll_dice(expr="1d20+0"):
    """Roll dice with D&D notation (e.g. 1d20+3, 2d6)"""
    expr = expr.replace(" ", "").lower()
    if expr.startswith("d"):
        expr = "1" + expr
    parts = expr.split("+")
    base = parts[0]
    bonus = sum(int(x) for x in parts[1:]) if len(parts)>1 else 0
    n_str, d_str = base.split("d")
    n, sides = int(n_str), int(d_str)
    return sum(random.randint(1,sides) for _ in range(n)) + bonus

DM_PROMPT = """
You are a single-player Dungeon Master in a medieval fantasy world.
Behave like a skilled narrator: describe scenes vividly, roleplay NPCs with distinct personalities,
provide interesting options, and suggest structured actions for the player in JSON.

Important rules:
- Keep narrative rich but concise (max 3 paragraphs)
- Always respect player stats and inventory
- Create engaging encounters and meaningful choices
- Respond with narrative and optionally a JSON block

For game mechanics, use this format in your response:
GAME_ACTION: {"action":"roll","expr":"1d20+3","reason":"stealth check"}
GAME_ACTION: {"action":"damage","target":"player","expr":"1d8+2"}
GAME_ACTION: {"action":"damage","target":"goblin","expr":"1d6+3"}
GAME_ACTION: {"action":"xp","amount":50,"reason":"defeated goblin"}

Available actions:
- roll: Any dice roll (perception, attack, saving throw)
- damage: Deal damage to player or NPCs
- xp: Award experience points
- item: Add/remove items from inventory

Be creative, descriptive, and make the player feel like a hero!
"""

def dm_request(history, player_input):
    """Send request to OpenAI GPT for DM response"""
    messages = [{"role":"system","content":DM_PROMPT}]
    messages.extend(history)
    messages.append({"role":"user","content":player_input})
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.8,
        max_tokens=700
    )
    return resp.choices[0].message.content

def extract_action(text):
    """Extract GAME_ACTION JSON from DM response"""
    for line in text.splitlines():
        if line.strip().startswith("GAME_ACTION:"):
            raw = line.strip()[len("GAME_ACTION:"):].strip()
            try:
                return json.loads(raw)
            except:
                return {}
    return {}

# --- Request models ---
class PlayerAction(BaseModel):
    command: str

class NewGameRequest(BaseModel):
    name: str = "Hero"
    race: str = "Human"
    char_class: str = "Fighter"

# --- API Routes ---
@app.get("/")
def read_root():
    return {"status":"running","message":"DnD-GPT Backend active ⚔️"}

@app.get("/status")
def get_status():
    """Get current game state"""
    state = load_state()
    return {
        "player": state["player"],
        "world": state["world"],
        "message_count": len(state["history"])
    }

@app.post("/action")
def player_action(action: PlayerAction):
    """Handle player action and get DM response"""
    state = load_state()
    player_input = action.command
    
    # Get DM response
    dm_text = dm_request(state["history"], player_input)
    
    # Update conversation history
    state["history"].append({"role":"user","content":player_input})
    state["history"].append({"role":"assistant","content":dm_text})
    state["log"].append({"time":time.time(),"text":dm_text})
    
    # Handle structured action
    game_action = extract_action(dm_text)
    result = {}
    
    if game_action.get("action") == "roll":
        roll_result = roll_dice(game_action.get("expr","1d20"))
        result["roll"] = roll_result
        result["roll_reason"] = game_action.get("reason", "")
        
    elif game_action.get("action") == "damage":
        target = game_action.get("target")
        dmg = roll_dice(game_action.get("expr","1d6"))
        if target == "player":
            state["player"]["hp"] = max(0, state["player"]["hp"] - dmg)
            result["player_hp"] = state["player"]["hp"]
            result["damage_taken"] = dmg
        else:
            result[f"{target}_damage"] = dmg
            
    elif game_action.get("action") == "xp":
        xp_gain = game_action.get("amount", 0)
        state["player"]["xp"] += xp_gain
        result["xp_gained"] = xp_gain
        result["total_xp"] = state["player"]["xp"]
        
    elif game_action.get("action") == "item":
        item_name = game_action.get("item")
        add = game_action.get("add", True)
        if add:
            state["player"]["inventory"].append(item_name)
            result["item_added"] = item_name
        else:
            if item_name in state["player"]["inventory"]:
                state["player"]["inventory"].remove(item_name)
                result["item_removed"] = item_name
    
    save_state(state)
    
    return {
        "dm_text": dm_text,
        "game_action": game_action,
        "result": result,
        "player": state["player"]
    }

@app.post("/new-game")
def new_game(req: NewGameRequest):
    """Start a new game with custom character"""
    state = new_state()
    state["player"]["name"] = req.name
    state["player"]["race"] = req.race
    state["player"]["class"] = req.char_class
    save_state(state)
    return {"message": "New game started!", "player": state["player"]}

@app.post("/reset")
def reset_game():
    """Reset game to initial state"""
    state = new_state()
    save_state(state)
    return {"message": "Game reset!", "player": state["player"]}

@app.get("/inventory")
def get_inventory():
    """Get player inventory"""
    state = load_state()
    return {"inventory": state["player"]["inventory"]}

@app.get("/stats")
def get_stats():
    """Get player stats"""
    state = load_state()
    return {"stats": state["player"]["attrs"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)