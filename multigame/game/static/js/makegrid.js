$(document).ready(function(){
	$.ajax({
		url: "/game/arena/",
		type : 'POST',
		success : function(result){
			var result = JSON.stringify(result);
			var json_obj = $.parseJSON(result);
			var gamedet = $.parseJSON(json_obj.game_details);
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
				divid = result.divid;
				color = result.usercol;
				$('#'+divid).removeClass("board");
				$('#'+divid).addClass("acquired");
				$('#'+divid).css("background", color);
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
			playerdet = JSON.parse(result.player_details);
			active_data = "<i> Active Players </i>"
			for(i =0 ; i< playerdet.length ; i++){
				active_data = active_data + '<br><br>'+playerdet[i].fields.username + ' : ' + playerdet[i].fields.color;
			}
			$("#active_player_info").html(active_data);
			griddet = JSON.parse(result.grid_details);
			for(i = 0 ; i < griddet.length ; i ++){
				divid = griddet[i].fields.divs;
				color = griddet[i].fields.div_color;
				$('#'+divid).removeClass("board");
				$('#'+divid).addClass("acquired");
				$('#'+divid).css("background", color);
			}
			if(result.status == false){
				$("body").addClass("loading");
				var seconds_left = 10;
				var interval = setInterval(function() {
					--seconds_left;
					//console.log(seconds_left);
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

