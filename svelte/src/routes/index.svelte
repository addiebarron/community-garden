<script>
  import LoadingOverlay from "$lib/LoadingOverlay.svelte";
  import Grid from "$lib/Grid.svelte";
  import Sidebar from "$lib/Sidebar.svelte";
  import Footer from "$lib/Footer.svelte";

  import { sockets, allSocketsConnected } from "$lib/store/sockets";

  import { onMount } from "svelte";

  let gridSocketHandlers;

  onMount(() => {
    Object.entries(sockets).forEach(([name, socket]) => {
      socket.connect((e) => {
        console.log("Socket connected:", socket._socket);
        socket.onMessage(gridSocketHandlers[name]);
      });
    });
  });
</script>

{#if !$allSocketsConnected}
  <LoadingOverlay />
{/if}
<Grid bind:gridSocketHandlers />
<Sidebar />
<Footer />
