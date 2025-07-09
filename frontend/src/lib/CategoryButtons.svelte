<script>
  export let active = 'All Foods';
  export let setActive = (val) => {};

  const categories = [
    { label: "All Foods", code: null },
    { label: "Chicken", code: "CH" },
    { label: "Pork", code: "PO" },
    { label: "Sea Food", code: "SF" },
    { label: "Vegetables", code: "VE" },
    { label: "Breakfast", code: "BF" },
    { label: "Snacks", code: "SN" },
    { label: "Fruits", code: "FR" }
  ];
</script>

<div class="flex gap-2 flex-wrap mt-4">
  {#each categories as cat}
    <button
      class="px-3 py-1 rounded-full border border-gray-300 text-sm transition-all
        {active === cat.label ? 'bg-red-600 text-white' : 'bg-white text-gray-700'}"
      on:click={() => setActive(cat.label)}
    >
      {cat.label}
    </button>
  {/each}
</div>
