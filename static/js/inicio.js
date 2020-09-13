
function init() {
	var notifOptions ={position:"bottom left", className: "success", autoHideDelay: 3000, arrowShow: true};
	var sNotifMsg;

	$('#alarmaChk').change(function() {
                ChkOnChange('#alarmaChk', '/alarma/on/','/alarma/off/');
        });
	$('#autoChk').change(function() {
                ChkOnChange('#autoChk', '/auto/on/','/auto/off/');
        });
        $('#parkingChk').change(function() {
                ChkOnChange('#parkingChk', '/radioParking/on/','/radioParking/off/');
        });
	sNotifMsg = $('#notifMsg').attr('value')
	if (sNotifMsg)
		$('#alarmaLbl').notify(sNotifMsg, notifOptions);
}

function ChkOnChange(ctrlId, urlOn, urlOff) {
        var chkActive = $(ctrlId).is(':checked');
	if (chkActive) {
                window.location.href = urlOn;
        }
        else {
                window.location.href = urlOff;
        }
}

$(function() {
	init();
})
