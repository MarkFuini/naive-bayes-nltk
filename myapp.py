import classifier
from GChartWrapper import Pie
from cgi import parse_qs, escape

html = """
<html>
<head>
<script>
function selectDefaults()
{
var combo = document.getElementById ( "origin" );
combo.value = '%s';

combo = document.getElementById ( "dest" );
combo.value = '%s';   

combo = document.getElementById ( "depthour" );
combo.value = '%s';   

combo = document.getElementById ( "dayofweek" );
combo.value = '%s';   
  
}
</script>
<body onload="selectDefaults();">
<!--<IMG SRC="/home/spry/environments/tutorial2/myapp/chart.png" ALT="some text" WIDTH=32 HEIGHT=32> -->
<h2>Flight Delay Prediction</h2>
<form method="get" action="">
<table>
<tr>
<td rowspan="2">
	Origin:
        <select name="origin" id="origin">
               <option value="ANY">ANY</option>
	       <option value="BWI">BWI</option>
               <option value="DFW">DFW</option>
	       <option value="FLL">FLL</option>
               <option value="PHL">PHL</option>
               <option value="MSY">MSY</option>
	</select> 
      </p>
      <p>
	Destination:
	<select name="dest" id="dest">
                <option value="ANY">ANY</option>
		<option value="BWI">BWI</option>
                <option value="DFW">DFW</option>
	        <option value="FLL">FLL</option>
   	        <option value="PHL">PHL</option>
  		<option value="MSY">MSY</option>

	</select> 
      </p>
      <p>
	Depart Hour:
	<select name="depthour" id="depthour">
	  <option value="ANY">ANY</option>
          %s
	</select>
      </p>
	<p>
	Day of Week: 
	<select name="dayofweek" id="dayofweek">
	  <option value="ANY">ANY</option>
	  <option value="1">1</option>
	  <option value="2">2</option>
	  <option value="3">3</option>
	  <option value="4">4</option>
	  <option value="5">5</option>
	  <option value="6">6</option>
	  <option value="7">7</option>
	</select> 
	</p>
      <p>
         <input type="submit" value="Submit">
      </p>
      </form>
</td>
<td>
Flights with this criteria will be:
<p>
On-time %s %% of the time.<br>
Late %s %% of the time.
</p>
</td>
</tr>

<tr>
<td align="left">
<p>
<img src="%s"/>
</p>
</td>
</tr>

</table>

</body>
</html>"""

c = classifier.Classifier()
c.load('fll-bwi.csv')
c.train()

def app(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])

    # create the feature set from the selected options
    origin = d.get('origin', [''])[0]
    dest = d.get('dest', [''])[0]
    depthour = d.get('depthour', [''])[0]
    dayofweek = d.get('dayofweek', [''])[0]

    featureset=dict()
    if origin != 'ANY' and origin != '':
     featureset[ 'origin' ] = origin
    if dayofweek != 'ANY' and dayofweek != '':
     featureset['dayofweek']=dayofweek
    if depthour != 'ANY' and depthour != '':
     featureset['depthour']=depthour
    if dest != 'ANY' and dest != '':
     featureset['dest']=dest

    print featureset
    ontime = round(c.findprob(featureset,'ontime') * 100,2)
    late = round(c.findprob(featureset,'late') * 100,2)

    print ontime, late

    # set up the combo for hour of day
    hourofday = ""
    select = "<option value=""%d"">%d</option>"
    for i in range(24):
	hourofday = hourofday + select % (i,i)

    # transform response
    pie = Pie([late,ontime]).title('Flight Delay').color('red','lime').label('late', 'on-time')

    response_body = html % (origin, dest,depthour,dayofweek,hourofday, ontime, late, pie )

    start_response("200 OK", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(response_body)))
    ])
    return iter([response_body])

