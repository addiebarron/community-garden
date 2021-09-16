import { writable, derived, get } from "svelte/store";
import { API_URL } from "$lib/store/settings";

// WebSocket wrapper
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
    const protocol = window.location.protocol == "https:" ? "wss" : "ws";
    this._socket = new WebSocket(`${protocol}://${API_URL}/ws/${this.name}`);
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

// Array derived store
export let allSocketsConnected = derived(
  Object.values(sockets).map((socket) => socket.open),
  ([...arr]) => {
    return arr.every(($open) => $open);
  }
);
