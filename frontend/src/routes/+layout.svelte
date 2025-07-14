<!-- src/routes/+layout.svelte -->
<script>
  import "../index.css";
</script>

<div class="flex flex-col lg:flex-row min-h-screen bg-gray-100">
  <!-- ✅ Sidebar -->
  <aside class="w-full lg:w-64 bg-red-900/80 shadow-lg p-6 lg:p-10">
    <div class="flex justify-center lg:justify-start">
      <img
        src="UFS-Logo-Maroon.png"
        alt="UFS logo"
        class="h-32 w-auto object-contain"
      />
    </div>

    <h1 class="text-2xl lg:text-3xl text-center lg:text-left mt-4 font-bitter text-white">
      Hello, User
    </h1>

    <h2 class="text-[16px] lg:text-[17.5px] text-center lg:text-left mt-2 mb-6 font-bitter text-white">
      Welcome to the UFS Menu Planner!
    </h2>

    <nav class="space-y-2 text-lg p-2 text-center lg:text-left">
      <a href="/" class="block text-white hover:underline font-raleway">Meals for Today</a>
      <a href="/meals" class="block text-white hover:underline font-raleway">All Meals</a>
      <a href="/request" class="block text-white hover:underline font-raleway">Food FAQs</a>
    </nav>
  </aside>

  <!-- ✅ Page Content -->
  <main class="flex-1 p-4 sm:p-6 lg:p-8">
    <slot />
  </main>
</div>
