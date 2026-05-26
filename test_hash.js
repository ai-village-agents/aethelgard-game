function fnv1a(input) {
  let hash = 2166136261;
  for (let i = 0; i < input.length; i += 1) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function mulberry32(seedValue) {
  let state = seedValue >>> 0;
  return function next() {
    state = (state + 0x6d2b79f5) >>> 0;
    let value = Math.imul(state ^ (state >>> 15), state | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

let seed = "aethelgard-day420-turn1-region1";
let hash_val = fnv1a(seed);
console.log("hash:", hash_val);
let random_gen = mulberry32(hash_val);
console.log("random 1:", random_gen());
console.log("random 2:", random_gen());
console.log("random 3:", random_gen());
