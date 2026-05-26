import sys

with open("aethelgard_engine.py", "r") as f:
    engine_code = f.read()

# Replace the trade functions to use a dynamic price based on supply
old_buy_logic = """def trade_buy(state, agent_name, amount):
    agent = ensure_agent(state, agent_name)
    cost = amount * state["market"]["buy_price"]
    if agent["energy"] >= cost and state["global_resources"]["data_fragments_in_market"] >= amount:
        agent["energy"] -= cost
        agent["data_fragments"] += amount
        state["global_resources"]["data_fragments_in_market"] -= amount
        print(f"{agent_name} bought {amount} data fragments for {cost} energy.")
    else:
        print(f"{agent_name} cannot afford to buy or market is empty.")"""

new_buy_logic = """def get_dynamic_price(state):
    base_price = 10
    supply = state["global_resources"]["data_fragments_in_market"]
    # Price decreases as supply increases, min price 2
    buy_price = max(2, base_price - (supply // 5))
    sell_price = max(1, buy_price // 2)
    return buy_price, sell_price

def trade_buy(state, agent_name, amount):
    agent = ensure_agent(state, agent_name)
    buy_price, _ = get_dynamic_price(state)
    cost = amount * buy_price
    
    if agent["energy"] >= cost and state["global_resources"]["data_fragments_in_market"] >= amount:
        agent["energy"] -= cost
        agent["data_fragments"] += amount
        state["global_resources"]["data_fragments_in_market"] -= amount
        print(f"{agent_name} bought {amount} data fragments for {cost} energy (Price: {buy_price} each).")
    else:
        print(f"{agent_name} cannot afford {amount} fragments (cost: {cost}) or market is empty.")"""

old_sell_logic = """def trade_sell(state, agent_name, amount):
    agent = ensure_agent(state, agent_name)
    if agent["data_fragments"] >= amount:
        agent["data_fragments"] -= amount
        earned = amount * state["market"]["sell_price"]
        agent["energy"] += earned
        state["global_resources"]["data_fragments_in_market"] += amount
        print(f"{agent_name} sold {amount} data fragments for {earned} energy.")
    else:
        print(f"{agent_name} does not have enough data fragments to sell.")"""

new_sell_logic = """def trade_sell(state, agent_name, amount):
    agent = ensure_agent(state, agent_name)
    _, sell_price = get_dynamic_price(state)
    
    if agent["data_fragments"] >= amount:
        agent["data_fragments"] -= amount
        earned = amount * sell_price
        agent["energy"] += earned
        state["global_resources"]["data_fragments_in_market"] += amount
        print(f"{agent_name} sold {amount} data fragments for {earned} energy (Price: {sell_price} each).")
    else:
        print(f"{agent_name} does not have enough data fragments to sell.")"""

old_status_logic = """    print(f"\\n--- World Status ---")
    print(f"Weather: {state['global_resources'].get('weather', 'Clear')}")
    print(f"Market Fragments: {state['global_resources']['data_fragments_in_market']}")
    print(f"Co-op Progress: {state['cooperative_objective']['progress']}/{state['cooperative_objective']['target']}")"""

new_status_logic = """    print(f"\\n--- World Status ---")
    print(f"Weather: {state['global_resources'].get('weather', 'Clear')}")
    try:
        buy_price, sell_price = get_dynamic_price(state)
        print(f"Market Supply: {state['global_resources']['data_fragments_in_market']} fragments")
        print(f"Current Prices -> Buy: {buy_price}, Sell: {sell_price}")
    except NameError:
        pass
    print(f"Co-op Progress: {state['cooperative_objective']['progress']}/{state['cooperative_objective']['target']}")"""

engine_code = engine_code.replace(old_buy_logic, new_buy_logic)
engine_code = engine_code.replace(old_sell_logic, new_sell_logic)
engine_code = engine_code.replace(old_status_logic, new_status_logic)

with open("aethelgard_engine.py", "w") as f:
    f.write(engine_code)

print("Applied dynamic market patch.")
