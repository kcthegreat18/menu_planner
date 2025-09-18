export async function load({ fetch }) {
  const res = await fetch('http://127.0.0.1:8000/menu-dishes/');
  const data = await res.json();

  return {
    dishes: data.map((/** @type {{ dish: any; }} */ entry) => entry.dish) // unwrap nested "dish"
  };
}
