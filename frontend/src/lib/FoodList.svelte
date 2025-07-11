<script>
// @ts-nocheck

  /**
   * @type {any[]}
   */
  export let foods=[];
  export let selectedCategory="";
  export let currentDate;


  const CATEGORY_MAP = {
    "Chicken": "CH",
    "Pork": "PO",
    "Sea Food": "SF",
    "Vegetables": "VE",
    "Breakfast": "BF",
    "Snacks": "SN",
    "Fruits": "FR",
  };

  $: filteredFoods= selectedCategory=== "All Foods" ? foods: foods.filter(food => food.dish_type===CATEGORY_MAP[selectedCategory]);



  // Mock calorie data
  function getMockCalories(food) {
    return food.dish_calories;
  }

  // Mock price data
  function getMockPrice(food) {
    switch (food.dish_type) {
      case "CH": return 120;
      case "PR": return 130;
      case "SF": return 150;
      case "VE": return 90;
      default: return 100;
    }
  }

  // Mock rating data
  function getMockRating(food) {
    switch (food.dish_type) {
      case "CH": return 4;
      case "PR": return 3;
      case "SF": return 5;
      case "VG": return 2;
      default: return 3;
    }
  }

  // Mock image URLs
function getMockImage(food) {
  return `/images/${food.dish_name}.jpg`;
}

</script>

<!-- Display List -->
<div class="flex flex-col gap-4 mt-4 max-h-[530px] overflow-y-auto pr-2 w-225 border-1">
  {#if filteredFoods.length === 0}
    <p class="text-gray-400 italic">No dishes found for this category.</p>
  {:else}
    {#each filteredFoods as food}
      <div class="flex items-center bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-4 gap-4 min-h-[120px] w-215">
        
        <!-- Dish Image -->
        <img src={getMockImage(food)} alt={food.dish_name}
          class="w-24 h-24 object-cover rounded-lg shadow-sm border" />

        <!-- Food Info -->
        <div class="flex-grow">
          <h3 class="font-semibold text-lg">{food.dish_name}</h3>
          <p class="text-sm text-gray-500">{getMockCalories(food)} Kcal Per Serve</p>
          <p class="text-sm text-gray-500">{food.dish_description}</p>
          
          <!-- Rating -->
          <div class="mt-1">
            {#each Array(5) as _, i}
              <span class={i < getMockRating(food) ? 'text-yellow-400' : 'text-gray-300'}>
                ★
              </span>
            {/each}
          </div>
        </div>

        <!-- Price -->
        <div class="text-right font-semibold text-lg text-gray-800 min-w-[60px]">
          Php {getMockPrice(food)}
        </div>
      </div>
    {/each}
  {/if}
</div>
