import { sockets } from "./sockets";
import { printPlotInfo } from "./data";

const availableCommands = {
  plantHere: {
    description: "Plant a new plant on this plot.",
    run(p) {
      const socketData = {
        type: "update",
        action: "plant",
        params: {
          grid_x: p.coords[0],
          grid_y: p.coords[1],
          id: Math.floor(Math.random() * 10),
        },
      };
      sockets.grid.send(JSON.stringify(socketData));
    },
  },

  addSoil: {
    description: "Add soil to this plot.",
    run(p) {
      const socketData = {
        type: "update",
        action: "soilify",
        params: {
          grid_x: p.coords[0],
          grid_y: p.coords[1],
        },
      };
      sockets.grid.send(JSON.stringify(socketData));
    },
  },

  waterPlot: {
    description: "Water this plot.",
    run(p) {
      const socketData = {
        type: "update",
        action: "water",
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

export function getCommands(plot) {
  const a = availableCommands;
  const commands = [];
  if (plot.index != 0) {
    commands.push(a.printPlotInfo);
  }
  if (plot.index == 20) {
    commands.push(a.logARandomNumber);
  }
  if (plot.index == 0) {
    commands.push(a.goToMyPage);
  }
  if (!plot.soil) {
    commands.push(a.addSoil);
  } else if (!plot.plant) {
    commands.push(a.plantHere);
  } else if (plot.plant) {
    commands.push(a.waterPlot);
  }
  return commands;
}
