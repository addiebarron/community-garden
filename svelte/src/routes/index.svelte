<script>
  import Overlay from "$lib/Overlay.svelte";
  import Grid from "$lib/Grid.svelte";
  import Sidebar from "$lib/Sidebar.svelte";
  import Footer from "$lib/Footer.svelte";

  import { sockets, allSocketsConnected } from "$lib/store.js";

  import { onMount } from "svelte";
  import { derived } from "svelte/store";

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
  <Overlay />
{/if}
<Grid bind:gridSocketHandlers />
<Sidebar />
<Footer />
