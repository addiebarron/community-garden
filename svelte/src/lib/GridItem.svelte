<script>
  export let i, root, plot;
</script>

<div
  bind:this={root}
  on:mouseup|preventDefault
  on:mousedown|preventDefault
  on:keydown|preventDefault
  class="grid-item grid-item-{i}"
  class:with-soil={!!plot.soil}
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
  div {
    position: relative;
    color: white;
  }
  div:after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
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
</style>
