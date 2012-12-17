$(document).ready(function() {
	// initialize page, selecting Shorten Link tab
	$('#tabs a[href="#importDataTab"]').tab('show');
	
	// tab click animation
	$('#tabs a[href="#organizationPerformanceTab"]').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
  		$('#branchPerformanceTab').hide();
  		$('#organizationPerformanceTab').show();
		$('#importDataTab').hide();
		$('#loPerformanceTab').hide();
	});
	
	// tab click animation
	$('#tabs a[href="#importDataTab"]').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
		$('#branchPerformanceTab').hide();
  		$('#organizationPerformanceTab').hide();
  		$('#importDataTab').show();
		$('#loPerformanceTab').hide();
	});

	// tab click animation branchPerformanceTab
  	$('#tabs a[href="#branchPerformanceTab"]').click(function (e) {
                e.preventDefault();
                $(this).tab('show');
                $('#branchPerformanceTab').show();
		$('#organizationPerformanceTab').hide();
                $('#importDataTab').hide();
		$('#loPerformanceTab').hide();
		
        });
	
	// tab click animation loPerformanceTab
        $('#tabs a[href="#loPerformanceTab"]').click(function (e) {
                e.preventDefault();
                $(this).tab('show');
                $('#branchPerformanceTab').hide();
                $('#organizationPerformanceTab').hide();
                $('#importDataTab').hide();
                $('#loPerformanceTab').show();

        });
	
	// OrgPerformance Tab
  	$.get('/microfinance/OrgData', function(data) {
 	graph_now(data);
 	updateOrgPerformanceTable(data);
	});
	
	// BranchPerformance Tab
	var branch_data = $.get('/microfinance/BranchData', function(data) {
	metric = $('#branchMetric').val();
 	graph_branch(data,metric);
	});

        $('#branchMetric').change(function() {
	var branch_data_JSON = $.parseJSON(branch_data.responseText);
        $('#branch_chart').empty();
	$('#branch_legend').empty();
	metric = $('#branchMetric').val();
        graph_branch(branch_data_JSON,metric);
        });

	// loPerformanceTab
        $.get('/microfinance/LoanOfficerData',$('#loBranch').serialize(),function(data) {
        console.log(data);
	metric = $('#loMetric').val();
	graph_lo(data,metric);
        });
        
	$('#loBranch').change(function() {
		$.get('/microfinance/LoanOfficerData',$('#loBranch').serialize(),function(data) {
		metric = $('#loMetric').val();
		$('#lo_chart').empty();
		$('#lo_legend').empty();
		graph_lo(data,metric);
		});
	});

	$('#loMetric').change( function() {
		$.get('/microfinance/LoanOfficerData',$('#loBranch').serialize(), function(data) {
		metric = $('#loMetric').val();
		$('#lo_chart').empty();
		$('#lo_legend').empty();
		graph_lo(data,metric);		
		});
	});

	// get data for CSV FILE DELETE
	$.get('/microfinance/CsvDataFiles', function(data) {
	appendDeleteFilesForm(data);
	});

	$('#deleteFilesForm').submit(function() {
        var files_delete = $(this).serialize();
        console.log(files_delete);
        $.ajax({
                url: "/microfinance/CsvDataFiles",
                data: files_delete,
		type: "DELETE"
                });
	return false; 
        });

	return false;

});
  	
function appendDeleteFilesForm(data) {

	for (var i = 0; i < data.files.length; i++) {
	$('#deleteFilesFormTable').append("<tr><td>"+data.files[i]+"</td><td><input type='checkbox' name='file' value='"+data.files[i]+"'</td></tr>");
	}	
}

