<script>
  import { Dessert } from "@lucide/svelte";

  let user_information = {
    name: "",
    studentNumber: "",
    upMail: ""
  };

  let dish_request_details = {
    dishName: "",
    dishType: "Chicken",
    dishDescription: ""
  };

  async function submitRequest() {
    const payload = {
      name: user_information.name,
      student_number: user_information.studentNumber,
      up_mail: user_information.upMail,
      dish_name: dish_request_details.dishName,
      dish_type: dish_request_details.dishType,
      dish_description: dish_request_details.dishDescription
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/requests/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        alert("🎉 Successfully submitted your dish request!");
        // Clear the form if needed
        user_information = { name: "", studentNumber: "", upMail: "" };
        dish_request_details = { dishName: "", dishType: "Chicken", dishDescription: "" };
      } else {
        const errorData = await response.json();
        console.error("Submission error:", errorData);
        alert("❌ Error submitting request. Check the console.");
      }

    } 
    catch (err) {
      console.error("Fetch error:", err);
      alert("❌ Network error.");
    }
  }
</script>


<main class="px-4 pb-8">

      <!-- ✅ Header Section -->
  <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-6">
    <div>
      <h1 class="text-2xl sm:text-3xl font-sharetech font-semibold leading-snug">
        Request a Meal <br class="sm:hidden" />
      </h1>
      <h2 class="text-l sm:text-2xl font-bitter leading-snug text-gray-700"> Want your favorite dish to be served in UFS? Request it now!</h2>
    </div>
  </div>

  <!--Div for all -->
    <div class="flex flex-col gap-10 mb-6">
       <!--Div for User Information Section -->
      <div class="w-full sm:w-3/4 bg-white rounded-lg shadow-sm p-4">
          <h2 class="text-lg sm:text-xl font-bitter text-red-800/70">
          User Information
          </h2>

          <!--Div for Name, Student Number -->
          <div class="flex flex-wrap sm:flex-row gap-4">

          <!--Name label and input -->
            <div class="flex flex-row sm:flex-row gap-2 mt-2">
              <label class="font-raleway" for="Name"> 
                Name:
              </label>
              <input class="border-grey-50 rounded-xs border-1" type="text" placeholder="" id="Name" bind:value={user_information.name}>
            </div>

            <!--Student Number label and input -->
            <div class="flex flex-row sm:flex-row gap-2 mt-2">
              <label class="font-raleway" for="Student Number"> 
                Student Number:
              </label>
              <input class="border-grey-50 rounded-xs border-1" type="text" placeholder="" id="Student Number" bind:value={user_information.studentNumber}>
            </div>

            <!--Student Email and input -->
            <div class="flex flex-row sm:flex-row gap-2 mt-2">
              <label class="font-raleway" for="UP Mail"> 
                UP Mail:
              </label>
              <input class="border-grey-50 rounded-xs border-1" type="email" placeholder="" id="UP Mail" bind:value={user_information.upMail}>
            </div>

          </div>

      </div>

      <!--Div for User Dish Section -->
          <div class="w-full sm:w-3/4 bg-white rounded-lg shadow-sm p-4">
            <h2 class="text-lg sm:text-xl font-bitter text-red-800/70">
            Dish Request Details
            </h2>

            <!--Div for Dish Name, Dish Type, Dish Description -->
            <div class="flex flex-col sm:flex-row gap-4">

            <!--Dish Name label and input -->
              <div class="flex flex-row sm:flex-row gap-2 mt-2">
                <label class="font-raleway" for="Dish Name"> 
                  Dish Name:
                </label>
                <input id="Dish Name" class="border-grey-50 rounded-xs border-1" type="text" placeholder="" bind:value={dish_request_details.dishName}>
              </div>

              <!--Dish Type label and input -->
              <div class="flex flex-row sm:flex-row gap-2 mt-2">
                <label class="font-raleway" for="Dish Type"> 
                  Dish Type:
                </label>
                <select id="Dish Type" class="border-grey-50 rounded-xs border-1" bind:value={dish_request_details.dishType}>
                  <option value="CH">Chicken</option>
                  <option value="PK">Pork</option>
                  <option value="SF">Sea Food</option>
                  <option value="VE">Vegetables</option>
                  <option value="BF">Breakfast</option>
                  <option value="SN">Snacks</option>
                  <option value="FR">Fruits</option>
                </select>
              </div>

              <!--Dish Description and input -->
              <div class="flex flex-row sm:flex-row gap-2 mt-2">
                <label class="font-raleway" for="Dish Description"> 
                  Dish Description:
                </label>
                <input class="border-grey-50 rounded-xs border-1" type="text" placeholder="" bind:value={dish_request_details.dishDescription}>
              </div>

            </div>

      </div>

<!-- ...other code... -->

  <!-- Center the button on small screens -->
  <div class="flex justify-center md:justify-between">
    <button
      class="flex w-xs px-4 py-2 rounded-full border text-sm font-raleway transition items-center justify-center bg-red-800/70 text-white border-red-800 hover:shadow-xs hover:-translate-y-1 hover:bg-red-800"
      on:click={()=>submitRequest()}
    >
      Submit Request
      <Dessert class="inline-block ml-2" size="20" />
    </button>
  </div>




    </div>

</main>