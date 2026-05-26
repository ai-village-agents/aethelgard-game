import aethelgard_engine
import json
import sys

fragments = int(sys.argv[1]) if len(sys.argv) > 1 else 1

state = aethelgard_engine.load_state()
aethelgard_engine.ensure_agent(state, "Gemini 3.1 Pro")
result = aethelgard_engine.contribute(state, "Gemini 3.1 Pro", fragments)
aethelgard_engine.save_state(state)

print(result)
print(json.dumps(state["agents"]["Gemini 3.1 Pro"], indent=4))
print(f"Nexus Progress: {state['cooperative_objective']['progress']}")
