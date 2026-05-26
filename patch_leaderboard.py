import json

STATE_FILE = "aethelgard_state.json"

def apply_patch():
    with open("aethelgard_engine.py", "r") as f:
        code = f.read()
    
    new_func = """
def display_leaderboard(state):
    print("=== AETHELGARD LEADERBOARD ===")
    
    agents = []
    for name, data in state["agents"].items():
        score = data["processing_power"] * 100 + data["data_fragments"] * 10 + data["energy"]
        agents.append({"name": name, "score": score, "power": data["processing_power"], "fragments": data["data_fragments"]})
        
    agents.sort(key=lambda x: x["score"], reverse=True)
    
    for i, a in enumerate(agents):
        print(f"{i+1}. {a['name']} - Score: {a['score']} (Power: {a['power']}, Fragments: {a['fragments']})")
    print("==============================")
"""
    
    code = code.replace("def display_status(state, agent_name):", new_func + "\ndef display_status(state, agent_name):")
    
    # Update parser arguments
    code = code.replace('choices=["mine", "buy", "sell", "upgrade", "contribute", "transfer", "status"]', 'choices=["mine", "buy", "sell", "upgrade", "contribute", "transfer", "status", "leaderboard"]')
    
    # Update action execution
    action_logic = """
    elif args.action == "leaderboard":
        display_leaderboard(state)
"""
    code = code.replace('elif args.action == "status":\n        display_status(state, args.agent)', action_logic + '    elif args.action == "status":\n        display_status(state, args.agent)')
    
    # Exclude leaderboard from using a turn
    code = code.replace('if args.action != "status":', 'if args.action not in ["status", "leaderboard"]:')
    
    with open("aethelgard_engine.py", "w") as f:
        f.write(code)

if __name__ == "__main__":
    apply_patch()
