function SearchTopGames(){
    const store = "android"
    $.get("https://api.appmonsta.com/v1/stores/%s/rankings.json" % store, showResults)
  }

function showResults(results) {
  $('#app_name').html(results.app_name);
  $('#avr_rating').html(results.avr.rating);
  $('#price').html(results.price);
  $('#country').html(results.country)
}
