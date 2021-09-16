import { GRID_X, GRID_Y } from "./settings";

export function coordsToIndex(x, y) {
  if (y * x == 0) return 0;
  return (y - 1) * GRID_X + x;
}

// Convert array index to xy coordinates
export function indexToCoords(i) {
  if (i == 0) return [0, 0];

  let y = Math.ceil(i / GRID_X);
  let x = i - GRID_X * (y - 1);

  return [x, y];
}

// Reset cursor coordinates so they stay within the grid
export function bound(x, y) {
  // 0,0 is allowed (unselected)
  if (x == 0 && y == 0) return [x, y];

  return [
    // Otherwise, bound between 1 and GRID_*
    Math.min(Math.max(1, x), GRID_X),
    Math.min(Math.max(1, y), GRID_Y),
  ];
}

export function getAlphaCoord(x, y) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  return !!alphabet[x - 1] ? alphabet[x - 1] + y : "";
}
