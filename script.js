function myfunction_onload(prompt){
  console.log("Running code...")
  var pass_to_python = prompt
  $.ajax({
      type:'POST',
      dataType: 'json',
      contentType:'application/json;charset-utf-08',
      url: "http://127.0.0.1:5000/run_app?value='"+pass_to_python,
      success:function (data) {
        var reply=data.reply;
        if (reply=="success")
        {
            return;
        }
        else
            {
            alert("some error ocured in session agent")
            }
        }
      })
  console.log("Done!")
}



var margin  = {top: 10, right: 5, bottom: 10, left: 100},
    width   = 1150-margin.left-margin.right,
    height  = 900-margin.top-margin.bottom;   
//We start off by creating an SVG
// container to hold the visualization. We only need to specify
// the dimensions for this container.
var svg = d3.select("body").append("svg")
  .attr("width",width)
  .attr("height",height);

//create the tooltip that holds the country name
var tooltip = d3.select('body').append('div') .attr("class","tooltip")
      .style({
        'background' : 'black',
        'color':'white',
        'width':"90px",
        'border-radius':'15px',
        'text-align':'center',
        'padding-top':'10px',
        'padding-left':'5px',
        'padding-right':'5px',
        // 'padding-bottom':'3px'
        });

// d3.json("https://raw.githubusercontent.com/DealPete/forceDirected/master/countries.json",function(data){ 
  d3.json("output.json",function(data){ 
    console.log(data["tracks"]);

  // ensure that json has links field

  data["links"] = [
    { "target": 1, "source": 2 },
    { "target": 1, "source": 3 },
    { "target": 1, "source": 4 },
    { "target": 1, "source": 5 },
    { "target": 2, "source": 3 },
    { "target": 2, "source": 4 },
    { "target": 2, "source": 5 },
    { "target": 3, "source": 4 },
    { "target": 3, "source": 5 },
    { "target": 4, "source": 5 },
    { "target": 5, "source": 1 },
    { "target": 5, "source": 4 },
    { "target": 6, "source": 1 },
    { "target": 6, "source": 2 },
    { "target": 6, "source": 3 },
    { "target": 6, "source": 4 },
    { "target": 6, "source": 5 },
    { "target": 10, "source": 9 },
    { "target": 11, "source": 2 },
    { "target": 7, "source": 3 },
    { "target": 9, "source": 4 },
    { "target": 8, "source": 5 }
  ];
  
  // Extract the nodes and links from the data.
  var nodes = data["tracks"];
  var links = data["links"];
  // Now we create a force layout object and define its properties.
  // Those include the dimensions of the visualization and the arrays
  // of nodes and links.
  var force = d3.layout.force()
    .size([width,height])
    .nodes(d3.values(nodes))
    .links(links)
    .on("tick",tick)
// There's one more property of the layout we need to define,
// its `linkDistance`. That's generally a configurable value and,
// for a simple example, we'd normally leave it at its default.
// Unfortunately, the default value results in a visualization
// that's not especially clear. This parameter defines the
// distance (normally in pixels) that we'd like to have between
// nodes that are connected. (It is, thus, the length we'd
// like our links to have.)
    .linkDistance(500)
//now so it's time to turn
// things over to the force layout. Here we go.
    .start();
  
// Next we'll add the nodes and links to the visualization.
// Note that we're just sticking them into the SVG container
// at this point. We start with the links. The order here is
// important because we want the nodes to appear "on top of"
// the links. SVG doesn't really have a convenient equivalent
// to HTML's `z-index`; instead it relies on the order of the
// elements in the markup. By adding the nodes _after_ the
// links we ensure that nodes appear on top of links.

// Links are pretty simple. They're just SVG lines, and
// we're not even going to specify their coordinates. (We'll
// let the force layout take care of that.) Without any
// coordinates, the lines won't even be visible, but the
// markup will be sitting inside the SVG container ready
// and waiting for the force layout.
  var link = svg.selectAll('.link')
    .data(links)
    .enter().append('line')
    .attr("class","link");
  

  // Now it's the nodes turn. Each node is drawn as a flag.
  var node = d3.select('#flags').selectAll('img')
    .data(force.nodes())
    .enter().append('img').on("click", function(d) {
      title = document.getElementsByClassName("name");  // Find the elements
      albumCover = document.getElementsByClassName("cover");
      artists = document.getElementsByClassName("artist");
      wrapper = document.getElementsByClassName("wrapper");
      instructions = document.getElementsByClassName("instructions");
      more = document.getElementsByClassName("seeMore");
      guidelines = document.getElementsByClassName("guidelines");
      console.log(d["name"]);
      for(var i = 0; i < title.length; i++){
        title[i].innerText = d["name"];    // Change the content
        albumCover[i].style.backgroundImage= "url(" + d["album"]["images"][0]["url"] + ")"; 
        artists[i].innerText = d["artists"][0]["name"]; 
        instructions[i].innerText = ""; 
        wrapper[i].style.backgroundImage= "url(" + d["album"]["images"][0]["url"] + ")";
        guidelines[i].innerText = ""; 
        more[i].onclick = function () {
          window.open(
            d["external_urls"]["spotify"], "_blank");
        };
      } 
  })
  //we return the exact flag of each country from the image
    .attr('class', function (d) { return 'flag flag-' + Math.floor((Math.random() * (10 - 1) + 1)).toString(); })
  //we call some classes to handle the mouse
    .on('mouseover', mouseoverHandler)
    .on("mousemove",mouseMoving)
    .on("mouseout", mouseoutHandler);
  
  // We're about to tell the force layout to start its
  // calculations. We do, however, want to know when those
  // calculations are complete, so before we kick things off
  // we'll define a function that we want the layout to call
  // once the calculations are done.
  function tick(e){
    // First let's reposition the nodes. As the force
    // layout runs it updates the `x` and `y` properties
    // that define where the node should be positioned.
    // To move the node, we set the appropriate SVG
    // attributes to their new values. 
     node.style('left', function (d) { return d.x + 'px'; })
         .style('top', function (d) { return d.y + 'px'; })
         .call(force.drag);
    
    // We also need to update positions of the links.
    // For those elements, the force layout sets the
    // `source` and `target` properties, specifying
    // `x` and `y` values in each case.
    link.attr('x1', function(d){ return  d.source.x})
        .attr('y1',function(d){ return  d.source.y})
        .attr('x2', function(d){ return  d.target.x})
        .attr('y2',function(d){ return   d.target.y})
  }
  
  //hover over a flag
  //the tooltip with the name of the country is going to show up
  function mouseoverHandler (d) {
     tooltip.transition().style('opacity', .9)
     tooltip.html('<p>' + d["name"] + '</p>' );
  }
  //leaving a flag
  //the tooltip will disappear
  function mouseoutHandler (d) {
      tooltip.transition().style('opacity', 0);
  }

  function mouseMoving (d) {
      tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px").style("color","white");
  }
})

  function myFunction()
  {
  x=document.getElementsByClassName("name");  // Find the elements
      for(var i = 0; i < x.length; i++){
      x[i].innerText="Piece Title";    // Change the content
      }

  }

function guide()
{
x=document.getElementsByClassName("seeMore");  // Find the elements
guides = document.getElementsByClassName("guidelines");
    for(var i = 0; i < x.length; i++){
      if (guides[i].innerText == "") {
        guides[i].innerText = "We created Music Fun :3 to give music recommendations based on your mood! write out anything you have in mind and enjoy browsing through your song recs! \n\n\n examples: \n\n i'm so excited to eat out today \n\n hype me up! \n\n its cold and rainy outside right now :( \n\n\n\n <<-- press the blobs to find your songs :D";

      }
      else {
        guides[i].innerText = "";
      }
  }

}
document.addEventListener('keyup', function(e){
    if(e.keyCode == 13){
      var search = document.getElementsByClassName('search')[0].value;
      console.log(search);
      myfunction_onload(search);
    }

  })
