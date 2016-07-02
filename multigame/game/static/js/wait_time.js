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
				var game = result['game'];
				var name = result['name'];
				console.log(game);
				console.log(name);
				console.log(pcount);
				if(pcount >2){
					$("#loading").html('<h4>Wait for the next round</h4>');
					$.ajax({
					url: "/game/checkgamestatus/",
					type : 'POST',
					success : function(result){
							if(result.status == true){
								window.location = '/game/arena/';
							}
							else{
								checkuserjoin();
							}
						}
					});
				}
				else if(pcount == 2){
					var seconds_left = 5;
					var interval = setInterval(function() {
						$("#loading").html('');
						$("#timer_div").html('<h4>Your game will start in ' + --seconds_left + ' seconds</h4>');
					    if (seconds_left <= 0)
					    {
					        window.location = '/game/arena/';
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

