<!-- src/routes/+layout.svelte -->
<script>
  export let data;
  import "../index.css"
  
</script>



<div class="flex min-h-screen bg-gray-100 ">
  <!-- Sidebar -->
  <aside class="w-64 bg-red-900/80 shadow-xl/60 p-10">
    <div> <img src='UFS-Logo-Maroon.png' alt="UFS logo" class="h-40 w-96 object-scale-down"/> </div>
    <h1 class="text-3xl text-center mb-1 mt-5 font-bitter" >
        Hello, User</h1>
    <h2 class="text-[17.5px] text-center  mb-10 font-bitter text-white">
        Welcome to the UFS Menu Planner!
    </h2>
    <nav class="space-y-3 text-xl p-3">
      <a href="/" class="block text-black hover:underline font-raleway">Meals for Today</a>
      <a href="meals_for_week" class="block text-black hover:underline font-raleway">Meals for the Week </a>
      <a href="/meals" class="block text-black hover:underline font-raleway">All Meals</a>
      <a href="/request" class="block text-black hover:underline font-raleway">Food FAQs</a>
    </nav>
  </aside>

  <!-- Page Content -->
  <main class="flex-1 p-8">
    <slot />
  </main>
</div>