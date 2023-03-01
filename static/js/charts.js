function sendJson(){
  var request = new XMLHttpRequest();
  request.open("POST","");

  request.setRequestHeader("Content-type","application/json");
  send_data = {'url': "", 'name': "zhangsan", 'age': 15}
  console.log(JSON.stringify(send_data))
  //xml.send(JSON.stringify(send_data))
  request.send(JSON.stringify(send_data));
}

function fillSelect(){
  var targetYear = document.getElementById("calender_select_year");
  var targetMonth = document.getElementById("calender_select_month");

  var year = ['2016','2017','2018','2019','2020','2021','2022'];
  var month = ['01','02','03','04','05','06','07','08','09','10','11','12'];

  for(var i = 0;i<year.length;i++){
    var mac = document.createElement('option');
    mac.appendChild(document.createTextNode(year[i]))
    targetYear.append(mac);
  }
  for(var i = 0;i<month.length;i++){
    var mac = document.createElement('option');
    mac.appendChild(document.createTextNode(month[i]))
    targetMonth.append(mac);
  }
}

function clearNodes(){
  var root = document.getElementById("click_ul");
  var nodes = root.childNodes;
  for(var i = 1;i<nodes.length;i++){
    root.removeChild(nodes[i]);
  }
  change();
}

function show(){
  if(info_div.style.width != '300px'){
    info_div.style.width  = '300px';
    info_div.style.height = '600px';
    document.getElementById("back").style.display = "block";
    document.getElementById("clear").style.display = "block";
  }
  var li = document.getElementsByClassName("info_li");
    for(var i=0;i<li.length;i++){
      console.log(i);
      li[i].style.display = 'block';
    }
}

function change(){
  if(info_div.style.width == '300px'){
    info_div.style.width  = '25px';
    info_div.style.height = '100px';
    document.getElementById("back").style.display = "none";
    document.getElementById("clear").style.display = "none";
    var li = document.getElementsByClassName("info_li");
    for(var i=0;i<li.length;i++){
      console.log(i);
      li[i].style.display = 'none';
    }
  }else{
    info_div.style.width  = '300px';
    info_div.style.height = '600px';
    document.getElementById("back").style.display = "block";
    document.getElementById("clear").style.display = "block";
    var li = document.getElementsByClassName("info_li");
    for(var i=0;i<li.length;i++){
      console.log(i);
      li[i].style.display = 'block';
    }
  }
}

const layouts = [
  [[0, 0]],
  [
    [-0.25, 0],
    [0.25, 0]
  ],
  [
    [0, -0.2],
    [-0.2, 0.2],
    [0.2, 0.2]
  ],
  [
    [-0.25, -0.25],
    [0.25, -0.25],
    [-0.25, 0.25],
    [0.25, 0.25]
  ]
];
const pathes = [
  "M827.392 195.584q65.536 65.536 97.792 147.456t32.256 167.936-32.256 167.936-97.792 147.456-147.456 98.304-167.936 32.768-168.448-32.768-147.968-98.304-98.304-147.456-32.768-167.936 32.768-167.936 98.304-147.456 147.968-97.792 168.448-32.256 167.936 32.256 147.456 97.792zM720.896 715.776q21.504-21.504 18.944-49.152t-24.064-49.152l-107.52-107.52 107.52-107.52q21.504-21.504 24.064-49.152t-18.944-49.152-51.712-21.504-51.712 21.504l-107.52 106.496-104.448-104.448q-21.504-20.48-49.152-23.04t-49.152 17.92q-21.504 21.504-21.504 52.224t21.504 52.224l104.448 104.448-104.448 104.448q-21.504 21.504-21.504 51.712t21.504 51.712 49.152 18.944 49.152-24.064l104.448-104.448 107.52 107.52q21.504 21.504 51.712 21.504t51.712-21.504z",
  "M511.999994 0C229.205543 0 0.020822 229.226376 0.020822 512.020827c0 282.752797 229.184721 511.979173 511.979173 511.979173s511.979173-229.226376 511.979173-511.979173C1023.979167 229.226376 794.794446 0 511.999994 0zM815.371918 318.95082l-346.651263 461.201969c-10.830249 14.370907-27.32555 23.409999-45.27877 24.742952-1.582882 0.124964-3.12411 0.166619-4.665338 0.166619-16.328682 0-32.074198-6.373185-43.779197-17.911565l-192.903389-189.44604c-24.617988-24.20144-24.992881-63.731847-0.791441-88.349835 24.20144-24.659643 63.731847-24.951226 88.349835-0.833096l142.042875 139.501932 303.788472-404.2182c20.744091-27.575479 59.899605-33.115568 87.516739-12.413131C830.534266 252.219827 836.116009 291.375341 815.371918 318.95082z"
  
];
const colors = ['#c4332b','#16B644'];
const infoList = ['上午签到','上午签退','下午签到','下午签退'];

function getVirtulData(year) {
  let date = +echarts.number.parseDate(year + '-01-01');
  let end = +echarts.number.parseDate(+year + 1 + '-01-01');
  let dayTime = 3600 * 24 * 1000;
  let data = [];
  for (let time = date; time < end; time += dayTime) {
    let items = [];
    let eventCount = 4;
    for (let i = 0; i < eventCount; i++) {
      items.push(Math.round(Math.random() * (pathes.length - 1)));
    }
    data.push([echarts.format.formatTime('yyyy-MM-dd', time), items.join('|'),{"0":"去把老板挂路灯了，晚上回来"}]);
  }
  return data;
}

