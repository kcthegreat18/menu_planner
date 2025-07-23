export async function load({ fetch }) {
  const res = await fetch('http://127.0.0.1:8000/dishes/');
  const data = await res.json();


  return {
    dishes:data
  };
}
