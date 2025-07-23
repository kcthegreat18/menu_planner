<script>
  export let data;
</script>

<main class="p-4">
  <h1 class="text-2xl font-bold">{data.meal.dish_name}</h1>
  <p><strong>Type:</strong> {data.meal.dish_type}</p>
  <p><strong>Method:</strong> {data.meal.dish_method || 'N/A'}</p>
  <p><strong>Color:</strong> {data.meal.dish_color || 'N/A'}</p>
  <p><strong>Description:</strong> {data.meal.dish_description}</p>
</main>
