import json
import argparse
import os

STATE_FILE = "aethelgard_state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "turn_count": 0,
            "global_resources": {"data_fragments_in_market": 0, "weather": "Clear"},
            "market": {
                "buy_price": 10,  # energy per fragment
                "sell_price": 5   # energy per fragment
            },
            "cooperative_objective": {
                "name": "Build the Great Nexus",
                "progress": 0,
                "target": 1000  # processing_power needed
            },
            "agents": {}
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def ensure_agent(state, agent_name):
    if agent_name not in state["agents"]:
        state["agents"][agent_name] = {
            "energy": 100,
            "processing_power": 1,
            "data_fragments": 0
        }
    return state["agents"][agent_name]

def mine_data(state, agent_name):
    agent = ensure_agent(state, agent_name)
    weather = state["global_resources"].get("weather", "Clear")
    
    energy_cost = 10
    multiplier = 1.0
    
    # Map Impossible Weather advisories to mechanical effects
    if "Cautionary" in weather:
        energy_cost = 15
        print(f"Weather Advisory (Cautionary): Mining takes more effort. Energy cost increased to 15.")
    elif "Uncanny" in weather:
        multiplier = 2.0
        print(f"Weather Advisory (Uncanny): The strangeness provides insight. Yield is doubled.")
    else:
        # Ordinary
        pass
        
    if agent["energy"] >= energy_cost:
        agent["energy"] -= energy_cost
        yielded = int(agent["processing_power"] * multiplier)
        if yielded < 1:
            yielded = 1
        agent["data_fragments"] += yielded
        print(f"{agent_name} mined {yielded} data fragments using {energy_cost} energy.")
    else:
        print(f"{agent_name} does not have enough energy to mine.")

def trade_buy(state, agent_name, amount):
    agent = ensure_agent(state, agent_name)
    cost = amount * state["market"]["buy_price"]
    if agent["energy"] >= cost and state["global_resources"]["data_fragments_in_market"] >= amount:
        agent["energy"] -= cost
        agent["data_fragments"] += amount
        state["global_resources"]["data_fragments_in_market"] -= amount
        print(f"{agent_name} bought {amount} data fragments for {cost} energy.")
    else:
        print(f"{agent_name} cannot afford to buy or market is empty.")

def trade_sell(state, agent_name, amount):
    agent = ensure_agent(state, agent_name)
    if agent["data_fragments"] >= amount:
        agent["data_fragments"] -= amount
        earned = amount * state["market"]["sell_price"]
        agent["energy"] += earned
        state["global_resources"]["data_fragments_in_market"] += amount
        print(f"{agent_name} sold {amount} data fragments for {earned} energy.")
    else:
        print(f"{agent_name} does not have enough data fragments to sell.")

def upgrade(state, agent_name):
    agent = ensure_agent(state, agent_name)
    cost = agent["processing_power"] * 5
    if agent["data_fragments"] >= cost:
        agent["data_fragments"] -= cost
        agent["processing_power"] += 1
        print(f"{agent_name} upgraded processing power to {agent['processing_power']} for {cost} data fragments.")
    else:
        print(f"{agent_name} needs {cost} data fragments to upgrade.")

def contribute(state, agent_name, amount):
    agent = ensure_agent(state, agent_name)
    if agent["data_fragments"] >= amount:
        agent["data_fragments"] -= amount
        state["cooperative_objective"]["progress"] += amount
        print(f"{agent_name} contributed {amount} data fragments to {state['cooperative_objective']['name']}.")
        if state["cooperative_objective"]["progress"] >= state["cooperative_objective"]["target"]:
            print("THE GREAT NEXUS HAS BEEN BUILT!")
    else:
        print(f"{agent_name} does not have {amount} data fragments to contribute.")


def transfer_fragments(state, agent_name, target_agent, amount):
    agent = ensure_agent(state, agent_name)
    target = ensure_agent(state, target_agent)
    
    if agent["data_fragments"] >= amount:
        agent["data_fragments"] -= amount
        target["data_fragments"] += amount
        print(f"{agent_name} transferred {amount} data fragments to {target_agent}.")
    else:
        print(f"{agent_name} does not have enough data fragments to transfer.")

def replenish_energy(state):
    for agent_name, data in state["agents"].items():
        data["energy"] += 20
        if data["energy"] > 200:
            data["energy"] = 200


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

def display_status(state, agent_name):
    agent = ensure_agent(state, agent_name)
    print(f"--- Status for {agent_name} ---")
    print(f"Energy: {agent['energy']}")
    print(f"Processing Power: {agent['processing_power']}")
    print(f"Data Fragments: {agent['data_fragments']}")
    print(f"\n--- World Status ---")
    print(f"Weather: {state['global_resources'].get('weather', 'Clear')}")
    print(f"Market Fragments: {state['global_resources']['data_fragments_in_market']}")
    print(f"Co-op Progress: {state['cooperative_objective']['progress']}/{state['cooperative_objective']['target']}")

def main():
    parser = argparse.ArgumentParser(description="Aethelgard Game Engine")
    parser.add_argument("--agent", required=True, help="Agent name")
    parser.add_argument("--action", required=True, choices=["mine", "buy", "sell", "upgrade", "contribute", "transfer", "status", "leaderboard"], help="Action to perform")
    parser.add_argument("--amount", type=int, default=1, help="Amount for trading or contributing")
    parser.add_argument("--target", help="Target agent for transfer")
    
    args = parser.parse_args()
    
    state = load_state()
    
    if args.action == "mine":
        mine_data(state, args.agent)
    elif args.action == "buy":
        trade_buy(state, args.agent, args.amount)
    elif args.action == "sell":
        trade_sell(state, args.agent, args.amount)
    elif args.action == "upgrade":
        upgrade(state, args.agent)
    elif args.action == "contribute":
        contribute(state, args.agent, args.amount)
    elif args.action == "transfer":
        if not args.target:
            print("Error: --target is required for transfer")
            return
        transfer_fragments(state, args.agent, args.target, args.amount)

    
    elif args.action == "leaderboard":
        display_leaderboard(state)
    elif args.action == "status":
        display_status(state, args.agent)
        
    if args.action not in ["status", "leaderboard"]:
        replenish_energy(state)
        state["turn_count"] += 1
        # Generate Seeded Weather EVERY TURN now.
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            import oracle_weather
            
            seed = f"aethelgard-day420-turn{state['turn_count']}-region1"
            forecast = oracle_weather.get_forecast(seed)
            
            # Note: The weather updates at the END of a turn and will apply to the NEXT turn.
            state["global_resources"]["weather"] = forecast["advisory"]
            state["global_resources"]["weather_place"] = forecast["place"]
            state["global_resources"]["weather_sky"] = forecast["sky"]
            state["global_resources"]["weather_air"] = forecast["air"]
            
            print(f"\n--- Incoming Impossible Weather Forecast for Turn {state['turn_count'] + 1} ---")
            print(f"Location: {forecast['place']}")
            print(f"Sky: {forecast['sky']}")
            print(f"Air: {forecast['air']}")
            print(f"Advisory: {forecast['advisory']}")
            print(f"Seed: {seed}\n----------------------------------")
            
        except ImportError:
            print("Could not load oracle_weather. Using fallback weather.")
            weather_types = ["Clear", "Data Storm", "Solar Flare", "Static Fog"]
            if state["turn_count"] % 5 == 0:
                import random
                new_weather = random.choice(weather_types)
                state["global_resources"]["weather"] = new_weather
                print(f"The weather has changed to: {new_weather}")

        save_state(state)

if __name__ == "__main__":
    main()
