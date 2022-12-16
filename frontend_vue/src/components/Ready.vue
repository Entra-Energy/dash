<template>
    <div class="card card-chart">
    <div class="card-body">
        <v-chart class="chart" :option="option" style="background-color:#27293d;max-width: 100%; height: 350px" autoresize />
    </div>
  </div>
  
  
  </template>
  
  
  <script>
  import axios from 'axios';
  import { use } from "echarts/core";
  import { CanvasRenderer } from "echarts/renderers";
  import { LineChart } from "echarts/charts";
  import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    DataZoomComponent,
  } from "echarts/components";
  import VChart, { THEME_KEY } from "vue-echarts";
  import { ref, defineComponent } from "vue";
  
  use([
    CanvasRenderer,
    LineChart,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    DataZoomComponent,
  ]);
  
  var toolTipSet = function (params) {
    let chartdate = new Date(params[0].value[0])
    let month = chartdate.getMonth()+1
    month = ("0"+month).slice(-2)
    let day = chartdate.getDate()
    day = ("0"+day).slice(-2)
    let hours  = chartdate.getUTCHours()
    hours = ("0"+hours).slice(-2)
    let mins = chartdate.getMinutes()
    mins = ("0" + mins).slice(-2)
    let formatTime = day+"."+month+"/"+hours+":"+mins
    var vals = params.reduce((prev, curr) => prev + '<li style="list-style:none">' + curr.marker + curr.seriesName + "&nbsp;&nbsp;" + curr.value[1] + "</li>", "");
  
    return formatTime + vals;
    }
  var timeLineSet = function(value,index){
    let local = new Date(value)
    let min = local.getMinutes()
    if(min < 10)
    {
      min = ("0"+min).slice(-2)
    }
    let hours = local.getUTCHours()
  
    //hours = ("0"+hours).slice(-2)
  
    let texts = hours+":"+min
    return texts
  }
  
  export default {
  
    props: {
      query: {
        type: String,
      },
    },
    zoom: {},
    param:'today',
    currTime:'',
    currDate:'',
    currYear:'',
    currMonth:'',
    monthLenth:'',
    dev:'',
  
    name: "Ready",
    components: {
      VChart
    },
    // provide: {
    //   [THEME_KEY]: "dark"
    // },
  
    setup () {
     const option = ref({
    test: '',
    responsive: true,
    maintainAspectRatio: true,
    grid: {
                     left: '10%',
                     bottom: '0%',
                     right: '10%',
                     top: '10%'},
    tooltip: {
  
          trigger: 'axis',
          show:true,
          position: function (pt) {
              return [pt[0], '10%'];
          }
      },
    height: 250,
    xAxis: {
      type: 'time',
      splitNumber: 24,
      axisLabel: {
          rotate:40,
          margin:20,
          //interval: 1,
          //formatter: "t",
  
          textStyle: {
              color: '#9a9a9a'
          },
  
      },
      axisLine: {
        show: true,
  
      },
      splitLine: {
        show: true,
        interval: 24,
        lineStyle: {
          color: '#9a9a9a',
          type: 'dashed',
  
  
        },
  
      },
    },
    yAxis: {
      type: 'value',
      splitLine: {
       show: false
     },
     axisLabel: {
          formatter: '{value}'
        }
      // splitLine: {
      //             lineStyle: {
      //                 color: 'blue'
      //             }
      //         },
    },
    dataZoom: [{
      // bottom: 20,
      // height: 20,
  
      show: false,
  
      start: 0,
      end: 100
    }],
    series: [
    {
      name: "ready",
      smooth: true,
      step: 'middle',
      clip: true,

      itemStyle: {
        color: 'rgb(102,173,62)'
      },
      sampling: 'average',
      data: [],
      type: 'line'
    },
      
    ],
  
    });
  
     return { option };
   },
  
  
   methods: {
  
  
     daysInMonth (month, year) {
         return new Date(year, month, 0).getDate();
     },
  
       getData() {
  
         let query_param = this.param;
         //console.log(query_param)
         let end = this.currTime
         let start = this.currDate
  
         let url = ''
         let url2 = ''
         let devQuery = '&dev=' + this.dev
        if(!this.dev)
        {
            devQuery = ''
        }
         //console.log(query_param)
         if (query_param == 'today'){
           this.option.xAxis.type = 'category'
           this.option.xAxis.axisLabel.formatter = timeLineSet
           this.option.tooltip.formatter =  toolTipSet
           this.option.xAxis.splitNumber = 20
  
           url = "http://64.225.100.195:8000/api/posts/?date_range="+query_param+devQuery//+readyParam"
           url2 = "http://64.225.100.195:8000/api/price/?timestamp=&start_date="+end
           const requestOne = axios.get(url);
           const requestTwo = [];
  
           axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
           const responseOne = responses[0].data
           //const responseTwo = responses[1].data
           console.log(this.option.series)
           responseOne.forEach((itemFirstRes) => {
             this.option.series[0].data.push([itemFirstRes.created_date,itemFirstRes.grid])
           });
           
           }))
           .catch(errors => {
                // react on errors.
            })
         }        
    },
  
     getCurrTime(){
       let date = new Date();
       date.setDate(date.getDate());
       let y = date.getFullYear()
       this.currYear = y
       let thisMonth = date.getMonth()+1
       thisMonth = ('0' + thisMonth).slice(-2);
       this.currMonth = thisMonth
       let toDay = date.getDate()
       toDay = ('0' + toDay).slice(-2);
       let currHour = date.getHours()
       currHour = ('0' + currHour).slice(-2);
       let currMin = ":00:00Z"
       let now = y+"-"+thisMonth+"-"+toDay+"T"+currHour+currMin
       this.currTime = now
       this.currDate = y+"-"+thisMonth+"-"+toDay+"T"+"00:00:00Z"
  
     },
  
  
   },
   created (){
     this.getCurrTime()
     let date = this.currDate.split("T")[0].split("-")
     let year = parseInt(date[0])
     let month = parseInt(date[1])
     console.log(this.param)
     this.monthLenth = this.daysInMonth(month,year)
  
  
  
   },
   computed: {
  
   },
   watch: {
   '$store.state.count': {
     immediate: true,
     handler() {

           this.getCurrTime();
           //this.option.series = []  

           let path = this.$route.path
           if (path == '/client')
           {
             let rangeIndex = this.$store.state.client_init;
             this.param = rangeIndex
             if(this.dev){
             this.getData();
             }
           }

      },
   },
   '$store.state.selected': {
     immediate: true,
     handler() {
       //this.option.series = []     

       

       this.dev = this.$store.state.selected;

       this.getCurrTime();
       let path = this.$route.path
       if (path == '/client')
       {
         //console.log(this.dev)
        
         if(this.dev){
         this.getData();
         }
       }

     }
   },

 }
  
  
  };
  </script>
  
  <style scoped>
  .chart {
    height: 400px;
  }
  .card-chart {
      overflow: hidden;
  }
  .card {
      background: #27293d;
      border: 0;
      position: relative;
      width: 100%;
  
      margin-bottom: 30px;
      -webkit-box-shadow: 0 1px 20px 0 rgb(0 0 0 / 10%);
      box-shadow: 0 1px 20px 0 rgb(0 0 0 / 10%);
  }
  </style>
  