$(document).ready(function() {

	$("[data-action='like']").click(() => {
		$.ajax({
            type: "GET",
            url: `/item-like-toggle/${item["id"]}`,
            dataType: "json",
            success: function(result) {
                item = result["item"];
                display();
                console.log("data", item);
            },
            error: function(request, status, error) {
                console.log("Error");
                console.log(request);
                console.log(status);
                console.log(error);
            }
        });
	});

	$("[data-action='add-comment']").click(() => {
		const data = {
			id: item["id"],
			comment: $("input[name='new-comment']").val()
		};
        $("input[name='new-comment']").val("");

		$.ajax({
            type: "POST",
            url: "/item-comment",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            success: function(result) {
                item = result["item"];
                display();
                console.log("data", item);
            },
            error: function(request, status, error) {
                console.log("Error");
                console.log(request);
                console.log(status);
                console.log(error);
            }
        });
	});

	var displayComments = () => {
        $("[data='comments']").empty();

        item["comments"].forEach(entry => {
            const user = $(`<strong>${entry["user"]} </strong>`);
            const comment = $(`<span>${entry["comment"]}</span>`);

            var container = $("<div>");
            container.append(user);
            container.append(comment);
            $("[data='comments']").append(container);
        });
	}

	var displayButtonGroup = () => {
        $(".like-btn").empty();
        const likeBtn = item["likedByUser"] ? $("<i class='fas fa-heart pink'></i>") : $("<i class='far fa-heart'></i>");
        $(".like-btn").append(likeBtn);

        if (user !== item["user"]) {
        	$(".edit-btn").addClass("disabled");
			$(".delete-btn").addClass("disabled");
		}
	}

	var display = () => {
		$("[data='image']").attr("src", item["image"]);
		displayButtonGroup();
		const amt = item["likes"].length == 1 ? " like" : " likes";
		$("[data='likes']").html(item["likes"].length + amt);

        $("[data='title']").html(item["title"]);
		$("[data='location']").html(item["location"]);
		$("[data='date']").html(item["date"]);
        $("[data='user']").html(item["user"]);
		$("[data='description']").html(item["description"]);
		displayComments();

		$("[data-action='edit']").attr("href", `/item-edit/${item["id"]}`);
		$("[data-action='delete']").attr("href", `/item-delete/${item["id"]}`);
	}

	display();
});