<!-- src/routes/+layout.svelte -->
<script>
  export let data;
  import "../index.css"
  
</script>



<div class="flex min-h-screen bg-gray-100 ">
  <!-- Sidebar -->
  <aside class="w-64 bg-red-900/80 shadow-xl/60 p-10">
    <div> <img src='UFS-Logo-Maroon.png' alt="UFS logo" class="h-40 w-96 object-scale-down"/> </div>
    <h1 class="text-2xl text-center mb-4 mt-2 font-sans-serif" >
        Hello, User</h1>
    <nav class="space-y-3 text-xl p-3">
      <a href="/" class="block text-black hover:underline">Meals for Today</a>
      <a href="/about" class="block text-black hover:underline">All Meals</a>
      <a href="/contact" class="block text-black hover:underline">Food FAQs</a>
    </nav>
  </aside>

  <!-- Page Content -->
  <main class="flex-1 p-8">
    <slot />
  </main>
</div>