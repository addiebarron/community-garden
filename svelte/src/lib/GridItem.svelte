<script>
  import { GRID_X, GRID_Y } from "$lib/store/settings";

  export let i, root, plot;

  function randomColor() {
    let vals = [];
    for (let i = 0; i < 3; i++) {
      vals[i] = Math.floor(256 * Math.random());
    }
    vals[3] = (Math.random() / 10 + 0.2).toFixed(2);

    // return `rgba(${vals.join(",")})`;
    return;
  }

  let corners = {
    top: i <= GRID_X,
    right: i % GRID_X == 0,
    bottom: i > GRID_X * (GRID_Y - 1),
    left: i % GRID_X == 1,
  };

  let emojis = ["🌹", "🌺", "🌻", "🌼", "🌷", "🌱", "🌳", "🌵", "🌾", "🍀"];
</script>

<div
  bind:this={root}
  on:mouseup|preventDefault
  on:mousedown|preventDefault
  on:keydown|preventDefault
  class="grid-item grid-item-{i}"
  class:grid-item-top={corners.top}
  class:grid-item-right={corners.right}
  class:grid-item-bottom={corners.bottom}
  class:grid-item-left={corners.left}
  data-index={i}
  style="background-color: rgba(0,0,0,{Math.random() / 5});"
>
  {plot.acoord}
  {emojis[plot.plant]}
</div>

<style>
  .grid-item {
    --edge-border: dashed 5px rgb(36, 36, 36);
    /* center text */
    text-align: center;
    padding-top: 50%;
    line-height: 0;
    color: grey;
  }
  .grid-item:focus,
  .grid-item.selected {
    background-color: rgb(255, 255, 136) !important;
  }
  .grid-item:hover {
    border: solid 1px rgba(0, 0, 0, 0.3);
  }
  /* prettier-ignore */
  .grid-item.grid-item-top { border-top: var(--edge-border); } /* prettier-ignore */
  .grid-item.grid-item-right { border-right: var(--edge-border); } /* prettier-ignore */
  .grid-item.grid-item-bottom { border-bottom: var(--edge-border); } /* prettier-ignore */
  .grid-item.grid-item-left { border-left: var(--edge-border); }
</style>
