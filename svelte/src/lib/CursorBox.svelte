<script>
  import { ZOOM_LEVEL } from "$lib/store";

  export let cur, i;

  const { client, cursor } = cur;
  let x = cursor.x,
    y = cursor.y;

  const hue = (i * 222) % 360;
  const color = `hsl(${hue}, 100%, 50%)`;

  $: size = 100 * $ZOOM_LEVEL;
</script>

<div
  class="cursor-{client}"
  style="
    top: {size * ($y - 1) - 1}px; 
    left: {size * ($x - 1) - 1}px;
    width: {size}px;
    height: {size}px;
    border-color: {color};
  "
>
  <span style="background-color: {color};">
    {client}
  </span>
</div>

<style>
  [class^="cursor-"] {
    pointer-events: none;
    position: absolute;
    border: solid 1px;
    overflow: hidden;
  }
  [class^="cursor-"] span {
    position: absolute;
    top: 0;
    left: 0;
    color: white;
  }
</style>
