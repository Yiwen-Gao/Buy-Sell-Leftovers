$(document).ready(function() {

    window.onscroll = () => {
        if (window.pageYOffset > $("[data-role='navbar']").height()) {
            $("#back-btn").removeClass("normal-back-btn");
            $("#back-btn").addClass("sticky-back-btn");
        }
        else {
            $("#back-btn").removeClass("sticky-back-btn");
            $("#back-btn").addClass("normal-back-btn");            
        }
    };

	$("[data-action='like']").click(() => {
		if (user in item["likes"])
            return;

        $.ajax({
            type: "GET",
            url: `/item-like/${item["id"]}`,
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

    var submitComment = () => {
        const data = {
            id: item["id"],
            comment: $("input[name='new-comment']").val()
        };
        $("input[name='new-comment']").val("");
        console.log(data)

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
    };

    $("input[name='new-comment']").keydown((event) => {
        if (event.key === "Enter")
            submitComment();
    });

    $("[data-action='comment']").click(submitComment);

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
	};

	var displayButtonGroup = () => {
        $(".like-btn").empty();
        const likeBtn = user in item["likes"] ? $("<i class='fas fa-heart pink'></i>") : $("<i class='far fa-heart'></i>");
        $(".like-btn").append(likeBtn);

        if (user !== item["user"]) {
        	$(".edit-btn").addClass("disabled");
			$(".delete-btn").addClass("disabled");
		}
	};

	var display = () => {
		$("[data='image']").attr("src", item["image"]);
		displayButtonGroup();

        const num = Object.keys(item["likes"]).length;
		const amt = num == 1 ? " like" : " likes";
		$("[data='likes']").html(num + amt);

        $("[data='title']").html(item["title"]);
		$("[data='location']").html(`<i class="fas fa-map-marker-alt"></i>${item["location"]}`);
        const date = new Date(item["createdTime"]);
        const formattedDate = date.toLocaleString("default", {
            "month": "short",
            "day": "numeric",
            "hour": "numeric",
            "minute": "numeric"
        });
		$("[data='date']").html(`<i class="fas fa-calendar"></i>${formattedDate}`);
        $("[data='user']").html(item["user"]);
		$("[data='description']").html(item["description"]);
		$("input[name='new-comment']").attr("placeholder", `Leave a question, comment, or concern for @${item["user"]}...`);
        displayComments();

		$("[data-action='edit']").attr("href", `/item-edit/${item["id"]}`);
		$("[data-action='delete']").attr("href", `/item-delete/${item["id"]}`);
	};

	display();
});