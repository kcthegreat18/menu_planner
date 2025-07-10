<script>
  import CategoryButtons from '$lib/CategoryButtons.svelte';
  import FoodList from '$lib/FoodList.svelte';
  import "../index.css";
  import "../app.css";

  export let data;
  let selected = 'All Foods';
</script>

<main>
  <div class="border-0 flex items-center gap-30 mb-5">
    <h1 class="text-3xl font-bitter font-[600] p-5 ml-2">
      What's Cookin', Good Lookin'?
    </h1>
    <p class="text-[17.5px] font-medium">
      Food Choices for: <span class="text-red-800/70">{selected}</span>
    </p>
  </div>

<CategoryButtons active={selected} setActive={(/** @type {string} */ val)=>selected=val}
/>

  <FoodList foods={data.dishes} selectedCategory={selected} />
</main>