function updateOrgPerformanceTable(data) {

	for (var i = 0; i < data.results.length; i++) {
   	 //console.log(data.db[i][0]);
   	 //console.log(data.db[i][1]);
   	 //console.log(data.clicks[i][1]);
   	 var dt = data.results[i]['ReportDate'];
   	 var cl = data.results[i]['loanClients'];
   	 var op = Math.round(data.results[i]['principalBalance']);
   	 var p1 = Math.round(data.results[i]['principal1Day']);
   	 var p30 = Math.round(data.results[i]['Principal30Day']);

	$('#orgPerformanceTableHeader').append("<th>"+dt+"</th>");
	$('#orgClients').append("<td>"+cl+"</td>");
	$('#orgPortfolio').append("<td>TZS"+numberWithCommas(op)+"</td>");
	$('#orgPortfolio1').append("<td>TZS"+numberWithCommas(p1)+"</td>");
	$('#orgPortfolio30').append("<td>TZS"+numberWithCommas(p30)+"</td>");
/*
$('#orgPerformanceTableBody').append("<tr><td>"+cl+"</td><td>"+"$"+numberWithCommas(op)+"</td><td>"+"$"+numberWithCommas(p1)+"</td><td>"+
"$"+numberWithCommas(p30)+"</td></tr>");

$('#orgPerformanceTableBody').append("<tr><td>"+dt+"</td><td>"+cl+"</td><td>"+"$"+numberWithCommas(op)+"</td><td>"+"$"+numberWithCommas(p1)+"</td><td>"+"$"+numberWithCommas(p30)+"</td></tr>"); 
*/	
	}
}

function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function graph_now(data) {

var seriesData = [[],[],[]];

	for (var i=0;i<data.results.length;i++) {
		seriesData[0].push( { x: 
		Date.parse(data.results[i]['ReportDate']).getTime()/1000, 
		y: parseFloat(data.results[i]['principalBalance']) } );
 		seriesData[1].push( { x: 
		Date.parse(data.results[i]['ReportDate']).getTime()/1000, y: 
		parseFloat(data.results[i]['principal1Day']) } );
		seriesData[2].push( { x: 
		Date.parse(data.results[i]['ReportDate']).getTime()/1000, 
		y: parseFloat(data.results[i]['Principal30Day']) } );	
		//console.log(data.results[i]['ReportDate']);
	}

var palette = new Rickshaw.Color.Palette();

var graph = new Rickshaw.Graph( {
	element: document.getElementById("chart"),
	width: 800,
	height: 400,
	renderer: 'line',
	series: [
		{
//			color: "#c05020",
			color: palette.color(),
			data: seriesData[0],
			name: 'Principal Balance'
		}, {
//			color: "#30c020",
			color: palette.color(),
			data: seriesData[1],
			name: 'Principal > 1 day'
		}, {
//			color: "#6060c0",
			color: palette.color(),
			data: seriesData[2],
			name: 'Principal > 30 days'
		}
	]
} );

var x_axis = new Rickshaw.Graph.Axis.Time({
	graph: graph
});

var y_axis = new Rickshaw.Graph.Axis.Y({
	graph: graph,
	tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
});

//

var hoverDetail = new Rickshaw.Graph.HoverDetail( {
	graph: graph
} );

var legend = new Rickshaw.Graph.Legend( {
	graph: graph,
	element: document.getElementById('org_legend')

} );

var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
	graph: graph,
	legend: legend
} );

var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
    graph: graph,
    legend: legend
});

var axes = new Rickshaw.Graph.Axis.Time( {
	graph: graph
} );
/*
var slider = new Rickshaw.Graph.RangeSlider({
    graph: graph,
    element: document.querySelector('#org_slider')
});
*/
graph.render();

}

