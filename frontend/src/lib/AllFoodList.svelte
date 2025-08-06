<script>
// @ts-nocheck

  export let foods = [];
  export let selectedCategory = "";
  export let currentDate = "";

  export let search="";
  import { goto } from '$app/navigation';
  import Tracker from './Tracker.svelte';
  const CATEGORY_MAP = {
    "Chicken": "CH",
    "Pork": "PO",
    "Sea Food": "SF",
    "Vegetables": "VE",
    "Breakfast": "BF",
    "Snacks": "SN",
    "Fruits": "FR",
  };

  $:filteredFoods=foods.filter(food=>{
    const correctCategory= selectedCategory==="All Foods" || food.dish_type===CATEGORY_MAP[selectedCategory];

    const correctSearch= search==="" || food.dish_name.toLowerCase().includes(search.toLowerCase());

    return correctCategory && correctSearch;
  })

  function lowerAll(string){
    let str=""
    for (let i=0; i<string.length; i++){
      if (i===0){
        str+=string[i]
      }
      else{
        str+=string[i].toLowerCase()
      }
    }
      return str;
  }

  function getMockCalories(food) {
    return food.dish_calories;
  }

  function getMockPrice(food) {
    switch (food.dish_type) {
      case "CH": return 120;
      case "PR": return 130;
      case "SF": return 150;
      case "VE": return 90;
      default: return 100;
    }
  }

  function getMockRating(food) {
    switch (food.dish_type) {
      case "CH": return 4;
      case "PR": return 3;
      case "SF": return 5;
      case "VE": return 2;
      default: return 3;
    }
  }

  function getMockImage(food) {
    return `/images/${food.dish_name}.jpg`;
  }
</script>

<!-- ✅ Flex-based Responsive Layout -->
<div class="flex flex-col lg:flex-row gap-4 mt-4 px-4 ">

  <!-- Left: Food Grid -->
  <div class="w-full lg:w-2/3">
    {#if filteredFoods.length === 0}
      <p class="text-gray-400 italic text-center">No dishes found for this category.</p>
    {:else}
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {#each filteredFoods as food}
          <div class="flex flex-col sm:flex-row bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-4 gap-4"
           on:click={() => goto(`/meals/${food.id}`)} >
            
            <!-- Dish Image -->
            <img src={getMockImage(food)} alt={food.dish_name}
              class="w-full sm:w-24 sm:h-24 h-48 object-cover rounded-lg shadow-sm border" />

            <!-- Food Info -->
            <div class="flex flex-col flex-grow justify-between">
              <div>
                <h3 class="font-semibold text-lg">{food.dish_name}</h3>
                <p class="text-sm text-gray-500">{getMockCalories(food)} Kcal Per Serve</p>
                <p class="text-sm text-gray-500">{food.dish_description}</p>
              </div>

              <!-- Rating & Price -->
              <div class="mt-2 flex justify-between items-center">
                <div>
                  <p class="text-sm text-gray-500">{lowerAll(food.dish_method)}</p>
                </div>
                <div class="font-semibold text-gray-800 text-sm sm:text-lg">
                  Php {getMockPrice(food)}
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>


</div>
