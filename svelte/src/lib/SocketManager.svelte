<script>
  import LoadingOverlay from "$lib/LoadingOverlay.svelte";

  import { DATA, hydrateData } from "$lib/store/data";
  import { sockets, allSocketsConnected } from "$lib/store/sockets";
  import { Cursor, otherCursors } from "$lib/store/cursor";
  import { getCommands } from "$lib/store/commands";

  import { onMount } from "svelte";
  import { get } from "svelte/store";

  $: console.log($DATA[1]?.soil);

  const socketMessageHandlers = {
    grid: function (e) {
      const data = JSON.parse(e.data);

      console.log("Received grid message: ", data);

      switch (data.type) {
        case "grid.fullUpdate":
          DATA.set(hydrateData(data.grid));
          break;

        case "grid.plotUpdate":
          DATA.update((original) => {
            return original.map((plot) => {
              // Don't use array comparison here. [1,2] != [1,2] in JS
              if (
                plot.coords[0] == data.plot.grid_x &&
                plot.coords[1] == data.plot.grid_y
              ) {
                plot.plant = data.plot.plant;
                plot.soil = data.plot.soil;
                plot.commands = getCommands(plot);
              }
              return plot;
            });
          });
          break;

        case "server_error":
          console.error(data.message);
          break;

        default:
          console.error("Unexpected message type:", data.type);
          break;
      }
    },
    cursor: function (e) {
      const data = JSON.parse(e.data);

      console.log("Received cursor message: ", data);

      switch (data.type) {
        case "cursor.update":
          const { client, coords } = data;
          const thisCursor = get(otherCursors).find(
            (cur) => cur.client == client
          );
          if (thisCursor) {
            thisCursor.cursor.set(...coords);
          } else {
            otherCursors.update((original) => {
              return [...original, { client, cursor: new Cursor(...coords) }];
            });
          }
          break;

        case "cursor.connect":
          console.log("Connected with client name:", data.client);
          break;

        case "cursor.disconnect":
          console.log("Client", data.client, "disconnected");
          otherCursors.update((original) => {
            return original.filter((cur) => cur.client != data.client);
          });
          break;

        case "server_error":
          console.error(data.message);

        default:
          console.error("Unexpected message type:", data.type);
          break;
      }
    },
  };

  onMount(() => {
    Object.entries(sockets).forEach(([name, socket]) => {
      socket.connect((e) => {
        socket.onMessage(socketMessageHandlers[name]);
      });
    });
  });
</script>

{#if !$allSocketsConnected}
  <LoadingOverlay />
{/if}
