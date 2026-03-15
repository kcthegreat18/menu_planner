<script lang="ts">
  import CategoryButtons from '$lib/CategoryButtons.svelte';
  import FoodList from '$lib/FoodList.svelte';
  import "../../index.css";
  import "../../app.css";

  export let data;
  let selected = 'All Foods';

  import { onMount } from 'svelte';

  let currentDate = '';
  let currentTime = '';
  let formattedCurrentDate = '';

  function updateTime() {
    const now = new Date();

    currentDate = new Intl.DateTimeFormat('en-PH', {
      timeZone: 'Asia/Manila',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'long'
    }).format(now);

    currentTime = new Intl.DateTimeFormat('en-PH', {
      timeZone: 'Asia/Manila',
      hour: 'numeric',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    }).format(now);

    formattedCurrentDate = formatDateYYYYMMDD(now);
  }

  function formatDateYYYYMMDD(date:Date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  onMount(() => {
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  });
</script>

<main class="px-4 pb-8">
  <!-- ✅ Header Section -->
  <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-6">
    <div>
      <h1 class="text-2xl sm:text-3xl font-bitter font-semibold leading-snug">
        What's Cookin' for <br class="sm:hidden" />
        <strong class="text-red-800/70">{currentDate} at {currentTime}</strong>?
      </h1>
    </div>
    <p class="text-base sm:text-lg font-medium text-gray-700">
      Food Choices for: <span class="text-red-800/70">{selected}</span>
    </p>
  </div>

  <!-- ✅ Category Buttons -->
  <CategoryButtons
    active={selected}
    setActive={(val: string) => selected = val}
  />

  <!-- ✅ Food List -->
  <FoodList
    foods={data.dishes}
    selectedCategory={selected}
    currentDate={formattedCurrentDate}
  />
</main>
