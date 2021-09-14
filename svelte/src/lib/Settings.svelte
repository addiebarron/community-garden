<script>
  import { ZOOM_LEVEL } from "$lib/store";

  let inputZoomLevel = 1;

  function setZoomLevel(n) {
    ZOOM_LEVEL.set(n);
  }
</script>

<input
  type="range"
  step="0.1"
  max="2"
  min="0.5"
  bind:value={inputZoomLevel}
  on:input={setZoomLevel(inputZoomLevel)}
/>
