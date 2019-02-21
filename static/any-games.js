
function showResults(json_record) {

  $('#app_name').html(json_record["app_name"]);
  $('#price').html(json_record["price"]);
  $('#genre').html(json_record["genre"]);
}


function searchGames() {

    let formInputs = {
        "country_type": $("#country_type_field").val(),
        "store_type": $("#store_type_field").val(),
        "app_id_type": $("#app_id_type_field").val()
    };


    $.post("/details_any_games", formInputs, showResults);
}



