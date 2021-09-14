<script>
  import { currentInfo } from "$lib/store";
</script>

<footer>
  {$currentInfo};
</footer>

<style>
  footer {
    grid-area: foot;
    background: rgb(232, 244, 255);
  }
</style>
