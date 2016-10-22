$(document).ready(function() {

	$('#like-button').click(function() {
		var id = $(this).attr('data-category-id');
		$.get('/rango/like_category/', { category_id: id }, function(data) {
			$('#vote-count').html(data);
			$('#like-button').hide();
		});
	});
});