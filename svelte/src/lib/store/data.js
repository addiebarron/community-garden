import { writable, derived } from "svelte/store";
import { clientCursor } from "./cursor";
import { getAlphaCoord } from "./util";
import { sockets } from "./sockets";

export const DATA = writable([]);

// Plot info
export let currentInfo = writable("");

function printPlotInfo(data) {
  const info = JSON.stringify(data, null, 2);
  currentInfo.set(info);
}

// Constructing garden array from API data
export function populateGarden(data) {
  data.unshift({
    id: 0,
    grid_x: 0,
    grid_y: 0,
  });

  const garden = [];
  for (let datum of data) {
    const plot = {};

    plot.type = "none";
    plot.element = null;
    plot.index = datum.id;
    plot.coords = [datum.grid_x, datum.grid_y];
    plot.acoord = getAlphaCoord(...plot.coords);
    plot.plant = datum.plant;
    plot.commands = getCommands(plot);

    garden.push(plot);
  }
  return garden;
}

const availableCommands = {
  incrementPlant: {
    description: "Cycle the plant on this plot.",
    run(p) {
      const socketData = {
        type: "update",
        action: "increment_plant",
        params: {
          grid_x: p.coords[0],
          grid_y: p.coords[1],
        },
      };
      sockets.grid.send(JSON.stringify(socketData));
    },
  },

  printPlotInfo: {
    description: "Show information about this plot.",
    run(p) {
      printPlotInfo(p);
    },
  },

  goToMyPage: {
    description: "Open up my personal site.",
    run(p) {
      window.open("https://addieis.online", "_blank");
    },
  },

  logARandomNumber: {
    description: "Log a random number.",
    run(p) {
      printPlotInfo(Math.floor(100 * Math.random()));
    },
  },
};

function getCommands(plot) {
  const commands = [];
  if (plot.index != 0) {
    commands.push(availableCommands.printPlotInfo);
  }
  if (plot.index == 20) {
    commands.push(availableCommands.logARandomNumber);
  }
  if (plot.index == 0) {
    commands.push(availableCommands.goToMyPage);
  }
  if (typeof plot.plant == "number") {
    commands.push(availableCommands.incrementPlant);
  }
  return commands;
}

export let currentPlot = derived(
  [DATA, clientCursor.index],
  ([$g, $i]) => $g[$i]
);
