let foodList = []

function addToList(food) {
  foodList.push(food);
  document.getElementById(food['fdcId']).innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/></svg>'
  document.getElementById('overlay').style.display = 'block';
  document.getElementById('food-name').innerHTML = titleCase(food['description']);
  document.getElementById('serving-size').innerHTML = food['servingSize'] + ' ' + food['servingSizeUnit']
}

function hidePopUp() {
  document.getElementById('overlay').style.display = 'none';
}

function getList() {
  return foodList
}

function titleCase(str) {
  str = str.toLowerCase().split(' ').map(function(word) {
    return (word.charAt(0).toUpperCase() + word.slice(1));
  });

 return str.join(' '); 
}