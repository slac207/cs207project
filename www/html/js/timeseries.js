// code modified from flot AJAX example 	
// http://www.flotcharts.org/flot/examples/ajax/index.html
	
	$(function() {

		// flot plot options! 
		var options = {
			lines: {
				show: true
			},
			points: {
				show: false
			},
			legend: {
				show: true
			},
			grid: {
        		hoverable: true
      		}
	};

		// GLOBAL VARIABLES AND FUNCTIONS
		
		
		console.log('Initializing variables.');
		// initialize the arrays hold the data for plotting
		var data = [];
		var dataTarget = [];
		
		// IP address to access our UI
		// (empty for relative URLs)
		var publicIP = '';
		
		// building blocks of metadata table
		var tableTop = "<table id='metadata'>";
		var tableBottom = "</table>";
		var tableHeader = "<tr style='background-color:black;color:white;'><th>ID</th><th>Mean</th><th>StDev</th><th>Level</th><th>Blarg</th></tr>";
		var metadataTable = tableTop + tableHeader;
		
		// helps with managing the uploaded time series
		var files;
		
		// initialize the timeseries plot (will be empty)
		console.log('Initializing flot plot (empty plot).');
		$.plot("#placeholder", data, options);

		// ACTIONS TO COMPLETE WHEN THE `SUBMIT` BUTTON IS CLICKED
		$("button#tsQuery").click(function () {
		
			console.log('Submit button has been clicked.');
			
			// show the progress bar so the user knows that stuff 
			// is going on behind the scenes
			
			console.log('Adding in ticking progress bar.');
			$( "#progressbar" ).progressbar({
  				value: false
			}); 
			
			// reset everything in preparation for new data
			console.log('Resetting helper variables in preparation for new data.');
			document.getElementById('timeseriesMetadata').innerHTML = '';
			data = [];
			var simIDs = [];
			var idNum = {};
			var counter = 0;
			metadataTable = tableTop + tableHeader;
			
			$.plot("#placeholder", data, options);

			// retrieve the time series specified by the user, and the number of 
			//   most similar time series
			var timeSeriesID = document.getElementById("tsID").value;
			var numSim = document.getElementById("n_closest").value;
			console.log('Retrieved timeseries ID #' + timeSeriesID + 'and will retrieve the ' + numSim + 'most similar timeseries.');

			// CONSTRUCT OUR QUERY
			// if the user has specified an ID, use that; 
			//   otherwise assume there's an uploaded file.
			if (timeSeriesID != '') {
			
				// DECIDE WHETHER WE NEED A SIMQUERY
				// if the user hasn't provided a number of similar TS, or the
				//   number is zero, we won't bother sending off a simquery
				if (numSim == '' | numSim == 0) {
					
					// add on the ID number of the target TS
					simIDs.push(timeSeriesID);
					
					// now we loop over all the IDs and collect their data
					console.log("Collecting data of specified time series.");
					
					var dataurl = publicIP + "/timeseries/" + timeSeriesID;
								
					console.log('Retrieving data associated with TS ID#'+ timeSeriesID + '.');
				
					$.ajax({
						url: dataurl,
						type: "GET",
						dataType: "json",
						success: onDataReceived
					});

				
				} else {
			
					var simurl = publicIP + "/simquery?id=" + timeSeriesID + "&topn=" + numSim;
					console.log('Constructed simquery:', simurl);
				
					// get the IDs of the similar time series
					console.log('Retrieving the ID numbers of the similar TS (ID number supplied).');
					$.ajax({
						url: simurl,
						type: "GET",
						dataType: "json",
						success: function(data) {
						
									// parse the ID numbers returned from the server
									getSimIDs(data);
								
									// add on the ID number of the target TS
									simIDs.push(timeSeriesID);

									// now we loop over all the IDs and collect their data
									console.log("Looping over the retrieved ID numbers and collecting their data.");
							
									for(var i=0; i < simIDs.length; i++) {
				
										idNum   = simIDs[i];
								
										var dataurl = publicIP + "/timeseries/" + idNum;
								
										console.log('Retrieving data associated with TS ID#'+ idNum + '.');
										// solution from http://stackoverflow.com/questions/4201934/
										//               jquery-ajax-pass-additional-argument-to-success-callback
										$.ajax({
											url: dataurl,
											type: "GET",
											dataType: "json",
											success: onDataReceived
										});
				
									}		
						 }
					});
				}
				
			} else if ( document.getElementById("fileSelect").files.length > 0  ) {
			
				// DECIDE WHETHER WE NEED A SIMQUERY
				// if the user hasn't provided a number of similar TS, or the
				//   number is zero, we won't bother sending off a simquery
				if (numSim == '' | numSim == 0) {
				
					console.log("Locally received data uploaded by user.");			
					console.log( document.getElementById("fileSelect").files[0] );
			
					// parse the uploaded file
					// https://www.html5rocks.com/en/tutorials/file/dndfiles/
					read = new FileReader();
					read.readAsText(document.getElementById("fileSelect").files[0]);
					
					read.onloadend = function(){
						//console.log(read.result);
						//console.log(JSON.parse(read.result))
						//console.log(JSON.parse(read.result).ts)
						var dataTemp = JSON.parse(read.result).ts;
						dataTarget = dataTemp[0].map(function (e, i) { 
												return [e, dataTemp[1][i]];});												
									
						tsData = {label: "uploaded timeseries", data: dataTarget, lines: {lineWidth:6}};
					
						console.log('Appending uploaded time series to Flot data.');
					
						data.push(tsData);
					
						console.log(tsData);
					
						console.log('Plotting the data of the uploaded TS.');		
				
						$.plot("#placeholder", data, options);	
						
						console.log("Destroy the progress bar -- we don't need it anymore.");
						$("#progressbar").progressbar( "destroy" );

					}			
				
				} else {
			
					console.log("Locally received data uploaded by user.");			
					console.log( document.getElementById("fileSelect").files[0] );
			
					var simurl = publicIP + "/simquery?" + "topn=" + numSim;

					console.log("Sending user-loaded data off to be processed:" + simurl);
					$.ajax({
						url: simurl,
						type: 'POST',
						data: document.getElementById("fileSelect").files[0],
						cache: false,
						contentType: 'application/json; charset=utf-8',
						dataType: 'json',
						processData: false, // Don't process the files
						contentType: false, // Set content type to false as jQuery will tell the server its a query string request
						error: function(jqXHR, textStatus, errorThrown) {
					 			// Handle errors here
									console.log('ERRORS: ' + textStatus);
						}
					})
						.done(function (result) {
		
							simIDs = result.id;
				
							$.ajax({
								url: simurl,
								type: "GET",
								dataType: "json",
								success: function(data) {

										// loop over all the IDs and collect their data
										console.log("Looping over the retrieved ID numbers and collecting their data.");
							
										for(var i=0; i < simIDs.length; i++) {
				
											idNum   = simIDs[i];
								
											var dataurl = publicIP + "/timeseries/" + idNum;
								
											console.log('Retrieving data associated with TS ID#' + idNum + '.');
											// solution from http://stackoverflow.com/questions/4201934/
											//               jquery-ajax-pass-additional-argument-to-success-callback
											$.ajax({
												url: dataurl,
												type: "GET",
												dataType: "json",
												success: onDataReceived
											});
				
										}		
							 }
						});
			
					// parse the uploaded file
					// https://www.html5rocks.com/en/tutorials/file/dndfiles/
					read = new FileReader();
					read.readAsText(document.getElementById("fileSelect").files[0]);
					
					read.onloadend = function(){
						//console.log(read.result);
						//console.log(JSON.parse(read.result))
						//console.log(JSON.parse(read.result).ts)
						var dataTemp = JSON.parse(read.result).ts;
						dataTarget = dataTemp[0].map(function (e, i) { 
												return [e, dataTemp[1][i]];});
									
						tsData = {label: "uploaded timeseries", data: dataTarget, lines: {lineWidth:6}};
					
						console.log('Appending uploaded time series to Flot data.');
					
						data.push(tsData);
					
						console.log(tsData);
					
						console.log('Plotting the data of the uploaded TS.');		
				
						$.plot("#placeholder", data, options);	

					}
			});
				}
					
			} else {
				// user hasn't specified anything!
				alert("You gotta give us something valid to work with...");
				
				$("#progressbar").progressbar( "destroy" );
			}
			
			function onDataReceived(series) {
			
				// pull the similar TS
				// 

				// * solution from Stack Overflow:
				//   http://stackoverflow.com/questions/22015684/
				//             how-do-i-zip-two-arrays-in-javascript
				console.log('Zipping TS ID#' + simIDs[counter] + ' into appropriate form for Flot to plot.');
				var dataTarget = series.ts[0].map(function (e, i) { 
					return [e, series.ts[1][i]]; 
				});
				
				tsData = {label: "timeseries " + simIDs[counter], data: dataTarget};
				
				console.log('Appending TS ID#' + simIDs[counter] +' to Flot data.');
				data.push(tsData);
				
				$.plot("#placeholder", data, options);	

				
				// if (1) we've reached the target TS ID, in the case of a specified TS ID
				//    (2) we've reached the end of the similar IDs, in the case of 
				//        an uploaded TS, 
				// we're done putting together the metadata table. 
				// highlight the row of the targt TS ID and show the table to the world
				if( series.metadata[0].id == timeSeriesID ) {	
				
					var tableRow = "<tr style='background-color:yellow;'><td>" + series.metadata[0].id + "</td>";
					tableRow    += "<td>" +series.metadata[0].mean  + "</td>";
					tableRow    += "<td>" +series.metadata[0].std   + "</td>";
					tableRow    += "<td>" +series.metadata[0].level + "</td>";
					tableRow    += "<td>" +series.metadata[0].blarg + "</td></tr>";
				
					console.log("Adding ID #" + series.metadata[0].id + " to metadata table.")
					metadataTable += tableRow;
								
					console.log("Put together + display the metadata table.");
					metadataTable += tableBottom;
					document.getElementById('timeseriesMetadata').innerHTML = metadataTable;	
					console.log("Destroy the progress bar -- we don't need it anymore.");
					$("#progressbar").progressbar( "destroy" );	
					
				} else if ( counter == simIDs.length - 1 ) {
				
					var tableRow = "<tr><td>" + series.metadata[0].id + "</td>";
					tableRow    += "<td>" +series.metadata[0].mean  + "</td>";
					tableRow    += "<td>" +series.metadata[0].std   + "</td>";
					tableRow    += "<td>" +series.metadata[0].level + "</td>";
					tableRow    += "<td>" +series.metadata[0].blarg + "</td></tr>";
				
					console.log("Adding ID #" + series.metadata[0].id + " to metadata table.")
					metadataTable += tableRow;
								
					console.log("Put together + display the metadata table.");
					metadataTable += tableBottom;
					document.getElementById('timeseriesMetadata').innerHTML = metadataTable;	
					console.log("Destroy the progress bar -- we don't need it anymore.");
					$("#progressbar").progressbar( "destroy" );
				
				} else {
				
					// put together the metadata
					var tableRow = "<tr><td>" + series.metadata[0].id + "</td>";
					tableRow    += "<td>" +series.metadata[0].mean  + "</td>";
					tableRow    += "<td>" +series.metadata[0].std   + "</td>";
					tableRow    += "<td>" +series.metadata[0].level + "</td>";
					tableRow    += "<td>" +series.metadata[0].blarg + "</td></tr>";
				
					console.log("Adding ID #" + series.metadata[0].id + " to metadata table.")
					metadataTable += tableRow;
				
				}
				
				// keeps track of where we are in the array of TS IDs to plot
				counter++;		

			}	
			
			function getSimIDs(series) { 
				for(var i=0; i < series.id.length; i++) {
					simIDs.push(series.id[i]); 
				}
			}
			
		});


		// Add the Flot version string to the footer
		$("#footer").prepend("Flot " + $.plot.version + " + ");
	});