// +page.js
export async function load({ fetch }) {
  const res = await fetch('http://localhost:8000/api/dishes/');
  const dishes = await res.json();
  return { dishes };
}
