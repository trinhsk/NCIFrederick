$(document).ready(function() {

		const form = $("#form-wavelength");
		const panelHeadHm = $("#panelHeadHm");		
		form.on("submit", function(e)

				{
				e.preventDefault();
				$.ajax({
				url:"/updateHeatmap/",
				data:{wavelength:$("#wavelength_selector").find(":selected").text()},
				dataType:'json',
				success: function(reply) {
					panelHeadHm.text(`Heatmap of ${reply.pltcode} at ${reply.selected_wavelength}nm`);
					$('#innerPanel').html(reply.htmlHeatmap).fadeIn(500);
								}
					});
					return false;
				});
});
