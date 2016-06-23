$(document).ready(function(){
	//console.log("ready");
	//var game_id = $("#loading").val();
	function checkuserjoin(){

		$.ajax
		({
			url:"/game/userjoin/",
			//data : {game_id:game_id}
			type : 'POST',
			success:function(result){
				var pcount = result['playercount'];
				console.log(pcount);
				if(pcount > 1){
					var seconds_left = 100;
					var interval = setInterval(function() {
						$("#loading").html('');
						$("#timer_div").html('<h4>Your game will start in ' + --seconds_left + ' seconds');
					    if (seconds_left <= 0)
					    {
					        $("#timer_div").html('Get Set Go');
					        clearInterval(interval);
					    }
					}, 1000);
				}
				else{
					$("#loading").html('<h4> Waiting for users to Join your game </h4>');
					checkuserjoin();
				}
			}
		});
	}
	checkuserjoin();
	
});

