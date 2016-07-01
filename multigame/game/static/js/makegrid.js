$(document).ready(function(){
	$.ajax({
		url: "/game/arena/",
		type : 'POST',
		success : function(result){
			var result = JSON.stringify(result);
			var json_obj = $.parseJSON(result);
			var gamedet = $.parseJSON(json_obj.game_details);
			var playerdet = $.parseJSON(json_obj.player_details);
			count =1;
			gridsize = gamedet[0].fields.square;
			for(i = 0; i<gridsize; i++){
				for(j = 0 ; j<gridsize; j++){
					boxdim = 500/gridsize;
					left = 420 + i*boxdim;
					ycor = 120+ j*boxdim;
					//console.log('<div class = "board" style = "position:absolute; left:'+left+'px;top :'+ycor+'px "> </div>');
					$("#makegrid").append('<div class = "board" id="area'+ count + '"style = "position:absolute; left:'+left+'px;top :'+ycor+'px "> </div>' );
					count ++;
				}
			}
			for(i =0 ; i< playerdet.length ; i++){
				$("#active_player_info").append('<br><br>'+playerdet[i].fields.username + ' : ' + playerdet[i].fields.color );
			}
		}
	});
	waitbeforeclick();
	$('#makegrid').on('click','.board',function(){
		var id = $(this).attr('id');
		$.ajax({
			url : "/game/updatescore/",
			type : 'POST',
			data : {id : id} ,
			success: function(result){
				waitbeforeclick();
			}
		});
	});
});

function waitbeforeclick(){
	$.ajax({
		url: "/game/checkgamestatus/",
		type : 'POST',
		success : function(result){
			if(result.status == false){
				console.log("yaha");
				var seconds_left = 20;
				var interval = setInterval(function() {
					--seconds_left;
					$("body").addClass("loading");
					if (seconds_left <= 0)
				    {
				    	$.ajax({
				    		url: "/game/changegamestatus/",
							type : 'POST',
							async : false,
							success : function(result){
								$("body").removeClass("loading");
				        		clearInterval(interval);
				        		waitbeforeclick();
							}
				    	});
				    }
				},1000)
			}
			else{
				//console.log("its here");
				waitbeforeclick();//alert("ab click hoga");
			}
		}
	});
}