//需要输入考勤信息，[bool,bool,bool,bool]分别对应上午签到，上午签退，下午签到，下午签退，晚上加班掉路灯
function calender(){
  var chartDom = document.getElementById('calendar_echart');
  var myChart = echarts.init(chartDom);
  var option;

  var rangeYear = document.getElementById("calender_select_year").value;
  var rangeMonth = document.getElementById("calender_select_month").value;

  option = {
    tooltip: {
      position: 'top',
      formatter: function (p) {
        //var format = echarts.format.formatTime('yyyy-MM-dd', p.data[0]);
        return "点击查看";
      }
    },
    calendar: [
      {
        left: 'center',
        top: 'middle',
        cellSize: [70, 70],
        yearLabel: { show: false },
        orient: 'vertical',
        dayLabel: {
          firstDay: 1,
          nameMap: 'cn'
        },
        monthLabel: {
          show: false
        },
        range: rangeYear+"-"+rangeMonth
      }
    ],
    series: [
      {
        type: 'custom',
        coordinateSystem: 'calendar',
        renderItem: function (params, api) {
          const cellPoint = api.coord(api.value(0));
          const cellWidth = params.coordSys.cellWidth;
          const cellHeight = params.coordSys.cellHeight;
          const value = api.value(1);
          const events = value && value.split('|');
          if (isNaN(cellPoint[0]) || isNaN(cellPoint[1])) {
            return;
          }
          const group = {
            type: 'group',
            children:
              (layouts[events.length - 1] || []).map(function (
                itemLayout,
                index
              ) {
                return {
                  type: 'path',
                  name: echarts.format.formatTime('yyyy-MM-dd', api.value(0))+"-"+infoList[index],
                  shape: {
                    pathData: pathes[+events[index]],
                    x: -8,
                    y: -8,
                    width: 16,
                    height: 16
                  },
                  position: [
                    cellPoint[0] +
                      echarts.number.linearMap(
                        itemLayout[0],
                        [-0.5, 0.5],
                        [-cellWidth / 2, cellWidth / 2]
                      ),
                    cellPoint[1] +
                      echarts.number.linearMap(
                        itemLayout[1],
                        [-0.5, 0.5],
                        [-cellHeight / 2 + 20, cellHeight / 2]
                      )
                  ],
                  style: api.style({
                    fill: colors[+events[index]]
                  })
                };
              }) || []
          };
          group.children.push({
            type: 'text',
            style: {
              x: cellPoint[0],
              y: cellPoint[1] - cellHeight / 2 + 10,
              text: echarts.format.formatTime('dd', api.value(0)),
              fill: '#777',
              textFont: api.font({ fontSize: 14 })
            }
          });
          return group;
        },
        dimensions: [undefined, { type: 'ordinal' }],
        data: getVirtulData(rangeYear)
      }
    ]
  };
  myChart.setOption(option);
  //设置点击事件
  myChart.on('click',function(params){
    console.log(params)
    var ul = document.getElementById("click_ul");
    
    //let data = params.data[1].split('|');
    let target = params.event.target.name+":\n"+params.data[2][0];
    
    //ul.appendChild
    var li = document.createElement("li");
    li.setAttribute("class","info_li");
    li.setAttribute("display","info_li");
    li.appendChild(document.createTextNode(target));
    ul.append(li);

    show();
  });
}

/*
function getVirtulData(year) {
  year = year || '2016';
  var date = +echarts.number.parseDate(year + '-01-01');
  var end = +echarts.number.parseDate(+year + '-02-01');
  var dayTime = 3600 * 24 * 1000;
  var data = [];
  for (var time = date; time < end; time += dayTime) {
    data.push([
      echarts.format.formatTime('yyyy-MM-dd', time),
      Math.floor((Math.random() * 100)%5)
    ]);
  }

  return data;
}

function calendar(){
  var chartDom = document.getElementById('calendar_echart');
  var myChart = echarts.init(chartDom);
  var option; 
    option = {
        title: {
          top: 30,
          left: 'center',
          text: 'Daily Step Count'
        },
        tooltip: {
          position: 'top',
          formatter: function (p) {
            var format = echarts.format.formatTime('yyyy-MM-dd', p.data[0]);
            return format + ': ' + p.data[1];
          }
        },
        visualMap: {
          min: 0,
          max: 4,
          type: 'piecewise',
          orient: 'horizontal',
          left: 'center',
          top: 65,
          inRange: {
            // 渐变颜色，从小到大
            color: [ '#bacae8', '#96b5ef', '#6797ef', '#3375e4']//, '#035cf5'//'#d1d4da',
         }
        },
        calendar: {
          top: 120,
          left: 30,
          right: 30,
          orient: 'vertical',
          cellSize: ['auto', 13],
          range: '2016-01',
          itemStyle: {
            borderWidth: 0.5
          },
          yearLabel: { show: false }
        },
        series: [{
          type: 'heatmap',
          coordinateSystem: 'calendar',
          dimensions:['name','value'],
          data: getVirtulData('2016')
        }]
      };
      
      myChart.setOption(option);

      //设置点击事件
      myChart.on('click',function(params){
        console.log(params);
        var ul = document.getElementById("click_ul");
        //ul.appendChild
      });
}
*/