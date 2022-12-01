function addToList(food) {
  document.getElementById('overlay').style.display = 'block';
  document.getElementById('food-name').innerHTML = titleCase(food['description']);
  if (food['servingSize']) {
    document.getElementById('serving-size').innerHTML = food['servingSize'] + ' ' + food['servingSizeUnit'];
  } else {
    document.getElementById('serving-size').innerHTML = 1;
  }

  // Filling hidden fields
  document.getElementById('fdcId').value = food['fdcId']
  document.getElementById('food_name').value = food['description']
  if (food['servingSize']) { // Check if serving size is an attribute in the database
    document.getElementById('serving_size').value = food['servingSize']
    document.getElementById('serving_size_unit').value = food['servingSizeUnit']
  }
  for (let i = 0; i < food['foodNutrients'].length; i++) {
    // console.log(food['foodNutrients'][i]['nutrientName'] + ' ' + food['foodNutrients'][i]['value']);
    if (food['foodNutrients'][i]['nutrientName'] === 'Potassium, K') {
      document.getElementById('k_value').value = food['foodNutrients'][i]['value'];
    } 
    else if (food['foodNutrients'][i]['nutrientName'] === 'Sodium, Na') {
      document.getElementById('na_value').value = food['foodNutrients'][i]['value'];
    }
    else if (food['foodNutrients'][i]['nutrientName'] === 'Phosphorus, P') {
      document.getElementById('phos_value').value = food['foodNutrients'][i]['value'];
    }
    else if (food['foodNutrients'][i]['nutrientName'] === 'Protein') {
      document.getElementById('protein_value').value = food['foodNutrients'][i]['value'];
    }
    else if (food['foodNutrients'][i]['nutrientName'] === 'Total lipid (fat)') {
      document.getElementById('fat_value').value = food['foodNutrients'][i]['value'];
    }
    else if (food['foodNutrients'][i]['nutrientName'] === 'Carbohydrate, by difference') {
      document.getElementById('carbs_value').value = food['foodNutrients'][i]['value'];
    }
    else if (food['foodNutrients'][i]['nutrientName'] === 'Energy') {
      document.getElementById('calories').value = food['foodNutrients'][i]['value'];
    }
  };
  
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