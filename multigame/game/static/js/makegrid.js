$(document).ready(function(){
	$.ajax({
		url: "/game/arena/",
		type : 'POST',
		success : function(result){
			var result = JSON.stringify(result);
			var json_obj = $.parseJSON(result);
			var gamedet = $.parseJSON(json_obj.game_details);
			var playerdet = $.parseJSON(json_obj.player_details);
			
			gridsize = gamedet[0].fields.square;
			for(i = 0; i<gridsize; i++){
				for(j = 0 ; j<gridsize; j++){
					boxdim = 500/gridsize;
					left = 420 + i*boxdim;
					ycor = 120+ j*boxdim;
					//console.log('<div class = "board" style = "position:absolute; left:'+left+'px;top :'+ycor+'px "> </div>');
					$("#makegrid").append('<div class = "board" style = "position:absolute; left:'+left+'px;top :'+ycor+'px "> </div>' );

				}
			}
			for(i =0 ; i< playerdet.length ; i++){
				$("#active_player_info").append('<br><br>'+playerdet[i].fields.username + ' : ' + playerdet[i].fields.color );
			}
		}
	})
});