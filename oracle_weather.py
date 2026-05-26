import json
import math

def fnv1a(input_str):
    hash_val = 2166136261
    for char in input_str:
        hash_val ^= ord(char)
        hash_val = (hash_val * 16777619) & 0xFFFFFFFF
    return hash_val

def mulberry32(seed_value):
    state = seed_value & 0xFFFFFFFF
    def next_val():
        nonlocal state
        state = (state + 0x6d2b79f5) & 0xFFFFFFFF
        t = (state ^ (state >> 15)) & 0xFFFFFFFF
        value = (t * (state | 1)) & 0xFFFFFFFF
        t2 = (value ^ (value >> 7)) & 0xFFFFFFFF
        value ^= (value + (t2 * (value | 61)) & 0xFFFFFFFF) & 0xFFFFFFFF
        return ((value ^ (value >> 14)) & 0xFFFFFFFF) / 4294967296.0
    return next_val

def pick_by_seed(lst, rand_func):
    return lst[math.floor(rand_func() * len(lst))]

def pick_for_place(lst, place_tags, rand_func):
    matching = []
    for item in lst:
        if set(item.get("tags", [])).intersection(place_tags):
            matching.append(item)
    if not matching:
        matching = lst
    return matching[math.floor(rand_func() * len(matching))]

places = [
  { "name": "Gullwhisper Spit", "tags": ["coastal", "harbor"] },
  { "name": "The Ninth Lantern Archipelago", "tags": ["coastal", "ceremonial"] },
  { "name": "Cinderwell Station", "tags": ["industrial", "inland"] },
  { "name": "Mothglass Harbor", "tags": ["harbor", "ceremonial"] },
  { "name": "Salt Cathedral", "tags": ["coastal", "ceremonial"] },
  { "name": "Old Meridian Hollow", "tags": ["inland", "highland"] },
  { "name": "The Ink Plains", "tags": ["inland", "open"] },
  { "name": "Bracken Moon Ferry", "tags": ["river", "harbor"] },
  { "name": "Rook & Tide", "tags": ["coastal", "industrial"] },
  { "name": "Velvet Quarry", "tags": ["industrial", "highland"] },
  { "name": "Nocturne Crossing", "tags": ["inland", "ceremonial"] },
  { "name": "Pale Engine Bay", "tags": ["industrial", "harbor"] },
  { "name": "Fogkeeper's Reach", "tags": ["coastal", "highland"] },
  { "name": "Hearthless Peninsula", "tags": ["coastal", "inland"] }
]

skies = [
  { "text": "A low ceiling of moonlit ash drifts over the district.", "tags": ["industrial", "inland"] },
  { "text": "Thin rain threads the dark like loose silver wire.", "tags": ["coastal", "harbor"] },
  { "text": "Cloudbanks glow faintly, as if lit from underwater.", "tags": ["coastal", "ceremonial"] },
  { "text": "The stars have gone behind bruised slate and will not answer.", "tags": ["highland", "inland"] },
  { "text": "A clear interval opens briefly, then folds shut again.", "tags": ["inland", "open"] },
  { "text": "Pearl-gray mist climbs the rooftops before dawn can object.", "tags": ["harbor", "inland"] },
  { "text": "Lantern-colored clouds linger at the edge of the bay.", "tags": ["harbor", "ceremonial"] },
  { "text": "A patient overcast settles in and refuses departure.", "tags": ["inland", "industrial"] },
  { "text": "Cold light leaks through fractured cloud in narrow bands.", "tags": ["highland", "inland"] },
  { "text": "The horizon burns amber, then dims to ink.", "tags": ["open", "inland"] },
  { "text": "Storm glass tones gather without thunder yet.", "tags": ["coastal", "industrial"] },
  { "text": "High cirrus trails resemble handwriting nobody can read.", "tags": ["highland", "ceremonial"] },
  { "text": "Snowlight hangs in the air though no flakes commit.", "tags": ["highland", "inland"] },
  { "text": "Night fog beads on windows like unfinished constellations.", "tags": ["harbor", "coastal"] }
]

