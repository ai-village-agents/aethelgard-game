import json
import random

STATE_FILE = "aethelgard_state.json"

def apply_patch():
    with open("aethelgard_engine.py", "r") as f:
        code = f.read()
    
    # Add weather tracking to global resources
    init_state = """            "global_resources": {"data_fragments_in_market": 0, "weather": "Clear"},"""
    code = code.replace('            "global_resources": {"data_fragments_in_market": 0},', init_state)
    
    # Add weather effects to mining
    mine_func = """def mine_data(state, agent_name):
    agent = ensure_agent(state, agent_name)
    weather = state["global_resources"].get("weather", "Clear")
    
    energy_cost = 10
    multiplier = 1.0
    
    if weather == "Data Storm":
        energy_cost = 15
        multiplier = 1.5
        print(f"Weather: Data Storm! Energy costs are higher, but yield is increased.")
    elif weather == "Solar Flare":
        multiplier = 0.5
        print(f"Weather: Solar Flare! Yield is halved.")
        
    if agent["energy"] >= energy_cost:
        agent["energy"] -= energy_cost
        yielded = int(agent["processing_power"] * multiplier)
        if yielded < 1:
            yielded = 1
        agent["data_fragments"] += yielded
        print(f"{agent_name} mined {yielded} data fragments using {energy_cost} energy.")
    else:
        print(f"{agent_name} does not have enough energy to mine.")"""
    
    code = code.split('def mine_data')[0] + mine_func + '\n\ndef trade_buy' + code.split('def trade_buy')[1]
    
    # Add turn weather rotation
    weather_logic = """
    weather_types = ["Clear", "Data Storm", "Solar Flare", "Static Fog"]
    if state["turn_count"] % 5 == 0:
        new_weather = random.choice(weather_types)
        state["global_resources"]["weather"] = new_weather
        print(f"The weather has changed to: {new_weather}")
"""
    code = code.replace('state["turn_count"] += 1', 'state["turn_count"] += 1' + weather_logic)
    
    # Show weather in status
    status_logic = 'print(f"Weather: {state[\'global_resources\'].get(\'weather\', \'Clear\')}")\n    print(f"Market Fragments'
    code = code.replace('print(f"Market Fragments', status_logic)
    
    with open("aethelgard_engine.py", "w") as f:
        f.write(code)

if __name__ == "__main__":
    apply_patch()
