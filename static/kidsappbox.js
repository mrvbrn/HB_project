function showResults(json_android) {

  $('#avg_rating').html(json_record["avg_rating"]);
  $('#downloads').html(json_record["downloads"]);
  $('#histogram').html(json_record["all_histogram"]);
}


function searchAndroid() {

    let formInputs = {
        "country_type": $("#country_type_field").val(),
        store : "android"
        app_id : "appId"
    };


    $.post("/employees/<int:employee_id>/kidsappbox_game", formInputs, showResults);
}





function showResult(json_itunes) {

  $('#avg_ratings').html(json_record["avg_rating"]);
  $('#reviews').html(json_record["all_reviews"]);
  $('#histograms').html(json_record["all_histogram"]);
}


function searchiTunes() {

    let formInput = {
        "country_type": $("#country_type_field").val(),
        "store_type": "itunes",
        "app_id_type": "appId"
    };


    $.post("/employees/<int:employee_id>/kidsappbox_game", formInput, showResult);
}
