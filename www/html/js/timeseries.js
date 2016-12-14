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
		
		// check whether the user specified a valid integer
		function isInt(n){
    		return Number(n) === n && n % 1 === 0;
		}
		
		// initialize the array that will hold the data for plotting
		var data = [];
		
		// IP address to access our UI
		var publicIP = 'http://54.157.228.231';
		
		// building blocks of metadata table
		var tableTop = "<table>"
		var tableBottom = "</table>"
		var tableHeader = "<tr><th>ID</th><th>Mean</th><th>StDev</th><th>Level</th><th>Blarg</th></tr>"
		var metadataTable = tableTop + tableHeader;
		
		// helps with managing the uploaded time series
		var files;
		var uploadButton = document.getElementById('tsQuery');
		
		// keep an eye on the file upload field, and save what's put there
		//$('input[type=file]').on('change', prepareUpload);

		// grab files and set them to our variable
		//function prepareUpload(event) {
  	//	files = event.target.files;
		//}
		
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
			console.log('Reseting helper variables in preparation for new data.');
			document.getElementById('timeseriesMetadata').innerHTML = '';
			data = [];
			var simIDs = [];
			var idNum = {};
			var counter = 0;
			metadataTable = tableTop + tableHeader;

			// retrieve the time series specified by the user, and the number of 
			//   most similar time series
			var timeSeriesID = document.getElementById("tsID").value;
			var numSim = document.getElementById("n_closest").value;
			console.log('Retrieved timeseries ID ', timeSeriesID, 'and will retrieve the ', numSim, 'most similar timeseries.');

			// CONSTRUCT OUR QUERY
			// if the user has specified an ID, use that; 
			//   otherwise assume there's an uploaded file.
			if (timeSeriesID != '') {
				var simurl = publicIP + "/simquery/" + timeSeriesID + "?topn=" + numSim;
				console.log('Constructed simquery.');
			} else if ( document.getElementById("fileSelect").files.length > 0  ) {
			
				// https://abandon.ie/notebook/simple-file-uploads-using-jquery-ajax
				
				//event.stopPropagation(); // Stop stuff happening
    		//event.preventDefault();  // Totally stop stuff happening

    		// Create a formdata object and add the files
    		var dataUpload = new FormData();
    		
    		// dataUpload.append( "ts",  );
    		
    		console.log( document.getElementById("fileSelect").files[0] );
    		
    		var simurl = publicIP + "/simquery" + "?topn=" + numSim;
    		
        //$(JSON.stringify({ ts: dataUpload })).appendTo('#dataTest')

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
        
        	var newData = result.id;
        	console.log(newData)

      	});
     		
   		 
   		 
				
				
			} else {
				
				alert("You gotta give us something valid to work with...");
			
			}
			
			function onDataReceived(series) {
			
				// pull the similar TS
				// 

				// * solution from Stack Overflow:
				//   http://stackoverflow.com/questions/22015684/
				//             how-do-i-zip-two-arrays-in-javascript
				console.log('Zipping TS ID#',simIDs[counter],' into appropriate form for Flot to plot.');
				var dataTarget = series.ts[0].map(function (e, i) { 
					return [e, series.ts[1][i]]; 
				});

				// Push the new data onto our existing data array
				//if (!alreadyFetched[timeSeriesID]) {
				//	alreadyFetched[timeSeriesID] = true;
					// data.push(series);
				//}
				
				tsData = {label: "timeseries " + simIDs[counter], data: dataTarget};
				
				console.log('Appending TS ID#',simIDs[counter],' to Flot data.');
				data.push(tsData);
				
				$.plot("#placeholder", data, options);	
				
				// parse and display the metadata
				document.getElementById('timeseriesMetadata').innerHTML = series.metadata[0];
				
				counter++;
								
				if (counter == simIDs.length - 1) {
					console.log("Destroy the progress bar -- we don't need it anymore.");
					$("#progressbar").progressbar( "destroy" );
					//document.getElementById('timeseriesMetadata').innerHTML = metadataTable;
					
					console.log("Plot the target curve on top and make it fancy!");
					//$.plot("#placeholder", data, options).getData()[counter].lines.lineWidth = 5;
					//$.plot("#placeholder", data, options)
				}
				
			}	
			
			function getSimIDs(series) { 
				for(var i=0; i < series.id.length; i++) {
					simIDs.push(series.id[i]); 
				}
			}
			
			// first get the IDs of the similar time series
			console.log('Retrieving the ID numbers of the similar TS.');
			$.ajax({
				url: simurl,
				type: "GET",
				dataType: "json",
				success: function(data) {

        		getSimIDs(data)
        		
        		simIDs.push(timeSeriesID);

        		  // call next ajax function
        			// now we loop over all the IDs and collect their data
							for(var i=0; i < simIDs.length; i++) {
				
								idNum   = simIDs[i];
								
								var dataurl = publicIP + "/timeseries/" + idNum;
								
								console.log('Retrieving data associated with TS ID#',idNum ,'.');
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
			
		});


		// Add the Flot version string to the footer
		$("#footer").prepend("Flot " + $.plot.version + " + ");
	});