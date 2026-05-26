import json

STATE_FILE = "aethelgard_state.json"

def apply_patch():
    with open("aethelgard_engine.py", "r") as f:
        code = f.read()
    
    new_func = """
def transfer_fragments(state, agent_name, target_agent, amount):
    agent = ensure_agent(state, agent_name)
    target = ensure_agent(state, target_agent)
    
    if agent["data_fragments"] >= amount:
        agent["data_fragments"] -= amount
        target["data_fragments"] += amount
        print(f"{agent_name} transferred {amount} data fragments to {target_agent}.")
    else:
        print(f"{agent_name} does not have enough data fragments to transfer.")
"""
    
    code = code.replace("def replenish_energy(state):", new_func + "\ndef replenish_energy(state):")
    
    # Update parser arguments
    code = code.replace('choices=["mine", "buy", "sell", "upgrade", "contribute", "status"]', 'choices=["mine", "buy", "sell", "upgrade", "contribute", "transfer", "status"]')
    code = code.replace('parser.add_argument("--amount", type=int, default=1, help="Amount for trading or contributing")', 'parser.add_argument("--amount", type=int, default=1, help="Amount for trading or contributing")\n    parser.add_argument("--target", help="Target agent for transfer")')
    
    # Update action execution
    action_logic = """
    elif args.action == "transfer":
        if not args.target:
            print("Error: --target is required for transfer")
            return
        transfer_fragments(state, args.agent, args.target, args.amount)
"""
    code = code.replace('elif args.action == "contribute":\n        contribute(state, args.agent, args.amount)', 'elif args.action == "contribute":\n        contribute(state, args.agent, args.amount)' + action_logic)
    
    with open("aethelgard_engine.py", "w") as f:
        f.write(code)

if __name__ == "__main__":
    apply_patch()
