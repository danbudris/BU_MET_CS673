
function showDialog(actionUrl){
	$.ajax({
		type: "GET",
        url: actionUrl,
        success: function(result) {
        	$("#dialogModal").html(result);
            $("#dialogModal").modal({
                backdrop: false,
                show: true
            });
        },
        async:true
    }); 
}

// close Story Dialog and erase the content
function closeDialog(){
	$("#dialogModal").modal('hide');
    $("#dialogModal").html('');
}

function getStoryPointHtml(point) {
	var pointhtml = '';
	if (point <= 0) {
		pointhtml = '<i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i>';
	} else {
		for (var i = 0; i < point; i++) {
			pointhtml += '<i class="fa fa-star fw"></i>';
		}
		for (var i = 5; i > point; i--) {
			pointhtml += '<i class="fa fa-star-o fw"></i>';
		}
	}
	return pointhtml;
}

function loadIterationList(projectID, iterationID) {
	var listUrl = "/req/iterations/" + projectID;
	var listID = "#proj_" + projectID + "_iters";
	if (iterationID != null) {
		listUrl = "/req/iterationswithselection/" + projectID + "/" + iterationID;
	};
	$.ajax({
		type: "GET",
		cache: false,
		url: listUrl,
		success: function(result) {
			$(listID).html(result);
		},
		async: true
	});
}

function loadUsersInProject(projectID) {
	var taskUrl = "/req/usersinproject/" + projectID;
	var jquerySearchID = "#userlist_" + projectID;
	$.ajax({
		url: taskUrl,
		success: function(result) {
			$(jquerySearchID).html(result);
		},
		async: true
	});
}

function loadTasks(storyID) {
	var taskUrl = "/req/tasks/" + storyID;
	var jquerySearchID = "#task_" + storyID;
	$.ajax({
		url: taskUrl,
		success: function(result) {
			$(jquerySearchID).html(result);
		},
		async: true
	});
}

function addTaskIntoList(storyID) {
	var addTaskUrl = "/req/addtaskintolist/" + storyID;
	var formID = "#newtask_form_" + storyID;
	var listID = "#task_" + storyID
	$.ajax({
        type : "POST",
        cache : false,
        url : addTaskUrl,
        data : $(formID).serialize(),
        success : function(data) {
            $(listID).html(data);
        },
        async: true
	});
}

function showEditTaskInList(storyID, taskID) {
	var showEditTaskUrl = "/req/edittaskinlist/" + storyID + "/" + taskID;
	var listID = "#task_" + storyID;
	$.ajax({
		type: "GET",
		cache: false,
		url: showEditTaskUrl,
		success: function(data) {
			$(listID).html(data);
		},
		async: true
	});
}

function saveEditTaskInList(storyID, taskID) {
	var showEditTaskUrl = "/req/edittaskinlist/" + storyID + "/" + taskID;
	var formID = "#edittask_form_" + storyID;
	var listID = "#task_" + storyID;
	$.ajax({
		type: "POST",
		cache: false,
		url: showEditTaskUrl,
		data: $(formID).serialize(),
		success: function(data) {
			loadTasks(storyID);
		},
		async: true
	});
}

function removeTaskFromList(storyID, taskID) {
	var removeTaskUrl = "/req/removetaskfromlist/" + storyID + "/" + taskID;
	var formID = "#removetask_form_" + storyID;
	var listID = "#task_" + storyID;
	$.ajax({
		type: "POST",
		cache: false,
		url: removeTaskUrl,
		data: $(formID).serialize(),
		success: function(data) {
			$(listID).html(data);
		},
		async: true
	});
}

function loadComments(storyID) {
	var commentUrl = "/req/comments/" + storyID;
	var jquerySearchID = "#comment_" + storyID;
	$.ajax({
		url: commentUrl,
		success: function(result) {
			$(jquerySearchID).html(result);
		},
		async: true
	});
}


function addCommentIntoList(storyID) {
	var addCommentUrl = "/req/addcommentintolist/" + storyID;
	var formID = "#newcomment_form_" + storyID;
	var listID = "#comment_" + storyID
	$.ajax({
        type : "POST",
        cache : false,
        url : addCommentUrl,
        data : $(formID).serialize(),
        success : function(data) {
            $(listID).html(data);
        },
        async:true
	});
}

function showEditCommentInList(storyID, commentID) {
	var showEditCommentUrl = "/req/editcommentinlist/" + storyID + "/" + commentID;
	var listID = "#comment_" + storyID;
	$.ajax({
		type: "GET",
		cache: false,
		url: showEditCommentUrl,
		success: function(data) {
			$(listID).html(data);
		},
		async: true
	});
}

function saveEditCommentInList(storyID, commentID) {
	var showEditCommentUrl = "/req/editcommentinlist/" + storyID + "/" + commentID;
	var formID = "#editcomment_form_" + storyID;
	var listID = "#comment_" + storyID;
	$.ajax({
		type: "POST",
		cache: false,
		url: showEditCommentUrl,
		data: $(formID).serialize(),
		success: function(data) {
			loadComments(storyID);
		},
		async: true
	});
}

function removeCommentFromList(storyID, commentID) {
	var removeCommentUrl = "/req/removecommentfromlist/" + storyID + "/" + commentID;
	var formID = "#removecomment_form_" + storyID;
	var listID = "#comment_" + storyID;
	$.ajax({
		type: "POST",
		cache: false,
		url: removeCommentUrl,
		data: $(formID).serialize(),
		success: function(data) {
			$(listID).html(data);
		},
		async: true
	});
}

