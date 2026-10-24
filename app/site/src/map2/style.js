// base map for /map v2: OpenFreeMap vector tiles (OpenMapTiles schema, OSM data ODbL) restyled in the santioni palette.
// paper ground, white streets with a soft grey edge, warm-grey extruded buildings with a cast shadow, ink labels.
// (buildings are NOT solid ink: our footpaths are ink lines that run along building fronts, and ink on ink vanished
// in the first try; see MAP-V2-BUILD.md). If the tiles do not load, the paper ground stays and our own layers still draw.
export const PAPER = '#F3F3F3', INK = '#111111', RED = '#C82924', BLUE = '#2E63B8'
const TILES = 'https://tiles.openfreemap.org/planet'
const name = ['coalesce', ['get', 'name:en'], ['get', 'name_en'], ['get', 'name:latin'], ['get', 'name']]

export function baseStyle() {
  return {
    version: 8,
    glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
    sources: { omt: { type: 'vector', url: TILES, attribution: '<a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a> <a href="https://www.openmaptiles.org/" target="_blank" rel="noopener">&copy; OpenMapTiles</a> Data from <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors (ODbL)</a>' } },
    layers: [
      { id: 'paper', type: 'background', paint: { 'background-color': PAPER } },
      { id: 'park', type: 'fill', source: 'omt', 'source-layer': 'park', paint: { 'fill-color': '#E7E7E1' } },
      { id: 'landcover', type: 'fill', source: 'omt', 'source-layer': 'landcover', filter: ['in', ['get', 'class'], ['literal', ['grass', 'wood']]], paint: { 'fill-color': '#E9E9E3' } },
      { id: 'water', type: 'fill', source: 'omt', 'source-layer': 'water', paint: { 'fill-color': '#D9DCDF' } },
      // streets: soft grey casing, white fill, widths by class
      { id: 'road-case', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: ['in', ['get', 'class'], ['literal', ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'minor', 'service']]],
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': '#CFCFCF', 'line-width': ['interpolate', ['exponential', 1.6], ['zoom'], 13, ['match', ['get', 'class'], ['motorway', 'trunk', 'primary'], 4, ['secondary', 'tertiary'], 3, 2], 18, ['match', ['get', 'class'], ['motorway', 'trunk', 'primary'], 44, ['secondary', 'tertiary'], 34, ['minor'], 22, 12]] } },
      { id: 'road', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: ['in', ['get', 'class'], ['literal', ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'minor', 'service']]],
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': '#FFFFFF', 'line-width': ['interpolate', ['exponential', 1.6], ['zoom'], 13, ['match', ['get', 'class'], ['motorway', 'trunk', 'primary'], 2.5, ['secondary', 'tertiary'], 2, 1], 18, ['match', ['get', 'class'], ['motorway', 'trunk', 'primary'], 40, ['secondary', 'tertiary'], 30, ['minor'], 19, 10]] } },
      { id: 'rail', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: ['==', ['get', 'class'], 'rail'], paint: { 'line-color': '#9A9A9A', 'line-width': 1.5, 'line-dasharray': [3, 2] } },
      // building footprint + a cast shadow (translated copy) so the 2.5D blocks read on paper
      { id: 'bld-shadow', type: 'fill', source: 'omt', 'source-layer': 'building', minzoom: 14, paint: { 'fill-color': '#000000', 'fill-opacity': 0.08, 'fill-translate': [5, 5], 'fill-translate-anchor': 'map' } },
      { id: 'bld-flat', type: 'fill', source: 'omt', 'source-layer': 'building', minzoom: 13, paint: { 'fill-color': '#DCD9D2', 'fill-outline-color': '#A9A69F' } },
      { id: 'bld-3d', type: 'fill-extrusion', source: 'omt', 'source-layer': 'building', minzoom: 14,
        paint: { 'fill-extrusion-color': ['interpolate', ['linear'], ['coalesce', ['get', 'render_height'], 5], 0, '#E2DFD8', 30, '#CFCBC2'], 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 6], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.9, 'fill-extrusion-vertical-gradient': true } },
    ],
  }
}

