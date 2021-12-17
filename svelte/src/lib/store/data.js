import { writable, derived } from "svelte/store";
import { clientCursor } from "./cursor";
import { getAlphaCoord } from "./util";
import { getCommands } from "./commands";

export const currentInfo = writable("");

export function printPlotInfo(data) {
  const info = JSON.stringify(data, null, 2);
  currentInfo.set(info);
}

export const DATA = writable([]);

export let currentPlot = derived(
  [DATA, clientCursor.index],
  ([$g, $i]) => $g[$i]
);

// Constructing garden array from API data
export function hydrateData(data) {
  data.unshift({
    id: 0,
    grid_x: 0,
    grid_y: 0,
  });

  const garden = [];
  for (let datum of data) {
    const plot = {};

    plot.element = null;
    plot.index = datum.id;
    plot.coords = [datum.grid_x, datum.grid_y];
    plot.acoord = getAlphaCoord(...plot.coords);
    plot.soil = datum.soil;
    plot.plant = datum.plant;
    plot.commands = getCommands(plot);

    garden.push(plot);
  }
  return garden;
}

