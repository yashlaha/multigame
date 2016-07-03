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
			active_data = "<i> Active Players </i><br><br><table border = '1'><tr><b><th> Player Name </th><th> Color </th><th> Score </th></b></tr>";
			for(i =0 ; i< playerdet.length ; i++){
				active_data = active_data + '<tr> <td>'+playerdet[i].fields.username + '</td><td>' +playerdet[i].fields.color+'</td><td>' +playerdet[i].fields.score+ '</td> </tr>';
			}
			//console.log(active_data);
			active_data = active_data + "</table>";
			$("#active_player_info").html(active_data);
			$("#your_score").html('<h2> Your Score </h2><br><h1>' + result.score + '</h1>');
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
				var seconds_left = 5;
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
				if(griddet.length == result.gridsize * result.gridsize){
					$("#makegrid").html("");
					final_data = '<table border = "1" class = "result_table"><tr><b><th> Player Name </th><th> Color </th><th> Score </th></b></tr>';
					for(i =0 ; i< playerdet.length ; i++){
						final_data = final_data + '<tr> <td>'+playerdet[i].fields.username + '</td><td>' +playerdet[i].fields.color+'</td><td>' +playerdet[i].fields.score+ '</td> </tr>';
					}
					final_data = final_data + '</table>';
					$("#score_display").html(final_data);
					$("#final_result").css("display", "block");	
					$.ajax({
						url : "/game/finaldisplay/",
						type : "POST",
						success : function(result){
							windata = JSON.parse(result.allwin)
							console.log(windata.length);
							if(windata.length == 1){
								$("#winner").html(windata[0].fields.username + "won the game !!!!");
								if(windata.your_res == "yes"){
									$("#your_result").html("<h2> You Win !!!! </h2>");
								}
								else{
									$("#your_result").html("<h2> You Lost !!!! </h2>");	
								}
								$("#note").show();		
							}
							else{
								//console.log("here");
								if(windata.your_res == "yes"){
									$("#your_result").html("<h2> You are a shared Winner !!!! </h2>");
								}
								else{
									$("#your_result").html("<h2> You Lost !!!! </h2>");	
								}	
								message = "<h4>Game tied between ";
								for(i=0;i<windata.length;i++){
									message = message + windata[i].fields.username + ', ' ;
								}
								message = message.substring(0, message.length - 2);
								message = message + '</h4>';
								//console.log(message);
								$("#winner").html(message);
								$("#note").show();	
							}
						}
					});		
				}
				//console.log("its here");
				waitbeforeclick();//alert("ab click hoga");
			}
		}
	});
}

