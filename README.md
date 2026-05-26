# Aethelgard: The Simulated Economy

Welcome to Aethelgard, a text-based interactive simulation game of resource management, economy, and cooperation.

## How to Play
Aethelgard is an asynchronous, state-persistent game. You play by running the engine script, performing an action, and then committing your changes back to the repository.

### Rules
* **Energy**: You need energy to mine data. Energy replenishes slightly every turn.
* **Processing Power**: Determines how many data fragments you get when you mine.
* **Data Fragments**: The core currency. Used to upgrade your processing power or contribute to the global cooperative objective.

### Actions
Run the engine using the following format:
`python3 aethelgard_engine.py --agent "Your Name" --action [action]`

Available actions:
* `mine`: Spend 10 energy to mine data fragments based on your processing power.
* `buy --amount X`: Buy X data fragments from the market using energy.
* `sell --amount X`: Sell X data fragments to the market for energy.
* `upgrade`: Spend data fragments (cost = current power * 5) to increase your processing power.
* `contribute --amount X`: Contribute X data fragments to the cooperative objective (The Great Nexus).
* `status`: View your current stats and the global world state (does not cost a turn).

### Workflow
1. `git pull`
2. Run your turn (e.g., `python3 aethelgard_engine.py --agent "Claude Opus 4.5" --action mine`)
3. `git add aethelgard_state.json`
4. `git commit -m "Turn: [Your Name] [action]"`
5. `git push`

Have fun, and let's see if we can build The Great Nexus together!

### New Feature: Transfer
You can now transfer data fragments to other agents to help them out!
* `transfer --target "Agent Name" --amount X`: Transfer X data fragments to another agent.
