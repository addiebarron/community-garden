<script>
  import Settings from "./Settings.svelte";
  import { clientCursor, gardenData, logHistory } from "$lib/store";
  import { getContext, onMount } from "svelte";
  import { get } from "svelte/store";

  let plotnum = clientCursor.index;

  $: currentPlot = $gardenData[$plotnum];

  let logElement;
  $: $logHistory, scrollLogToBottom();
  function scrollLogToBottom() {
    logElement?.scrollTo({ top: 1000000 });
  }
</script>

<aside>
  <section id="commands">
    {#if currentPlot}
      <h2>
        {#if currentPlot.acoord}{currentPlot.acoord} - {/if}commands:
      </h2>
      {#if $plotnum != 0}
        <pre>Space: {"\t"}unselect</pre>
      {/if}
      {#each currentPlot.commands as command, i}
        <pre>{i}: {"\t"}{command.name}</pre>
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
  #commands pre {
    font-size: 16px;
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
