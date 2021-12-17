<script>
  import GridItem from "$lib/GridItem.svelte";
  import CursorBox from "$lib/CursorBox.svelte";
  import ClientCursorBox from "$lib/ClientCursorBox.svelte";

  import { coordsToIndex } from "$lib/store/util";
  import { sockets } from "$lib/store/sockets";
  import { clientCursor, otherCursors } from "$lib/store/cursor";
  import { DATA } from "$lib/store/data";
  import {
    GRID_X,
    GRID_Y,
    ZOOM_LEVEL,
    controlsMap,
    prefersReducedMotion,
  } from "$lib/store/settings";

  let gridContainer, currentPlot;

  /* --- Settings --- */
  $: reduceMotion = $prefersReducedMotion;
  $: gridSize = 100 * $ZOOM_LEVEL;

  // x and y are store properties - destructure them into
  // variables to allow for reactive syntax ($x, $y)
  let [x, y] = [clientCursor.x, clientCursor.y];

  // Run onCursorMove when the cursor's position changes
  $: onCursorMove($x, $y);

  // Render cursor coordinates to the screen
  function onCursorMove(x, y) {
    let currentIndex = coordsToIndex(x, y);
    try {
      currentPlot = $DATA[currentIndex];
      let currentGridItem = currentPlot.element;
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
      if (!(err instanceof TypeError)) {
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
</script>

<svelte:body
  on:keydown={handleGlobalKeyDown}
  on:mousemove={enableGridPointerEvents}
  on:mousedown={enableGridPointerEvents} />

<main>
  <!-- Grid -->
  <div class="grid-container" bind:this={gridContainer}>
    <div
      class="grid"
      style="grid-template-columns: repeat({GRID_X}, {gridSize}px); grid-template-rows: repeat({GRID_Y}, {gridSize}px);"
    >
      {#each $DATA as plot, i}
        {#if i != 0}
          <GridItem
            bind:root={plot.element}
            on:mouseup={handlePlotMouseUp}
            {i}
            {plot}
          />
        {/if}
      {/each}
    </div>
  </div>

  <!-- Cursors -->
  {#each $otherCursors as cursor, i}
    <CursorBox cursor={cursor.cursor} client={cursor.client} {i} />
  {/each}
  <ClientCursorBox cursor={clientCursor} />
</main>

<style>
  main {
    position: relative;
    grid-area: main;
    overflow: scroll;
    /* hide scrollbars */
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
    box-shadow: inset 0 0 20px 5px rgba(0, 0, 0, 0.3);
    background-color: rgb(203, 255, 203);
  }
  /* main .overlay {
    position: sticky;
    top: 0%;
    left: 0%;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 2;
  } */
  main::-webkit-scrollbar {
    display: none;
  }
  .grid-container {
    position: relative;
  }
  .grid:after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    border: var(--edge-border);
  }
  .grid {
    display: grid;
    position: relative;
    width: fit-content;
    height: fit-content;
  }
</style>
