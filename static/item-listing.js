$(document).ready(function() {

	var display = () => {
		$("#results").empty();
		$("#error-msg-container").empty();

		if (results.length === 0) 
			displayErrorMessage();
		else
			displaySearchResults();
	}

	var displayErrorMessage = () => {
		const errorMsg = $("<div class='error-msg'>Sorry, there were no results for your search.</div>");
		const listingBtn = $("<a href='/item-listing' class='btn btn-light'>Browse All Listings</a>");
		$("#error-msg-container").append(errorMsg);
		$("#error-msg-container").append(listingBtn);
	}

	function displaySearchResults() {
		var entries = [];
		Object.assign(entries, results).reverse();
		var count = 0;

		entries.forEach(item => {
			const itemDetails = $(`<a href="/item-details/${item["id"]}" class='item-details'>`);

			const image = $("<img src='" + item["image"] + "' class='card-img-top' />");		
			const title = $("<h5 class='card-title'>" + item["title"] + "</h5>");

			const date = new Date(item["createdTime"]);
			const formattedDate = date.toLocaleString("default", {
				"month": "short",
				"day": "numeric",
				"hour": "numeric",
				"minute": "numeric"
			});
			const description = $(`<span class='card-text text-muted'>${item["location"]} | ${formattedDate}</span>`);
			const likes = $(`<span><i class="fas fa-heart"></i> ${Object.keys(item["likes"]).length}</span>`);
			var info = $("<div class='card-info'>");
			info.append(description);
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

    display();
    console.log(results);

});