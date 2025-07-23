<script>
  // @ts-nocheck
  import CategoryButtons from '$lib/CategoryButtons.svelte';
  import AllFoodList from '$lib/AllFoodList.svelte';
  import FoodList from '$lib/FoodList.svelte';
  import "../../index.css";
  import "../../app.css";

  export let data;

  console.log('✅ Loaded dishes:', data);
  let selected = 'All Foods';

  let search="";

</script>


<main class="px-4 pb-8">
  <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-6">
    <div>
      <h1 class="text-2xl sm:text-3xl font-bitter font-semibold leading-snug">
        All Meals

    </div>


    <input class="px-2.5 py-2 rounded-full border-1 text-sm font-medium border-gray-300 text-gray-700"  
    placeholder="Search for a Dish"
    bind:value={search} />


  </div>



  <div>
    <CategoryButtons
    active={selected}
    setActive={(val)=>{selected=val }}
    />

    <AllFoodList
    foods={data.dishes}
    selectedCategory={selected}
    search={search} 
  />


  </div>
</main>