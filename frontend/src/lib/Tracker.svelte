<script>
    import AnimatedCircularProgressBar from "./AnimatedCircularProgressBar.svelte";
    let { calorie_goal=0, calorie_intake = 0 ,protein_intake = 0, carb_intake = 0, fat_intake = 0 } = $props();

    let calories_left =$derived(calorie_goal - calorie_intake);
</script>

<!-- class="bg-stone-50 shadow-md rounded-lg p-6 flex flex-col space-y-4" -->
<div >

    <div class="content-start">
        
        <div class="mb-4 p-4">
            <!-- Logo + Title Row -->
            <div class="flex items-center space-x-2">
                <img src="flame_final.png" alt="Logo"class="w-6 h-6 object-contain -ml-2"/>
                <h2 class="font-bitter text-2xl font-normal">Calorie Goal:</h2>
                <input
                    type="number"
                    bind:value={calorie_goal}
                    class="border border-gray-300 rounded-lg px-2 py-1 w-24 text-center font-bitter text-xl font-medium"
                    placeholder="0"
                    min="0"
                />
             </div>    
            
        <h2 class="font-bitter ml-6 text-base text-gray-600" >You have <span class="text-amber-500">{calories_left<=0 ? 0 : calories_left}</span> KCal remaining </h2>
        

        </div>

    </div>
    <!-- Progress Bar -->
    <div class="flex flex-col items-center content-center">
        <AnimatedCircularProgressBar max={calorie_goal} value={calorie_intake} />
    </div>
</div>


