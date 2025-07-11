<script>

let {active="All Foods", setActive=(val)=>{}}=$props()

const categories= [
  {label:"All Foods", code:null},
  {label:"Chicken", code: "CH"},
  {label:"Pork", code: "PO"},
  {label:"Sea Food", code: "SF"},
  {label: "Vegetables", code: "VE"},
  {label: "Breakfast", code:"BF"},
  {label: "Snacks", code: "SN"},
  {label: "Fruits", code: "FR"}
]
</script>

<div class="flex gap-2 flex-wrap mt-4 border-1">
  {#each categories as category}
    <button class="px-3 py-1 rounded-full border-1 border-gray-300
    {active===category.label ? 'bg-red-800/70 text-white': 'bg-white text-black-700'}" onclick={()=>{setActive(category.label)}}>
      {category.label}
    </button>
  {/each}
</div>
