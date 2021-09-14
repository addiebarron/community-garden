<script>
  import Nav from "$lib/Nav.svelte";
  import Grid from "$lib/Grid.svelte";
  import Sidebar from "$lib/Sidebar.svelte";
  import Footer from "$lib/Footer.svelte";
</script>

<div id="app">
  <Nav />
  <slot />
</div>

<style>
  #app {
    display: grid;
    height: 100%;
    width: 100%;
    grid-template-areas:
      "nav nav"
      "main aside"
      "foot aside";
    grid-template-columns: 1fr 300px;
    grid-template-rows: 40px 5fr 1fr;
  }
</style>
