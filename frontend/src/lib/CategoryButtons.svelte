<script>
  export let active;
  export let setActive;

  const categories = [
    { name: 'Chicken', icon: '🍗' },
    { name: 'Pork', icon: '🥩' },
    { name: 'Sea Food', icon: '🐟' },
    { name: 'Vegetables', icon: '🥕' },
    { name: 'Breakfast', icon: '🍳'},
    { name: 'Snacks', icon: '🍉'}

  ];
</script>

<div class="flex gap-4 justify-center mt-10">
  {#each categories as category}
    <button
      on:click={() => setActive(category.name)}
      class={`flex flex-col items-center w-20 h-32 rounded-full shadow-md p-5 transition-colors duration-200
              ${active === category.name ? 'bg-red-800/70 text-black' : 'bg-white text-black'}`}
    >
      <div class="bg-white rounded-full w-12 h-12 flex items-center justify-center text-2xl">
        {category.icon}
      </div>
      <span class="mt-2 text-sm font-medium">{category.name}</span>
    </button>
  {/each}
</div>
