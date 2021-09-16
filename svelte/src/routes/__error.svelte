<script context="module">
  export function load({ error, status }) {
    return {
      props: {
        error,
        status,
      },
    };
  }
</script>

<script>
  import { DEV } from "$lib/store/settings";
  export let error, status;
</script>

<div>
  <h1>{status}</h1>
  <h2>{error.message}</h2>
  <p>{error.stack}</p>
</div>

<style>
  div {
    position: fixed;
    top: 50vh;
    left: 50vw;
    transform: translate(-50%, -50%);
    width: 50vw;
    height: 50vh;
    min-width: 500px;
    min-height: 400px;
    border: solid 1px grey;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.3);
  }
</style>