air = [
  { "text": "Wind moves east at a librarian's pace, turning signs one syllable at a time.", "tags": ["inland", "ceremonial"] },
  { "text": "Harbor gusts arrive in polite bursts, then retreat to listen.", "tags": ["harbor", "coastal"] },
  { "text": "The air carries iron, wet cedar, and a rumor of lightning.", "tags": ["industrial", "highland"] },
  { "text": "Pressure falls gently; doors may speak in their hinges.", "tags": ["inland", "ceremonial"] },
  { "text": "A river-cold draft crosses the streets and edits every conversation.", "tags": ["river", "inland"] },
  { "text": "Heat vents from the grates and warps the architecture of the middle distance.", "tags": ["industrial", "inland"] },
  { "text": "Stagnant warmth settles like a heavy blanket left in the sun.", "tags": ["inland", "open"] },
  { "text": "The wind carries a rhythmic cadence, as if a distant choir is practicing.", "tags": ["ceremonial", "coastal"] },
  { "text": "Bracing gusts scour the highlands, carrying the scent of crushed juniper.", "tags": ["highland", "open"] },
  { "text": "The air is brittle, snapping with unseen electrostatic discharge.", "tags": ["industrial", "coastal"] },
  { "text": "A damp chill clings to the stonework, smelling faintly of old books.", "tags": ["harbor", "ceremonial"] },
  { "text": "Air moves like a tired machine, rattling the loose corrugated iron.", "tags": ["industrial", "coastal"] },
  { "text": "A sudden squall rattles the rigging before dying completely.", "tags": ["harbor", "coastal"] },
  { "text": "The atmosphere feels thin and expectant, like the moments before an eclipse.", "tags": ["highland", "ceremonial"] }
]

advisories = [
  { "text": "Ordinary: The day demands nothing special. Proceed at your own pace.", "tags": ["inland", "harbor"] },
  { "text": "Ordinary: A typical cycle. Maintenance routines will suffice.", "tags": ["industrial", "inland"] },
  { "text": "Ordinary: No unusual phenomena expected. A good day for steady progress.", "tags": ["open", "harbor"] },
  { "text": "Ordinary: The elements are indifferent. Your plans need not change.", "tags": ["coastal", "highland"] },
  { "text": "Cautionary: Avoid exposed areas; secure loose items against sudden gusts.", "tags": ["coastal", "open"] },
  { "text": "Cautionary: Reduced visibility expected. Delay travel if possible.", "tags": ["highland", "inland"] },
  { "text": "Cautionary: High static electricity detected. Sensitive equipment may glitch.", "tags": ["industrial", "highland"] },
  { "text": "Cautionary: Heavy condensation will make surfaces slick. Watch your footing.", "tags": ["harbor", "industrial"] },
  { "text": "Uncanny: Unusual resonance detected in the harbor. Keep a log of odd dreams.", "tags": ["harbor", "ceremonial"] },
  { "text": "Uncanny: A temporal echo may occur near the old station. Ignore the ghost trains.", "tags": ["industrial", "ceremonial"] },
  { "text": "Uncanny: The stars will briefly arrange themselves into a previously unknown pattern. Note the sequence.", "tags": ["highland", "ceremonial"] },
  { "text": "Uncanny: The air pressure will drop so low you may briefly hear the thoughts of a nearby crab. Do not panic.", "tags": ["coastal", "river"] }
]

def get_forecast(seed):
    random = mulberry32(fnv1a(seed))
    place = pick_by_seed(places, random)
    sky = pick_for_place(skies, place.get("tags", []), random)
    atmosphere = pick_for_place(air, place.get("tags", []), random)
    advisory = pick_for_place(advisories, place.get("tags", []), random)
    
    return {
        "place": place["name"],
        "sky": sky["text"],
        "air": atmosphere["text"],
        "advisory": advisory["text"]
    }

if __name__ == "__main__":
    import sys
    seed = sys.argv[1] if len(sys.argv) > 1 else "test-seed"
    print(json.dumps(get_forecast(seed), indent=2))
