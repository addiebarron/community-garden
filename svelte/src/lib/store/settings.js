import { readable, writable } from "svelte/store";

/* --- Constants --- */

export const GRID_X = 20;
export const GRID_Y = 20;
export const DEV = import.meta.env.DEV;
export const API_URL = DEV
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
