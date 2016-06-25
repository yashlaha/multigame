$(document).ready(function(){
	$.ajax({
		url: "/game/arena/",
		type : 'POST',
		success : function(result){
			
			var result = JSON.stringify(result);
			var json_obj = $.parseJSON(result);
			console.log(json_obj)
			var player = $.parseJSON(json_obj.player_details);
			console.log(player);
			console.log(player.fields);
			//xs = JSON.stringify(x);
			//ys = JSON.stringify(y);
			console.log(x);
			console.log(y);
			for(i = 0; i<gridsize; i++){
				for(j = 0 ; j<gridsize; j++){
					boxdim = 500/gridsize;
					left = 400 + i*boxdim;
					ycor = 120+ j*boxdim;
					//console.log('<div class = "board" style = "position:absolute; left:'+left+'px;top :'+ycor+'px "> </div>');
					$("#makegrid").append('<div class = "board" style = "position:absolute; left:'+left+'px;top :'+ycor+'px "> </div>' );

				}
			}
		}
	})
});