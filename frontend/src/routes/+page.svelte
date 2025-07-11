<script>
  import CategoryButtons from '$lib/CategoryButtons.svelte';
  import FoodList from '$lib/FoodList.svelte';
  import "../index.css";
  import "../app.css";

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

  function formatDateYYYYMMDD(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Month is 0-indexed
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  onMount(() => {
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  });
</script>

<main>
  <div class="border-0 flex items-center gap-30 mb-5">
    <h1 class="text-3xl font-bitter font-[600] p-5 ml-2">
      What's Cookin' for <strong class="text-red-800/70">{currentDate} at {currentTime}</strong> ?
    </h1>
    <p class="text-[17.5px] font-medium">
      Food Choices for: <span class="text-red-800/70">{selected}</span>
    </p>
  </div>

<CategoryButtons active={selected} setActive={(/** @type {string} */ val)=>selected=val}
/>

  <FoodList foods={data.dishes} selectedCategory={selected} currentDate={formattedCurrentDate} />
</main>
