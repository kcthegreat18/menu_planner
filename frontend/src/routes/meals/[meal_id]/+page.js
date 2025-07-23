export async function load({fetch, params}){
    const res= await fetch(`http://127.0.0.1:8000/dishes/${params.meal_id}/`);
    const data = await res.json();

    return {meal:data};
}