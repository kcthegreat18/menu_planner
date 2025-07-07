<script>
  import CategoryButtons from '$lib/CategoryButtons.svelte';
  import "../index.css"
  import "../app.css"

  let selected = 'All Foods';
</script>

<main>
<div class="border-0 flex items-center gap-70">  <!-- 👈 Add flex and gap -->

  <h1 class="text-3xl font-bitter font-[600] p-5 ml-2">
    What's Cookin', Good Lookin'?
  </h1>

    <p class="text-[20px] font-medium mt-5">  <!-- 👈 p comes first in HTML order -->
    Food Choices for: <span class="text-red-800/70">{selected}</span>
  </p>
</div>

<CategoryButtons active={selected} setActive={(/** @type {string} */ value) => selected = value} />



</main>