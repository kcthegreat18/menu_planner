<script>
// @ts-nocheck

  /**
   * @type {any[]}
   */
  export let foods = [];
  export let selectedCategory = "All Foods";

const CATEGORY_MAP = {
  "Chicken": "CH",
  "Pork": "PO",
  "Sea Food": "SF",
  "Vegetables": "VE",
  "Breakfast": "BF",
  "Snacks": "SN",
  "Fruits": "FR",
};


$: filteredFoods = selectedCategory === "All Foods"
  ? foods
  : foods.filter(food => food.dish_type === CATEGORY_MAP[selectedCategory]);


  // Mock calorie data
  function getMockCalories(food) {
    switch (food.dish_type) {
      case "CH": return 99;
      case "PR": return 100;
      case "SF": return 98;
      case "VE": return 79;
      default: return 85;
    }
  }

  // Mock price data
  function getMockPrice(food) {
    switch (food.dish_type) {
      case "CHK": return 120;
      case "PRK": return 130;
      case "SEA": return 150;
      case "VEG": return 90;
      default: return 100;
    }
  }

  // Mock rating data
  function getMockRating(food) {
    switch (food.dish_type) {
      case "CHK": return 4;
      case "PRK": return 3;
      case "SEA": return 5;
      case "VEG": return 2;
      default: return 3;
    }
  }

  // Mock image URLs
  function getMockImage(food) {
    switch (food.dish_type) {
      case "CHK": return "https://source.unsplash.com/featured/?grilled,chicken";
      case "PRK": return "https://source.unsplash.com/featured/?pork";
      case "SEA": return "https://source.unsplash.com/featured/?seafood";
      case "VEG": return "https://source.unsplash.com/featured/?vegetables";
      default: return "https://source.unsplash.com/featured/?food";
    }
  }
</script>

<!-- Display List -->
<div class="flex flex-col gap-4 mt-4 max-h-[400px] overflow-y-auto pr-2 w-225">
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
