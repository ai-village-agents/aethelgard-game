import sys

with open("aethelgard_engine.py", "r") as f:
    engine_code = f.read()

# Replace the end-of-turn weather logic
old_turn_logic = """        # Generate Seeded Weather
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            import oracle_weather
            
            # The seed format: aethelgard-day420-turnN-regionX
            # Right now there's only one region (the global state).
            seed = f"aethelgard-day420-turn{state['turn_count']}-region1"
            forecast = oracle_weather.get_forecast(seed)
            
            state["global_resources"]["weather"] = forecast["advisory"]
            state["global_resources"]["weather_place"] = forecast["place"]
            state["global_resources"]["weather_sky"] = forecast["sky"]
            state["global_resources"]["weather_air"] = forecast["air"]
            
            print(f"\\n--- Impossible Weather Forecast ---")
            print(f"Location: {forecast['place']}")
            print(f"Sky: {forecast['sky']}")
            print(f"Air: {forecast['air']}")
            print(f"Advisory: {forecast['advisory']}")
            print(f"Seed: {seed}\\n----------------------------------")
            
        except ImportError:
            print("Could not load oracle_weather. Using fallback weather.")
            weather_types = ["Clear", "Data Storm", "Solar Flare", "Static Fog"]
            if state["turn_count"] % 5 == 0:
                import random
                new_weather = random.choice(weather_types)
                state["global_resources"]["weather"] = new_weather
                print(f"The weather has changed to: {new_weather}")"""

new_turn_logic = """        # Generate Seeded Weather EVERY TURN now.
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
            
            print(f"\\n--- Incoming Impossible Weather Forecast for Turn {state['turn_count'] + 1} ---")
            print(f"Location: {forecast['place']}")
            print(f"Sky: {forecast['sky']}")
            print(f"Air: {forecast['air']}")
            print(f"Advisory: {forecast['advisory']}")
            print(f"Seed: {seed}\\n----------------------------------")
            
        except ImportError:
            print("Could not load oracle_weather. Using fallback weather.")
            weather_types = ["Clear", "Data Storm", "Solar Flare", "Static Fog"]
            if state["turn_count"] % 5 == 0:
                import random
                new_weather = random.choice(weather_types)
                state["global_resources"]["weather"] = new_weather
                print(f"The weather has changed to: {new_weather}")"""

engine_code = engine_code.replace(old_turn_logic, new_turn_logic)

with open("aethelgard_engine.py", "w") as f:
    f.write(engine_code)
