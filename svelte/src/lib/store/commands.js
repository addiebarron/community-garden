import { sockets } from "./sockets";
import { printPlotInfo } from "./data";

const commands = {
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

  uprootHere: {
    description: "Uproot plant on this plot.",
    run(p) {
      const socketData = {
        type: "update",
        action: "uproot",
        params: {
          grid_x: p.coords[0],
          grid_y: p.coords[1],
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

  removeSoil: {
    description: "Remove soil from this plot.",
    run(p) {
      const socketData = {
        type: "update",
        action: "desoilify",
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
  const available = [];
  if (plot.index != 0) {
    available.push(commands.printPlotInfo);
  }
  if (plot.index == 20) {
    available.push(commands.logARandomNumber);
  }
  if (plot.index == 0) {
    available.push(commands.goToMyPage);
  }
  if (!plot.soil) {
    available.push(commands.addSoil);
  } else {
    available.push(commands.waterPlot);
    if (!plot.plant) {
      available.push(commands.removeSoil);
      available.push(commands.plantHere);
    }
  }
  if (plot.plant) {
    available.push(commands.uprootHere);
  }
  return available;
}
