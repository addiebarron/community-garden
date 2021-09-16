<script>
  import { GRID_X, GRID_Y } from "$lib/store/settings";

  export let i, root, plot;

  let corners = {
    top: i <= GRID_X,
    right: i % GRID_X == 0,
    bottom: i > GRID_X * (GRID_Y - 1),
    left: i % GRID_X == 1,
  };
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
  {/if}
</div>

<style>
  .grid-item {
    --edge-border: dashed 5px rgb(36, 36, 36);
    /* center text */
    text-align: center;
    padding-top: 50%;
    line-height: 0;
    position: relative;
    color: white;
    border: solid 0.5px rgb(68, 68, 68);
  }
  .grid-item:focus,
  .grid-item.selected {
    background-color: rgb(255, 255, 136) !important;
  }
  .grid-item:hover {
    border: solid 1px rgba(0, 0, 0, 0.3);
  }
  .grid-item.with-soil {
    background-color: rgb(139, 120, 117);
  }
  .grid-item span.water {
    display: block;
    position: absolute;
    bottom: 0.5em;
    left: 0;
  }
  .grid-item span.emoji {
    font-size: 20px;
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
