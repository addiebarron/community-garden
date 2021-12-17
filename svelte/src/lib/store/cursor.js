import { writable, derived, get } from "svelte/store";
import { coordsToIndex, indexToCoords, bound } from "./util";

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

export let otherCursors = writable([]);
