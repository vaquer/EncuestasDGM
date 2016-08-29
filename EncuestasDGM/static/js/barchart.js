  
var jsonBarchart;

$.ajax({
  type: "GET",
  url: "partials/barchart_example.json",
  async: false,
  success: function(data){
    if (validaJsonBarChart(data) ){
      jsonBarchart = data;
    }
  }
});

	//Escala de colores
  var categoryDatos = [
  "#00cc99",
  "#ff6666",
  "#663399",
  "#474747",
  "#ff9900",
  "#0099ff",
  "#333399",
  "#000000",
  "#006666",
  "#ff6699",
  "#666699",
  "#999999"
  ];

  var w = 400,
  h = 400,
  r = 80,
  inner = 70,
  color = categoryDatos;

  data = jsonBarchart;

  var margin = {top: (parseInt(d3.select('#bar-chart').style('height'), 10)/20), right: (parseInt(d3.select('body').style('width'), 10)/20), bottom: (parseInt(d3.select('body').style('height'), 10)/20), left: (parseInt(d3.select('body').style('width'), 10)/10)},
  width = parseInt(d3.select('body').style('width'), 10) - margin.left - margin.right,
  height = parseInt(d3.select('body').style('height'), 10) - margin.top - margin.bottom;

  var x0 = d3.scale.ordinal()
  .rangeRoundBands([0, width], .1);

  var x1 = d3.scale.ordinal();

  var y = d3.scale.linear()
  .range([height, 0]);

  var colorRange = d3.scale.category20();
  var color = d3.scale.ordinal()
  .range(categoryDatos);

  var xAxis = d3.svg.axis()
  .scale(x0)
  .orient("bottom");

  var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left")
  .tickFormat(d3.format(".2s"));

  var divTooltip = d3.select("#bar-chart").append("div").attr("class", "toolTip");

  var svg = d3.select("#bar-chart").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("font-family","Open sans")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


  dataset = jsonBarchart.valores;


  var options = d3.keys(dataset[0]).filter(function(key) { return key !== "label"; });

  dataset.forEach(function(d) {
    d.valores = options.map(function(name) { return {name: name, value: +d[name]}; });
  });

  x0.domain(dataset.map(function(d) { return d.label; }));
  x1.domain(options).rangeRoundBands([0, x0.rangeBand()]);
  y.domain([0, d3.max(dataset, function(d) { return d3.max(d.valores, function(d) { return d.value; }); })]);

  svg.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis)
  .append("text")
  .attr("x", "35%" )
  .attr("y",  50 )
  .text(jsonBarchart.ejex.toUpperCase());

  svg.append("g")
  .attr("class", "y axis")
  .call(yAxis)
  .append("text")
  .attr("transform", "rotate(-90)")
  .attr("x", -150 )
  .attr("y", -60)
  .attr("dy", ".71em")
  .style("text-anchor", "end")
  .text(jsonBarchart.ejey.toUpperCase());

  var bar = svg.selectAll(".bar")
  .data(dataset)
  .enter().append("g")
  .attr("class", "rect")
  .attr("transform", function(d) { return "translate(" + x0(d.label) + ",0)"; });

  bar.selectAll("rect")
  .data(function(d) { return d.valores; })
  .enter().append("rect")
  .attr("width", x1.rangeBand())
  .attr("x", function(d) { return x1(d.name); })
  .attr("y", function(d) { return y(d.value); })
  .attr("value", function(d){return d.name;})
  .attr("height", function(d) { return height - y(d.value); })
  .style("fill", function(d) { return color(d.name); });

  bar.on("mousemove", function(d){
    divTooltip.style("left", d3.event.pageX-100+"px");
    divTooltip.style("top", d3.event.pageY-140+"px");
    divTooltip.style("display", "inline-block");
    var x = d3.event.pageX, y = d3.event.pageY
    var elements = document.querySelectorAll(':hover');
    l = elements.length
    l = l-1
    elementData = elements[l].__data__
    divTooltip.html("<span class='title-pop'>"+elementData.name+"</span><hr>" + jsonBarchart.ejey + ": "+elementData.value.toLocaleString('en'));
  });

  bar.on("mouseout", function(d){
    divTooltip.style("display", "none");
  });

      //////////////////// Horizontal Legend ////////////////

      var svgLegned4 = d3.select(".svgLegend4").append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("font-family","Open sans")
      
      var dataL = 0;
      var offset = 100;

      var legend4 = svgLegned4.selectAll('.legend4')
      .data(options.slice())
      .enter().append('g')
      .attr("class", "legend4")
      .attr("transform", function (d, i) {
        if (i === 0) {
          dataL = d.length + offset 
          return "translate(0,0)"
        } else { 

          var newdataL = dataL
          dataL +=  d.length + offset
          return "translate(" + (newdataL) + ",0)"
        }
      })

      legend4.append('rect')
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", 20)
      .attr("height", 20)
      .style("fill", color);

      legend4.append('text')
      .attr("x", 25)
      .attr("y", 15)
      //.attr("dy", ".35em")
      .text(function(d) { return d; })
      .attr("class", "textselected")
      .style("text-anchor", "start")
      .style("font-size", 15)

  // Validacion de BarChart
  function validaJsonBarChart(json_barchart){
      var valores = json_barchart["valores"];

      if(!json_barchart['ejex']){
          alert("Error en la estructura del JSON: Se necesita especificar la unidad");
          return false;
      }

      if(!json_barchart['ejey']){
          alert("Error en la estructura del JSON: Se necesita especificar la unidad");
          return false;
      }

      for(index_valor in valores){
          var llaves_elemento = Object.keys(valores[index_valor]);
          if(!llaves_elemento.some(elem => elem === 'label')){
              alert("Error en la estructura del JSON: El campo label es requerido dentro de los valores. Elemento: " + (parseInt(index_valor) + 1).toString());
              return false;
          }

          for(index_llave in llaves_elemento){
              if(llaves_elemento[index_llave] === 'label'){
                  if(typeof llaves_elemento[index_llave] !== 'string'){
                      alert("Error en la estructura del JSON: El campo label debe ser una cadena");
                      return false;
                  }
              }else{
                  if(typeof valores[index_valor][llaves_elemento[index_llave]] !== 'number'){
                      alert("Error en la estructura del JSON: El campo " + llaves_elemento[index_llave] + " debe ser un numero");
                      return false;
                  }
              }
          }
      }

      return true;
  }




