<script>
  import { ZOOM_LEVEL } from "$lib/store/settings";

  export let cursor;

  let { x, y } = cursor;
  let color = "white";

  $: size = 100 * $ZOOM_LEVEL;
</script>

<div
  class="cursor-client"
  style="
    left: {size * ($x - 1) + 1}px;
    top: {size * ($y - 1) + 1}px; 
    width: {size - 2}px;
    height: {size - 2}px;
    box-shadow: inset 0 0 10px 5px {color};
  "
/>

<style>
  div {
    pointer-events: none;
    position: absolute;
    overflow: hidden;
  }
</style>
