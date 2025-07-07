<script>
  import CategoryButtons from '$lib/CategoryButtons.svelte';
    import "../index.css"
  import "../app.css"

  let selected = '';
</script>

<main>
    <h1 class="text-3xl font-game ml-5">What's Cookin', Good Lookin'?</h1>


<CategoryButtons active={selected} setActive={(/** @type {string} */ value) => selected = value} />
        <p class="mt-5 text-left text-xl font-medium">
  Food Choices for: <span class="text-red-800/70">{selected}</span>
</p>



</main>