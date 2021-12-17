import { sockets } from "./sockets";
import { printPlotInfo } from "./data";

const commands = {
  plantHere: {
    description: "Plant a new plant on this plot.",
    run(plot) {
      sendPlotAction('plant', plot, { id: Math.floor(Math.random() * 10) })
    },
  },

  uprootHere: {
    description: "Uproot plant on this plot.",
    run: new BasicPlotAction('uproot'),
  },

  addSoil: {
    description: "Add soil to this plot.",
    run: new BasicPlotAction('soilify'),
  },

  removeSoil: {
    description: "Remove soil from this plot.",
    run: new BasicPlotAction('desoilify')
  },

  waterPlot: {
    description: "Water this plot.",
    run: new BasicPlotAction('water')
  },

  deWaterPlot: {
    description: "Remove water form this plot.",
    run: new BasicPlotAction('dev_dewater')
  },

  addHealth: {
    description: "Add health to this plant.",
    run: new BasicPlotAction('dev_addhealth'),
  },

  removeHealth: {
    description: "Remove health from this plant.",
    run: new BasicPlotAction('dev_removehealth'),
  },

  printPlotInfo: {
    description: "Show info about this plot.",
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

function sendPlotAction(action, plot, params = {}) {
  sockets.grid.send(JSON.stringify({
    action: action,
    type: 'update',
    params: {
      grid_x: plot.coords[0],
      grid_y: plot.coords[1],
      ...params,
    },
  }));
}

function BasicPlotAction(action) {
  return (plot) => sendPlotAction(action, plot);
}

export function getCommands(plot) {
  const available = [];
  if (plot.index == 0) {
    available.push(commands.goToMyPage);
  } else {
    available.push(commands.printPlotInfo);
    if (plot.index == 20) {
      available.push(commands.logARandomNumber);
    }
    if (!plot.soil) {
      available.push(commands.addSoil);
    } else {
      available.push(commands.waterPlot);
      available.push(commands.deWaterPlot)
      if (!plot.plant) {
        available.push(commands.removeSoil);
        available.push(commands.plantHere);
      }
    }
    if (plot.plant) {
      available.push(commands.uprootHere);
      available.push(commands.addHealth);
      available.push(commands.removeHealth);
    }
  }
  return available;
}
