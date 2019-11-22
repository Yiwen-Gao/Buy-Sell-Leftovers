$(document).ready(function() {

	function displaySearchResults() {
		$("#results").empty();

		var entries = [];
		Object.assign(entries, results).reverse();
		var count = 0;

		entries.forEach(item => {
			const itemDetails = $(`<a href="/item-details/${item["id"]}" class='item-details'>`);

			const image = $("<img src='" + item["image"] + "' class='card-img-top' />");		
			const title = $("<h5 class='card-title'>" + item["title"] + "</h5>");

			const locationDate = $(`<span class='card-text text-muted'>${item["location"]} | ${item["date"]}</span>`);
			const likes = $(`<span><i class="fas fa-heart"></i> ${item["likes"].length}</span>`);
			var info = $("<div class='card-info'>");
			info.append(locationDate);
			info.append(likes);

			var body = $("<div class='card-body'>");
			body.append(title);
			body.append(info);

			var card = $("<div class='card result-card'>");
			card.append(itemDetails);
			card.append(image);
			card.append(body);

			const cols = $("#listing").children();
			cols.eq(count++ % cols.length).append(card);
		});
		
	}

    displaySearchResults();
    console.log(results);

});