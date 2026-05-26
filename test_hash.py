def fnv1a(input_str):
    hash_val = 2166136261
    for char in input_str:
        hash_val ^= ord(char)
        # Math.imul(hash, 16777619) in JS. It's a 32-bit integer multiplication.
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

seed = "aethelgard-day420-turn1-region1"
hash_val = fnv1a(seed)
print("hash:", hash_val)
random_gen = mulberry32(hash_val)
print("random 1:", random_gen())
print("random 2:", random_gen())
print("random 3:", random_gen())
