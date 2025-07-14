<script>
  let { active = "All Foods", setActive = (val) => {} } = $props();

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

<!-- ✅ Responsive Category Buttons -->
<div class="flex flex-wrap gap-2 mt-4 px-2">
  {#each categories as category}
    <button
      class={`px-4 py-2 rounded-full border text-sm font-medium transition
        ${
          active === category.label
            ? 'bg-red-800/70 text-white border-red-800'
            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
        }`}
      on:click={() => setActive(category.label)}
    >
      {category.label}
    </button>
  {/each}
</div>