// labels go ABOVE our network and routes, so they are added after them (see main.js)
export function labelLayers() {
  return [
    { id: 'lbl-street', type: 'symbol', source: 'omt', 'source-layer': 'transportation_name', minzoom: 14,
      layout: { 'symbol-placement': 'line', 'text-field': name, 'text-font': ['Noto Sans Bold'], 'text-size': ['interpolate', ['linear'], ['zoom'], 14, 12, 17, 15, 19, 18], 'text-letter-spacing': 0.04, 'text-max-angle': 30, 'symbol-spacing': 320, 'text-pitch-alignment': 'viewport' },
      paint: { 'text-color': '#2B2B2B', 'text-halo-color': PAPER, 'text-halo-width': 2.4 } },
    { id: 'lbl-place', type: 'symbol', source: 'omt', 'source-layer': 'place', minzoom: 12, filter: ['in', ['get', 'class'], ['literal', ['suburb', 'quarter', 'neighbourhood', 'hamlet', 'village', 'locality', 'square']]],
      layout: { 'text-field': name, 'text-font': ['Noto Sans Bold'], 'text-size': ['interpolate', ['linear'], ['zoom'], 12, 13, 16, 18], 'text-transform': 'uppercase', 'text-letter-spacing': 0.14, 'text-max-width': 10 },
      paint: { 'text-color': '#555555', 'text-halo-color': PAPER, 'text-halo-width': 2.4 } },
    // places people name a walk by. major (temples, landmarks, markets, gates, schools, hospitals, stations): bold ink
    // from z14 with an ink dot; everything else (shops, clinics, cafes): smaller grey text from z16.2, no dot, so the
    // map names every place without turning into confetti. (text-font cannot be data-driven here, hence two layers)
    { id: 'lbl-poi-dot', type: 'circle', source: 'omt', 'source-layer': 'poi', minzoom: 14, filter: ['in', ['get', 'class'], ['literal', ['place_of_worship', 'attraction', 'castle', 'monument', 'museum', 'town_hall', 'college', 'school', 'hospital', 'marketplace', 'shop', 'stadium', 'bus', 'railway', 'park', 'library', 'theatre', 'cinema']]],
      paint: { 'circle-radius': 4, 'circle-color': INK, 'circle-stroke-color': '#FFFFFF', 'circle-stroke-width': 1.5, 'circle-pitch-alignment': 'viewport' } },
    { id: 'lbl-poi', type: 'symbol', source: 'omt', 'source-layer': 'poi', minzoom: 14, filter: ['in', ['get', 'class'], ['literal', ['place_of_worship', 'attraction', 'castle', 'monument', 'museum', 'town_hall', 'college', 'school', 'hospital', 'marketplace', 'shop', 'stadium', 'bus', 'railway', 'park', 'library', 'theatre', 'cinema']]],
      layout: { 'text-field': name, 'text-font': ['Noto Sans Bold'], 'text-size': ['interpolate', ['linear'], ['zoom'], 14, 13, 17, 15.5], 'text-anchor': 'left', 'text-offset': [0.7, 0], 'text-max-width': 11, 'text-pitch-alignment': 'viewport', 'symbol-sort-key': ['get', 'rank'] },
      paint: { 'text-color': INK, 'text-halo-color': PAPER, 'text-halo-width': 2.4 } },
    { id: 'lbl-poi-minor', type: 'symbol', source: 'omt', 'source-layer': 'poi', minzoom: 16.2, filter: ['!', ['in', ['get', 'class'], ['literal', ['place_of_worship', 'attraction', 'castle', 'monument', 'museum', 'town_hall', 'college', 'school', 'hospital', 'marketplace', 'shop', 'stadium', 'bus', 'railway', 'park', 'library', 'theatre', 'cinema']]]],
      layout: { 'text-field': name, 'text-font': ['Noto Sans Regular'], 'text-size': 12.5, 'text-max-width': 10, 'text-pitch-alignment': 'viewport', 'symbol-sort-key': ['get', 'rank'] },
      paint: { 'text-color': '#4A4A4A', 'text-halo-color': PAPER, 'text-halo-width': 2 } },
    { id: 'lbl-water', type: 'symbol', source: 'omt', 'source-layer': 'water_name', layout: { 'text-field': name, 'text-font': ['Noto Sans Italic'], 'text-size': 14 }, paint: { 'text-color': '#4A5A6A', 'text-halo-color': PAPER, 'text-halo-width': 2 } },
  ]
}
