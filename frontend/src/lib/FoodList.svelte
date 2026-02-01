<script>
// @ts-nocheck

  const API_BASE = "http://127.0.0.1:8000";

  export let foods = [];
  export let selectedCategory = "";
  export let currentDate = "";

  export let search="";
  import Tracker from "./Tracker.svelte";
  import AnimatedCircularProgressBar from "./AnimatedCircularProgressBar.svelte";
  
  let chosen_foods= [];

  let liked_foods= new Set();
  let disliked_foods= new Set();


  function likeFood(food) {
    if (!liked_foods.has(food)){
      if (disliked_foods.has(food)){
        disliked_foods.delete(food);
      }
      liked_foods.add(food);
    }
    else{
      liked_foods.delete(food);
    }

    liked_foods = new Set(liked_foods);
    
  }

  function dislikeFood(food) {
    if (!disliked_foods.has(food)) {
      if (liked_foods.has(food)){
        liked_foods.delete(food);
      }
      disliked_foods.add(food);
    }
    else{
      disliked_foods.delete(food);
    }
  

    disliked_foods = new Set(disliked_foods);
    
  
  }

    function foodStatus(food) {
    if (liked_foods.has(food)) return "liked";
    if (disliked_foods.has(food)) return "disliked";
    return "neutral";
  }
  

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


  async function reactIncrement(dishId, reaction) {
    const res = await fetch(`${API_BASE}/dish/react-increment/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dish_id: dishId, reaction }), // reaction: "like"|"dislike"
    });

    if (!res.ok) {
      throw new Error(await res.text());
    }

    return await res.json();
  }


  //For the popup

  let popup_message="";
  let show_Popup=false;
  let popupTimer;

  function triggerPopup(message){
    popup_message=message;
    show_Popup=true;

    clearTimeout(popupTimer)
    popupTimer=setTimeout(() => {
      show_Popup=false;
    }, 1500)
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

          <div type="button" class="flex flex-col sm:flex-row bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-4 gap-4 w-full text-left"
            aria-label={`Select ${food.dish_name}`}
            role="button"
            tabindex="0"
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
                <div class="flex items-center justify-between">
                  <h3 class="font-semibold text-lg">{food.dish_name}</h3>
                  <div class="font-semibold text-gray-800 text-sm sm:text-lg">
                  Php {getMockPrice(food)}
                  </div>
                </div>
                <p class="text-sm text-gray-500">{getCalories(food)} Kcal Per Serve</p>
                <p class="text-sm text-gray-500">{food.dish_description}</p>
              </div>

              <!-- Rating & Price -->
              <div class="mt-2 flex justify-between items-center">
                <div>
                  <p class="text-sm text-gray-500">{lowerAll(food.dish_method)}</p>
                </div>

                <div class="flex items-center space-x-4">
                  <button 
                    aria-label="Like this dish"
                    on:click|stopPropagation={async () => {
                      const wasLiked = liked_foods.has(food);     // BEFORE
                      likeFood(food);                             // toggle local UI
                      triggerPopup(`You liked ${food.dish_name}`);
                      const isLiked = liked_foods.has(food);      // AFTER

                      // ✅ Only increment when it turns ON
                      if (!wasLiked && isLiked) {
                        try {
                          await reactIncrement(food.id, "like");
                        } catch (e) {
                          console.error(e);
                          // optional rollback to keep UI consistent
                          likeFood(food);
                          
                        }
                      }

                      console.log("liked_foods:", [...liked_foods].map(f => f.dish_name));
                      console.log("disliked foods:", [...disliked_foods].map(f => f.dish_name));
                    }}
                    class="hover:text-green-600 {liked_foods.has(food) && !disliked_foods.has(food) ? 'text-green-600' :'text-black'}"
                  >
                    <i class="{liked_foods.has(food) && !disliked_foods.has(food) ? 'fa-solid' : 'fa-regular'} fa-thumbs-up fa-lg"></i>
                  </button>

                  <button 
                    aria-label="Dislike this dish"
                    on:click|stopPropagation={async () => {
                      const wasDisliked = disliked_foods.has(food);  // BEFORE
                      dislikeFood(food);                             // toggle local UI
                      triggerPopup(`You disliked ${food.dish_name}`);
                      const isDisliked = disliked_foods.has(food);   // AFTER

                      // ✅ Only increment when it turns ON
                      if (!wasDisliked && isDisliked) {
                        try {
                          await reactIncrement(food.id, "dislike");
                        } catch (e) {
                          console.error(e);
                          // optional rollback
                          dislikeFood(food);
                          
                        }
                      }

                      console.log("liked_foods:", [...liked_foods].map(f => f.dish_name));
                      console.log("disliked foods:", [...disliked_foods].map(f => f.dish_name));
                    }}
                    class="hover:text-red-700/80 {disliked_foods.has(food) && !liked_foods.has(food) ? 'text-red-700/80' :'text-black'}"
                  >
                    <i class="{disliked_foods.has(food) && !liked_foods.has(food) ? 'fa-solid' : 'fa-regular'} fa-thumbs-down fa-lg"></i>
                  </button>

                </div>

              </div>
            </div>
          </div>
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

  {#if show_Popup==true}
  <div class="fixed bottom-6 right-6 bg-black text-white px-4 py-2 rounded-lg shadow-lg transition-opacity">
    {popup_message}
  </div>
{/if}
  
</div>
