<script>
  import { GRID_X, GRID_Y } from "$lib/store/settings";

  export let i, root, plot;

  let corners = {
    top: i <= GRID_X,
    right: i % GRID_X == 0,
    bottom: i > GRID_X * (GRID_Y - 1),
    left: i % GRID_X == 1,
  };

  function r(n) {
    return n * (Math.random() - 0.5);
  }

  // $: bg = plot.soil
  //   ? `hsl(8, 9%, ${60 - plot.soil.water_level / 3}%)`
  //   : `hsl(120, 50%, ${70}%)`;
</script>

<div
  bind:this={root}
  on:mouseup|preventDefault
  on:mousedown|preventDefault
  on:keydown|preventDefault
  class="grid-item grid-item-{i}"
  class:with-soil={!!plot.soil}
  class:grid-item-top={corners.top}
  class:grid-item-right={corners.right}
  class:grid-item-bottom={corners.bottom}
  class:grid-item-left={corners.left}
  data-index={i}
>
  <!-- {plot.acoord} -->
  {#if plot.soil}
    <span class="water">💧{plot.soil.water_level}%</span>
  {/if}
  {#if plot.plant}
    <span class="emoji">{plot.plant.species.emoji}</span>
    <span class="health">💖{plot.plant.health}%</span>
  {/if}
</div>

<style>
  :root {
    --edge-border: dashed 7px rgb(36, 36, 36);
  }
  .grid-item {
    position: relative;
    color: white;
    /* box-shadow: 0 0 0 1px black; */
    outline: solid 1px black;
  }
  .grid-item.with-soil {
    background-color: rgb(124, 98, 96);
  }
  .grid-item:hover {
    box-shadow: inset 0 0 0 10px rgba(255, 230, 0, 0.1);
  }
  .grid-item:focus,
  .grid-item.selected {
    box-shadow: inset 0 0 0 10px rgba(255, 230, 0, 0.35);
  }

  .grid-item * {
    pointer-events: none;
  }
  .grid-item span.water {
    display: block;
    position: absolute;
    bottom: 0;
    left: 2px;
  }
  .grid-item span.health {
    display: block;
    position: absolute;
    bottom: 1.1em;
    left: 2px;
  }
  .grid-item span.emoji {
    font-size: 2.5em;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  /* prettier-ignore */
  .grid-item.grid-item-top { border-top: var(--edge-border); } /* prettier-ignore */
  .grid-item.grid-item-right { border-right: var(--edge-border); } /* prettier-ignore */
  .grid-item.grid-item-bottom { border-bottom: var(--edge-border); } /* prettier-ignore */
  .grid-item.grid-item-left { border-left: var(--edge-border); }
</style>
