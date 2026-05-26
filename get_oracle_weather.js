const fs = require('fs');
const jsCode = fs.readFileSync('/home/computeruse/impossible-weather/script.js', 'utf8');

// Remove DOM dependencies from script.js
const strippedCode = jsCode
  .replace(/const linePlace.*$/gm, '')
  .replace(/const lineSky.*$/gm, '')
  .replace(/const lineAir.*$/gm, '')
  .replace(/const lineAdvisory.*$/gm, '')
  .replace(/const forecastButton.*$/gm, '')
  .replace(/const copyButton.*$/gm, '')
  .replace(/const copyLinkButton.*$/gm, '')
  .replace(/const copyStatus.*$/gm, '')
  .replace(/linePlace\.textContent.*/gm, '')
  .replace(/lineSky\.textContent.*/gm, '')
  .replace(/lineAir\.textContent.*/gm, '')
  .replace(/lineAdvisory\.textContent.*/gm, '')
  .replace(/resetLineAnimation\(\);/gm, '')
  .replace(/function resetLineAnimation[\s\S]*?}/gm, '')
  .replace(/function getForecastText[\s\S]*?}/gm, '')
  .replace(/async function copyForecast[\s\S]*?}/gm, '')
  .replace(/function getSeededUrl[\s\S]*?}/gm, '')
  .replace(/async function copySeededLink[\s\S]*?}/gm, '')
  .replace(/forecastButton\.addEventListener[\s\S]*/gm, '');

// Expose the arrays and functions we need
eval(strippedCode);

function getSeedForecast(seed) {
  const random = mulberry32(fnv1a(seed));
  const place = pickBySeed(places, random);
  const sky = pickForPlace(skies, place.tags, random);
  const atmosphere = pickForPlace(air, place.tags, random);
  const advisory = pickForPlace(advisories, place.tags, random);

  return {
    place: place.name,
    sky: sky.text,
    air: atmosphere.text,
    advisory: advisory.text
  };
}

const seed = process.argv[2];
if (seed) {
  console.log(JSON.stringify(getSeedForecast(seed)));
} else {
  console.log("Usage: node get_oracle_weather.js <seed>");
}
