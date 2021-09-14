import { indexToCoords, coordsToIndex, bound } from "./util";

import { readable, writable, derived, get } from "svelte/store";

/* --- Constants --- */

export const GRID_X = 20;
export const GRID_Y = 20;

export const apiURL = import.meta.env.DEV
  ? "localhost:9090"
  : import.meta.env.VITE_API_BASE_URL;

/* --- Logging --- */

export let logHistory = writable([]);
export const log = (...args) =>
  logHistory.update((text) => text.concat([...args]));

/* --- Settings --- */

// Zoom
export const ZOOM_LEVEL = writable(1);

// Reduce motion
export const prefersReducedMotion = readable(true, function start(set) {
  let stop = () => {};
  if (typeof window != "undefined") {
    let mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const setMatches = () => set(mediaQuery.matches);
    setMatches();
    mediaQuery.addEventListener("change", setMatches);
    stop = () => mediaQuery.removeEventListener("change", setMatches);
  }
  return stop;
});

// Controls
export const controlsMap = {
  ArrowRight: "moveRight",
  ArrowLeft: "moveLeft",
  ArrowUp: "moveUp",
  ArrowDown: "moveDown",
  Space: "clear",
};

/* --- Data --- */

// Websockets

class Socket {
  constructor(name) {
    this.name = name;
    this.open = writable(false);
  }

  get opened() {
    return get(this.open);
  }

  connect(callback) {
    // TODO error handling
    let protocol = window.location.protocol == "https:" ? "wss" : "ws";
    this._socket = new WebSocket(`${protocol}://${apiURL}/ws/${this.name}`);
    this.onConnect((e) => {
      this.open.set(true);
      if (typeof callback == "function") callback(e);
    });
  }

  send(message, callback) {
    if (this.opened) {
      this._socket.send(message);
      if (typeof callback == "function") callback();
    } else {
      console.log(
        `Cannot send message to socket "${this.name}": socket closed.`
      );
    }
  }

  onConnect(func) {
    if (!this.opened) {
      this._socket.addEventListener("open", func);
    }
  }

  onMessage(func) {
    this._socket.addEventListener("message", (e) => {
      if (typeof func == "function") func(e);
    });
  }
}

export let sockets = {
  grid: new Socket("grid"),
  cursor: new Socket("cursor"),
};

const openStoreArray = Object.values(sockets).map((socket) => socket.open);
export let allSocketsConnected = derived(openStoreArray, ([...arr]) => {
  return arr.every(($open) => $open);
});

// Plot info
export let currentInfo = writable("");

function printPlotInfo(data) {
  const info = JSON.stringify(data, null, 2);
  currentInfo.set(info);
}

// Grid data

export function populateGarden(arr) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  arr.unshift({
    grid_x: 0,
    grid_y: 0,
  });
  const gridData = arr.map((plot) => {
    let [x, y] = [plot.grid_x, plot.grid_y];
    return {
      type: "none",
      element: null,
      index: plot.id - 1,
      coords: [x, y],
      acoord: !!alphabet[x - 1] ? alphabet[x - 1] + y : "",
      plant: plot.plant,
      commands: [
        // The default command
        {
          name: "log info",
          run: (p) => logInfo(p),
        },
        {
          name: "increment",
          run: (p) => {
            console.log("incrementing plant:", p.coords);
            sockets.grid.send(
              JSON.stringify({
                type: "update",
                action: "increment_plant",
                params: {
                  grid_x: p.coords[0],
                  grid_y: p.coords[1],
                },
              })
            );
          },
        },
      ],
    };
  });
  gridData[0].commands.push({
    name: "go to my page",
    run: () => logInfo("https://addieis.online"),
  });
  gridData[20].commands.push({
    name: "log a random number",
    run: () => logInfo(Math.floor(100 * Math.random())),
  });
  // turn it into a store
  // later -- readable that can only be updated via API?
  return gridData;
}

export const gardenData = writable([]);

export function addGlobalCommand(name, run) {
  gardenData.update((garden) => {
    garden.forEach((plot) => plot.commands.push({ name, run }));
    return garden;
  });
}

// Cursor
// Does this need to be a class? Other players' cursors may be read in without corresponding functions
export class Cursor {
  // Initial cursor position
  constructor(x = 0, y = 0) {
    this.x = writable(x);
    this.y = writable(y);
    this.coords = derived([this.x, this.y], ([$x, $y]) => [$x, $y]);
    this.index = derived([this.x, this.y], ([$x, $y]) => coordsToIndex($x, $y));
  }

  // Set position of cursor given xy coordinates
  set(x, y) {
    [x, y] = bound(x, y); // 0,0 is allowed
    this.x.set(x);
    this.y.set(y);
  }

  get pos() {
    return get(this.coords);
  }

  // Set position of cursor given an array index
  setFromIndex(index) {
    this.set(...indexToCoords(index));
  }

  // Clear position of cursor
  clear() {
    this.set(0, 0);
  }
}

export class PlayerCursor extends Cursor {
  // Move in direction
  moveUp() {
    this.set(get(this.x), get(this.y) - 1);
  }
  moveDown() {
    this.set(get(this.x), get(this.y) + 1);
  }
  moveRight() {
    this.set(get(this.x) + 1, get(this.y));
  }
  moveLeft() {
    this.set(get(this.x) - 1, get(this.y));
  }
}

export let clientCursor = new PlayerCursor();
