$(document).ready(function() {
	const tags = ["Gluten Free", "Kosher", "Halal", "Vegetarian/Vegan", "Dairy Free"];
	var selectedTags = {};
	
	var displayTags = function() {
		$(".tags").empty();
		tags.forEach((tag, id) => {
			const selectedClass = selectedTags[id] ? "selected" : "";
			tagBtn = $("<button id='" + id + "' class='btn btn-light tag " + selectedClass + "' type='button'>" + tag + "</button>");
			$(".tags").append(tagBtn);
		});
	}

	$(".tags").on("click", ".tag", function(event) {
		const id = event.target.id
		if (selectedTags[id]) selectedTags[id] = null;
		else selectedTags[id] = tags[id];

		displayTags();
	});

	var display = function() {
		if (!jQuery.isEmptyObject(item)) {
			const image = $("<img src='" + item["image"] + "'>");
			$(".image").append(image);
			
			$("#form input[name='id']").val(item["id"]);
			$("#form input[name='image']").val(item["image"]);
			$("#form input[name='title']").val(item["title"]);
			$("#form input[name='location']").val(item["location"]);
			$("#form textarea[name='description']").val(item["description"]);
		}
		displayTags();
	}

	display();
});