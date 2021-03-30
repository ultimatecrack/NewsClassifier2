function submit_review() {
	review = $('#review').val();

	if (review == ''){
		$('#message').text('Please fill the review!');
		$('#message_parent').show();
		return false;
	}

	var jsonObjects = {'sentence':review};

	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url: '/predict',
		dataType : 'json',
		data : JSON.stringify(jsonObjects),
		success : function(result) {
			console.log(result);
			$('#message').text(result);
			$('#message_parent').show();
		},error : function(result){
		   console.log(result);
		}
	});
}