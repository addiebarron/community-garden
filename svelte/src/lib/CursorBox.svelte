<script>
  import { ZOOM_LEVEL } from "$lib/store/settings";

  export let client, cursor, i;

  let x = cursor.x,
    y = cursor.y;
  //const isUser = client == "user";

  // Color
  const hue = (i * 222) % 360;
  const color = `hsl(${hue}, 85%, 60%)`;

  // Size
  $: size = 100 * $ZOOM_LEVEL;
</script>

<div
  class="cursor-{client}"
  style="
    left: {size * ($x - 1) - 1}px;
    top: {size * ($y - 1) - 1}px; 
    width: {size + 2}px;
    height: {size + 2}px;
    box-shadow: inset 0 0 0 3px {color};
  "
>
  <span style="background-color: {color};">
    {client}
  </span>
</div>

<style>
  div {
    pointer-events: none;
    position: absolute;
    overflow: hidden;
  }
  div > span {
    position: absolute;
    top: 0;
    left: 0;
    color: white;
  }
</style>
