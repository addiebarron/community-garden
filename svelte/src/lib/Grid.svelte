<script>
  import { getContext, onMount } from "svelte";

  import GridItem from "./GridItem.svelte";
  import CursorBox from "./CursorBox.svelte";

  import { coordsToIndex, indexToCoords } from "$lib/util";
  import {
    // Settings
    GRID_X,
    GRID_Y,
    ZOOM_LEVEL,
    controlsMap,
    prefersReducedMotion,
    // Cursor
    Cursor,
    clientCursor,
    // Garden
    populateGarden,
    gardenData,
    addGlobalCommand,
    // Sockets
    sockets,
  } from "$lib/store";

  // Handlers are two-way bound with index.html
  export const gridSocketHandlers = {
    cursor: handleCursorSocketMessage,
    grid: handleGridSocketMessage,
  };

  // Bound elements
  let gridContainer, currentPlot;

  // Settings
  $: reduceMotion = $prefersReducedMotion;
  $: gridSize = 100 * $ZOOM_LEVEL;
  $: garden = $gardenData;

  // Cursors
  let otherCursors = [
    /* instantiate cursors on websocket events */
  ];

  // x and y are stores, subscribe with $x, $y
  let [x, y] = [clientCursor.x, clientCursor.y];
  // Run onCursorMove when the cursor's position changes
  $: if (garden.length) onCursorMove($x, $y);

  // Render cursor coordinates to the screen
  function onCursorMove(x, y) {
    let currentIndex = coordsToIndex(x, y);
    try {
      currentPlot = garden[currentIndex];
      let currentGridItem = currentPlot.element;

      garden.forEach((plot) => plot.element?.classList.remove("selected"));
      currentGridItem?.classList.add("selected");
      currentGridItem?.scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "center",
        inline: "center",
      });

      // Broadcast the cursor position update
      sockets.cursor.send(
        JSON.stringify({
          type: "cursor_update",
          coords: [x, y],
        })
      );
    } catch (err) {
      if (err instanceof TypeError) {
        void 0;
      } else {
        throw err;
      }
    }
  }

  function disableGridPointerEvents() {
    gridContainer.style.pointerEvents = "none";
  }
  function enableGridPointerEvents() {
    gridContainer.style.pointerEvents = "auto";
  }

  function handleGlobalKeyDown(e) {
    // Disable mouse hover effects when a key is pressed. Re-enable on mousemove/click
    disableGridPointerEvents();
    // Handle navigation keys
    if (Object.keys(controlsMap).includes(e.code)) {
      e.preventDefault();
      // Run the corresponding function to update the cursor
      clientCursor[controlsMap[e.code]]();
    }

    if (currentPlot && Object.keys(currentPlot.commands).includes(e.key)) {
      currentPlot.commands[e.key].run(currentPlot);
    }
  }

  function handlePlotMouseUp(e) {
    let index = e.target.dataset.index;
    clientCursor.setFromIndex(index);
  }

  function handleCursorSocketMessage(e) {
    const data = JSON.parse(e.data);

    if (data.type == "cursor_update") {
      const { client, coords } = data;
      const thisCursor = otherCursors.find((cur) => cur.client == client);
      // If the cursor already exists on the page, update its position
      if (thisCursor) {
        thisCursor.cursor.set(...coords);
        // Otherwise, add it to the list of cursors
      } else {
        otherCursors = [
          ...otherCursors,
          { client, cursor: new Cursor(...coords) },
        ];
      }
    } else if (data.type == "cursor_connected") {
      console.log("Connected with client name:", data.client);
    } else if (data.type == "cursor_disconnected") {
      console.log("Client", data.client, "disconnected");
      otherCursors = otherCursors.filter((cur) => cur.client != data.client);
    }
  }

  function handleGridSocketMessage(e) {
    const data = JSON.parse(e.data);
    if (data.type == "grid_populate") {
      gardenData.set(populateGarden(data.data));
    } else if (data.type == "grid_update") {
      gardenData.update((garden) => {
        return garden.map((p) => {
          if (p.coords[0] == data.grid_x && p.coords[1] == data.grid_y) {
            p.plant = data.plant;
          }
          return p;
        });
      });
    }
  }
</script>

<svelte:body
  on:keydown={handleGlobalKeyDown}
  on:mousemove={enableGridPointerEvents}
  on:mousedown={enableGridPointerEvents} />

<main>
  <div class="grid-container" bind:this={gridContainer}>
    <div
      class="grid"
      style="grid-template-columns: repeat({GRID_X}, {gridSize}px); grid-template-rows: repeat({GRID_Y}, {gridSize}px)"
    >
      {#each garden as { element, plant, acoord }, i}
        {#if i != 0}
          <GridItem
            bind:root={element}
            on:mouseup={handlePlotMouseUp}
            {i}
            {plant}
            {acoord}
          />
        {/if}
      {/each}
      {#each otherCursors as cur, i}
        <CursorBox {cur} {i} />
      {/each}
    </div>
  </div>
</main>

<style>
  main {
    grid-area: main;
    overflow: scroll;
    /* hide scrollbars */
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
    box-shadow: inset 0 0 0px 20px rgba(0, 0, 0, 0.1);
  }
  main::-webkit-scrollbar {
    display: none;
  }
  .grid {
    display: grid;
    position: relative;
  }
  .grid-container {
    width: 1000px;
    height: 1000px;
  }
</style>