function graph_branch(data,metric) {

var seriesData = [[],[],[],[],[],[]];

	for (var i=0;i<data.ho.length;i++) {
		seriesData[0].push( { x:
		Date.parse(data.ho[i]['ReportDate']).getTime()/1000,
		y: parseFloat(data.ho[i][metric]) });
	
                seriesData[1].push( { x:
                Date.parse(data.ar[i]['ReportDate']).getTime()/1000,
                y: parseFloat(data.ar[i][metric]) });

                seriesData[2].push( { x:
                Date.parse(data.da[i]['ReportDate']).getTime()/1000,
                y: parseFloat(data.da[i][metric]) });

                seriesData[3].push( { x:
                Date.parse(data.mo[i]['ReportDate']).getTime()/1000,
                y: parseFloat(data.mo[i][metric]) });

                seriesData[4].push( { x:
                Date.parse(data.te[i]['ReportDate']).getTime()/1000,
                y: parseFloat(data.te[i][metric]) });

                seriesData[5].push( { x:
                Date.parse(data.hi[i]['ReportDate']).getTime()/1000,
                y: parseFloat(data.hi[i][metric]) });
	}

var palette = new Rickshaw.Color.Palette();
	
var graph = new Rickshaw.Graph( {
	element: document.getElementById("branch_chart"),
	width: 800,
	height: 400,
//	renderer: 'line',
	series: [
		{
			color: palette.color(),
			data: seriesData[0],
			name: 'Head Office'
		}, {
			color: palette.color(),
			data: seriesData[1],
			name: 'Arusha'
		}, {
			color: palette.color(),
			data: seriesData[2],
			name: 'Dar es Salaam'
		}, {
			color: palette.color(),
			data: seriesData[3],
			name: 'Moshi'
		}, {
			color: palette.color(),
			data: seriesData[4],
			name: 'Tengeru'
		}, {
			color: palette.color(),
			data: seriesData[5],
			name: 'Himo'
		}
	]
} );

var x_axis = new Rickshaw.Graph.Axis.Time({
	graph: graph
});

var y_axis = new Rickshaw.Graph.Axis.Y({
	graph: graph,
	tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
});

var hoverDetail = new Rickshaw.Graph.HoverDetail( {
	graph: graph
} );

var legend = new Rickshaw.Graph.Legend( {
	graph: graph,
	element: document.getElementById('branch_legend')

} );

var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
	graph: graph,
	legend: legend
} );

var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
    graph: graph,
    legend: legend
});

var axes = new Rickshaw.Graph.Axis.Time( {
	graph: graph
} );

graph.render();

}

function graph_lo(data,metric) {

var lo_dict = {};

        for (var i=0;i<data.results.length;i++) {
                for (var y=0;y<data.results[i][1].length;y++) {
                	lo_dict[data.results[i][1][y]['Name']] = [];
                }
        }

        for (var i=0;i<data.results.length;i++) {
                for (var y=0;y<data.results[i][1].length;y++) {
                        lo_dict[data.results[i][1][y]['Name']].push(
                        { x: Date.parse(data.results[i][0]).getTime()/1000,
                        y: data.results[i][1][y][metric] } );
                }
        }

	for (var key in lo_dict) {
		while ( lo_dict[key].length < data.results.length ) {
		lo_dict[key].push( { x: 0, y: 0 } );
		}
	}

console.log(lo_dict);

var palette = new Rickshaw.Color.Palette();

var graph_series = [];
	for (var key in lo_dict) {
	graph_series.push( {
		color: palette.color(),
		data: lo_dict[key],
		name: key
	});
	}

var graph = new Rickshaw.Graph( {
	element: document.getElementById("lo_chart"),
	width: 800,
	height: 400,
	renderer: 'line',
	series: graph_series
} );

var x_axis = new Rickshaw.Graph.Axis.Time({
	graph: graph
});

var y_axis = new Rickshaw.Graph.Axis.Y({
	graph: graph,
	tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
});

var hoverDetail = new Rickshaw.Graph.HoverDetail( {
	graph: graph
} );

var legend = new Rickshaw.Graph.Legend( {
	graph: graph,
	element: document.getElementById('lo_legend')

} );

var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
	graph: graph,
	legend: legend
} );

var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
    graph: graph,
    legend: legend
});

var axes = new Rickshaw.Graph.Axis.Time( {
	graph: graph
} );

graph.render();

}
