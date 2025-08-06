<script>
// @ts-nocheck

  export let foods = [];
  export let selectedCategory = "";
  export let currentDate = "";

  export let search="";
  import Tracker from "./Tracker.svelte";
  import AnimatedCircularProgressBar from "./AnimatedCircularProgressBar.svelte";
  
  let chosen_foods= [];

  function sumCalories(foods) {
    let total=0;
    for (let i=0; i<foods.length; i++){
      total+=getCalories(foods[i]);
    }

    return total;
  }



  $: totalCalories = sumCalories(chosen_foods);

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

  function getCalories(food) {
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
<div class="flex flex-col lg:flex-row gap-4 mt-4 px-4">

  <!-- Left: Food Grid -->
  <div class="w-full lg:w-2/3">
    {#if filteredFoods.length === 0}
      <p class="text-gray-400 italic text-center">No dishes found for this category.</p>
    {:else}
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {#each filteredFoods as food}
          <button type="button" class="flex flex-col sm:flex-row bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-4 gap-4 w-full text-left"
            aria-label={`Select ${food.dish_name}`}
            on:click={() => {
              if (!chosen_foods.includes(food)){   
                if (food.dish_calories === 0) {
                  return;
                }
                else{
                chosen_foods=[...chosen_foods, food];
                }
              }
              else{
                chosen_foods = chosen_foods.filter(f => f !== food);
              }
}}
            on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { chosen_foods.push(food); } }}>
            
            <!-- Dish Image -->
            <img src={getMockImage(food)} alt={food.dish_name}
              class="w-full sm:w-24 sm:h-24 h-48 object-cover rounded-lg shadow-sm border" />

            <!-- Food Info -->
            <div class="flex flex-col flex-grow justify-between">
              <div>
                <h3 class="font-semibold text-lg">{food.dish_name}</h3>
                <p class="text-sm text-gray-500">{getCalories(food)} Kcal Per Serve</p>
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
          </button>
        {/each}
      </div>
    {/if}
  </div>
  
  <div class="w-full lg:w-1/3 flex flex-col border-0.5 border-gray-200 rounded-lg shadow-sm p-4 space-y-4">
    <div >
      <Tracker calorie_intake={totalCalories}/>

    </div>
    <div class="flex flex-col space-y-4">
      {#each chosen_foods as food}
      <div class="grid grid-cols-3 items-center justify-between p-2 border-b">
        <span class="font-semibold font-bitter">{food.dish_name}</span>
        <span class="text-gray-500 text-center font-bitter">{getCalories(food)} Kcal</span>
        <button class="text-amber-500 hover:text-amber-700 font-bitter" on:click={() => {
          chosen_foods = chosen_foods.filter(f => f !== food);
        }}>Remove</button>
      </div>

      {/each}
      {#if chosen_foods.length === 0}
        <p class="font-bitter ml-6 text-sm text-gray-400 text-center mr-12 mt-10"> Don't know your calories? Click <a class="text-amber-500"
          href="https://www.calculator.net/calorie-calculator.html"
          target="_blank">Here</a> and find out </p>
      {/if}
    </div>
  </div>
  
</div>
