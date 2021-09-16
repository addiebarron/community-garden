<script>
  import Settings from "./Settings.svelte";
  import { currentPlot } from "$lib/store/data";
  import { logHistory } from "$lib/store/settings";
  import { allSocketsConnected } from "$lib/store/sockets";

  $: p = $currentPlot;

  let logElement;
  $: $logHistory, scrollLogToBottom();
  function scrollLogToBottom() {
    logElement?.scrollTo({ top: 1000000 });
  }
</script>

<aside>
  <section id="commands">
    {#if $currentPlot}
      <h2>
        {#if $currentPlot.acoord}<span class="acoord">{p.acoord}</span>
        {/if}commands
      </h2>
      <hr />
      {#if $currentPlot.index != 0}
        <p><code>Space</code>{"\t"}Unselect.</p>
      {/if}
      {#each $currentPlot.commands as command, i}
        <p><code>{i}</code>{"\t"}{command.description}</p>
      {/each}
    {/if}
  </section>
  <section id="chat"><Settings /></section>
  <section id="log" bind:this={logElement}>
    <h2>log</h2>
    {#each $logHistory as log}
      <pre>{log}</pre>
    {/each}
  </section>
</aside>

<style>
  aside {
    grid-area: aside;
    overflow: auto;
    display: grid;
    grid-template-areas:
      "commands"
      "chat"
      "log";
    grid-template-rows: 1fr 1fr 1fr;
  }
  aside section {
    padding: 10px;
  }
  #commands {
    grid-area: commands;
    background: rgb(255, 231, 235);
  }
  #commands code {
    padding: 2px;
    background: gainsboro;
    border: solid 1px lightgrey;
    border-radius: 3px;
  }
  #commands .acoord {
    padding: 5px 5px 3px 5px;
    background: white;
    border: solid 1px gainsboro;
  }
  #commands hr {
    border-top: solid 1px rgba(0, 0, 0, 0.2);
    border-bottom: 0;
  }
  #chat {
    grid-area: chat;
    background: rgb(255, 255, 231);
  }
  #log {
    overflow-y: scroll;
    grid-area: log;
    background: rgb(243, 231, 255);
  }
</style>
