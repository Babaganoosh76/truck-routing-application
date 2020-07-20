function ajax(call_type, domain, obj, callback) {
	$.ajax({
		url: domain,
		type: call_type,
		data: JSON.stringify(obj),
		cache: false,
		dataType: 'json',
		contentType: 'application/json'
	}).done(function (data) {
		callback(data);
	}).fail(function (data) {
		console.log(data)
		console.error("Error reading file at '" + domain + "'.");
	});
}

function ajax_fd(form_data, callback=function(){}) {
	$.ajax({
		url: '/upload-dispatch',
		method: 'POST',
		data: form_data,
		cache: false,
		processData: false,
		contentType: false
	}).done(function(res) {
		callback(res);
	}).fail(function(res) {
		console.error("Error reading file at '" + domain + "'.");
	});
}