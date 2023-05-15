<template>
  <div class="card card-chart">
  <div class="card-body">
    <div v-if="dataLoader">
      <loader object="#ff9633" color1="#ffffff" color2="#17fd3d" size="5" speed="2" bg="#343a40" objectbg="#999793" opacity="80" name="circular"></loader>
    </div>
    <v-chart class="chart" ref='lineChart' style="background-color:#27293d;max-width: 100%; height: 350px" @mouseover="getDataSubset" @dataZoom="updateZoom" :option="option" autoresize  />
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
var timeLineSetMonth = function(value,index){
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
];
  let local = new Date(value)
  let min = local.getMinutes()
  if(min < 10)
  {
    min = ("0"+min).slice(-2)
  }
  let hours = local.getHours()
  let day = local.getDate()
  //hours = ("0"+hours).slice(-2)
  let year = local.getFullYear()
  let month = monthNames[local.getMonth()]

  let texts = day+"/"+month+'\n'+hours+":00"
  return texts
}


var tooltipDisplay = ""


export default {

  data() {
    return {
      dataLoader:true,
      active: false,
      currPage:1,
      items: [],
    }
  },

  props: {
    query: {
      type: String,
    },
  },

  currTime: '',
  currDate:'',
  currYear: '',
  currMonth: '',
  monthLenthDays:'',
  param:'today',
  nextP:'',
  pageNum:1,
  dev:'',
  myChart: null,
  zoomUpdater:{},
  checked_update: [],
  
  

  name: "LineCharts",
  components: {
    VChart
  },
  // provide: {
  //   [THEME_KEY]: "dark"
  // },

  setup () {
   const option = ref({
  test: '',
  title: {
   text: 'Power',
   left: 'center',
   padding: [1, 1, 1, 1],
   textStyle: {
      fontSize: 12,
      color:'#dfdfdf'
    },
  },
  responsive: true,

  maintainAspectRatio: true,
  grid: {
         left: '10%',
         bottom: '0%',
         right: '10%',
         top: '25%'
        },
  legend: {
          orient: 'vertical',
          padding:[-500,100,0,0],
        },
       
  tooltip: {

        trigger: 'axis',
        //triggerOn: "click",
        show:true,
        formatter : (params) => {
          return tooltipDisplay;
        },
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
  height: 200,

  xAxis: {
    type: 'time',
    //splitNumber: 0,
    axisLabel: {
        rotate:40,
        margin:20,
        //hideOverlap: true,
        //interval: 1,
        //formatter: "t",

        textStyle: {
            color: '#9a9a9a'
        },

    },
    axisLine: {
      show: false,
    },
    splitLine: {
      show: true,
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
        formatter: '{value} kW'
      }
  },


  dataZoom: [{

       bottom: 300,
       height: 20,
       // handleIcon: "pin",
       // handleSize: "75%",
       // handleStyle: {
       //          color: "#9a9a9a",
       //          borderColor: "rgba(255, 255, 255, 1)",
       //          opacity: 0.5
       //  },

       show: true,

       // backgroundColor:'#9a9a9a',
          //  fillerColor: "rgba(255, 255, 255, 0.1)",
           dataBackground: {
                areaStyle: {
                   color: "#9a9a9a"
                       }
                   },
       start: 0,
       end: 100
    },

 ],
  series: [
    
     {
      name: "sm-0001F",
      data: [],
      type: 'line',
      lineStyle:{
        type: 'dotted'
      },
      itemStyle: {
        color: '#d725bb'
      },
      sampling: 'lttb',
    },

  ],



   });

   return { option };
 },


 methods: {        
   

      getDataSubset(params) {

          if(params.seriesType == 'line'){
            if (params.data){
              tooltipDisplay = '<div class="tooltip-set" style="text-align:left; padding:0;margin:0;">' + '<ul style="padding-right:0;padding-left:15px;padding-bottom:0px;margin-bottom:0;">' + '<li>' + params.seriesName + "&nbsp;&nbsp;" + "</li>" + "<li>" + params.data[0] + "</li>" + "<li>" + "Power: "+ params.data[1] + "</li>" + '</ul>' + '</div>'
            }
          }   

      },


      daysInMonth (month, year) {
          return new Date(year, month, 0).getDate();
      },
      updateZoom(e) {

           let start = e.start.toFixed(2)
           let end = e.end.toFixed(2)
           let myZoom = {}
           myZoom.start = start;
           myZoom.end = end;
           this.zoomUpdater = myZoom;
           this.$store.commit('setZoom',myZoom)
           let path = this.$route.path
           if (path == '/dashboard')
           {
             this.$store.commit('dashZoomInit', myZoom)
             console.log(myZoom)
           }
           if (path == '/client')
           {
             this.$store.commit('clientZoomInit', myZoom)
           }
           // if(parseInt(myZoom.end) <= 35)
           // {
           //
           //   this.option.xAxis.splitNumber = 3
           // }
           //console.log(myZoom)
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
      let currMin = date.getMinutes()
      currMin = ('0' + currMin).slice(-2);
      //let currMin = ":00:00Z"
      let now = y+"-"+thisMonth+"-"+toDay+"T"+currHour+":"+currMin
      this.currTime = now
      this.currDate = y+"-"+thisMonth+"-"+toDay+"T"+"00:00:00Z"

    },


    get_data_helper(url,url2){
      
      console.log(url)
      console.log(url2)        
      let test = this.param
      const requestOne = axios.get(url);
     
      let requestTwo = [] 
      if (url2)
      {
        requestTwo = axios.get(url2); 
      }
     
     
      axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
        
        const responseOne = responses[0].data
        
        const responseTwo = responses[1]    
        
        let resObj = Object.keys(responseTwo)
        console.log(resObj)
        if (resObj.length > 0)
        {
          if (responseTwo.data.length > 0)
          {
            responseTwo.data.results.forEach(elm=>{
              
              let found = this.option.series.find(element => element.name === elm.devId)
              
              if (found)
              {
                if (test == 'today')
                {
                  found.data.push([elm.created_date,elm.value])
                }
                else{
                  found.data.push([elm.created,elm.value])
                }
                
              }
            })
          }
        }         
        responseOne.forEach((itemFirstRes) => {           
         
          let found = this.option.series.find(element => element.name === itemFirstRes.devId)              
          if (found)
          {
            // add negative value to the producers              
            let prodCoeff = 1
            if(found.name == "sm-0001" || found.name == "sm-0016")
            {
              prodCoeff = -1
            }
            
            if (test == 'today')
            {
              found.data.push([itemFirstRes.created_date,itemFirstRes.value*prodCoeff])
            }
            else
            {
              found.data.push([itemFirstRes.created,itemFirstRes.value*prodCoeff])
            }
          }
        });
 
        }))     
      
    
          .catch(errors =>  {
                       

           })
          .finally(() => {
            if(test == 'today'){
              this.option.xAxis.axisLabel.formatter = timeLineSet//'{HH}:{mm}'
              //this.option.tooltip.formatter =  toolTipSet
              //this.tooltip.show = false
              this.option.xAxis.splitNumber = 24
              let endStr = this.currDate.split("T")[0]+"T23:00:00.000Z"
              let startForZero = this.currDate.split("T")[0]+"T00:00:00.000Z"    
              //Add zero line
              this.option.series[0] = {
                name: "default",
                data: [[startForZero,0],[endStr,0]],   
                type: 'line',
                itemStyle: {
                  color: '#fbc808'
                },
                lineStyle:{
                  type: 'dotted',
                  width: 1
                },        
              }                
              this.dataLoader = false
              //console.log(this.option.series[0])
              
            }
            else if(test == 'month')
            {
              this.option.xAxis.axisLabel.formatter = {
                day: '{dayStyle|{d}}',
                hour: '{hourStyle|{HH}}'
              }
              this.option.xAxis.axisLabel.rich = {
                hourStyle: {
                  color: '#27293d'
                }
              }
                let monthLenthArr = this.currDate.split("T")[0].split("-")
                monthLenthArr[2] = this.monthLenthDays.toString()
                let monthEnd = [monthLenthArr.join("-"),0]
                let monthBegin = [this.currYear+"-"+this.currMonth+"-"+'01',0]
                //month ZeroLine
                this.option.series[0] = {
                name: "default",
                data: [monthBegin,monthEnd],   
                type: 'line',
                itemStyle: {
                  color: '#fbc808'
                },
                lineStyle:{
                  type: 'dotted',
                  width: 1
                },        
              }                
                // this.option.series[1].data[0]=monthBegin
                // this.option.series[1].data.push(monthEnd)
                this.option.xAxis.splitNumber = 30
                this.dataLoader = false
                
            }
            else {
              this.option.series[1].data[0]
                this.option.xAxis.axisLabel.formatter = {
                  month:'{MMM}',
                  day: '{d}',
                }
                let yearBegin = [this.currYear+"-"+"01"+"-"+"01",0]
                let yearEnd = [this.currYear+"-"+"12"+"-"+"31",0]
                this.option.series[0] = {
                name: "default",
                data: [yearBegin,yearEnd],   
                type: 'line',
                itemStyle: {
                  color: '#fbc808'
                },
                lineStyle:{
                  type: 'dotted',
                  width: 1
                },        
              }  
              
                // this.option.series[1].data[0]=yearBegin
                // this.option.series[1].data.push(yearEnd)
                this.option.xAxis.splitNumber = 12
                this.dataLoader = false

            }        

          })

    // }
     // else {
     //   let monthArrData = this.$store.state.monthData
     //
     //   monthArrData.forEach((itemFirstRes) => {
     //    // console.log(itemFirstRes)
     //     let found = this.option.series.find(element => element.name === itemFirstRes.devId)
     //
     //     if (found)
     //     {
     //       found.data.push([itemFirstRes.created_date,itemFirstRes.value])
     //     }
     //
     //   });
     //   this.option.xAxis.axisLabel.formatter = timeLineSet
     //   let monthLenthArr = this.currDate.split("T")[0].split("-")
     //   monthLenthArr[2] = this.monthLenthDays.toString()
     //   let monthEnd = [monthLenthArr.join("-"),null]
     //
     //
     //   let monthBegin = [this.currYear+"-"+this.currMonth+"-"+'01',null]
     //   this.option.series[1].data[0]=monthBegin
     //   this.option.series[1].data.push(monthEnd)
     //   this.option.xAxis.splitNumber = 30
     //
     // }




    },

     getData() {


       let path = this.$route.path
       if (path == '/dashboard')
       {
         this.dev = ''
       }

       let query_param = this.param;
       

       let end = this.currTime

       let start = this.currDate
       let devQuery = '&dev=' + this.dev
       let devQueryF = '&dev=' + this.dev + 'F'
      
      //  let found = capaLog.find(element => element.name === this.dev)    
      
       
       if(!this.dev)
       {
         devQuery = ''
         devQueryF = ''
       }

       let url = ''
       let url2 = ''
       //let page = "&page="+this.currPage
       //let num = 1

      url = "http://64.225.100.195:8000/api/posts/?date_range="+query_param+devQuery
      if (this.dev){
      url2 = "http://64.225.100.195:8000/api/post_forecast/?date_range="+query_param+devQueryF
      }
      
      this.get_data_helper(url,url2)



   },

 },
 created (){


   this.dataLoader = true
    // let urlMonth = "http://64.225.100.195:8000/api/posts/?date_range=month"
    // let monthData = []
    // axios.get(urlMonth)
    //       .then(response => response.data.forEach(el=>{
    //          monthData.push(el)
    //       }))
    //      .catch(errors => {
    //
    //      }).finally(() => {
    //
    //          this.$store.commit('loadMonthData', Object.freeze(monthData))
    //
    //      });

    this.option.series = []   

    this.getCurrTime()

    let date = this.currDate.split("T")[0].split("-")
    let year = parseInt(date[0])
    let month = parseInt(date[1])
    this.monthLenthDays = this.daysInMonth(month,year)

    //const devs = Object.keys(this.create_devs())
    let devs = this.$store.state.allIds    
    
   
    devs.forEach(item => {
      this.option.series.push(
        {
          "name": item,
          "data": [],
          "type": "line",
          "sampling": "lttb",
          "showSymbol": false,
          "connectNulls": false,
          "lineStyle": {
              "width": 1
          },
          triggerLineEvent: true,
          emphasis: { focus: 'series' }          
        }
      )
    })
  
      
    let path = this.$route.path
    if (path == '/dashboard')
    {
      let zoom = this.$store.state.dash_zoom


      this.option.dataZoom[0].start = zoom.start
      this.option.dataZoom[0].end = zoom.end

    }

    if (path == '/client')
    {
      let zoom = this.$store.state.client_zoom
      this.option.dataZoom[0].start = zoom.start
      this.option.dataZoom[0].end = zoom.end
      this.dataLoader = false;
      // if (this.dev)
      //  {
      //   this.getData();
      //  }

      // this.option.legend.selected = this.create_devs()
      // console.log(this.option.legend.selected)
      // if(this.$store.state.selected) {
      //   this.option.legend.selected[this.$store.state.selected] = true
      // }
    }
    else {
    //  this.option.legend.selected = {}
    }

 },
 destroyed() {

},
 computed: {


 },
 mounted() {

},
 watch: {
   '$store.state.count': {
     immediate: true,
     handler() {

          this.getCurrTime();
          this.option.series = []          
    
          let devs = this.$store.state.allIds            
           devs.forEach((item, i) => {
             this.option.series.push(
               {
                 "name": item,
                 "data": [],
                 "type": "line",
                 "sampling": "lttb",
               }
             )

           });
      let forecastDevs = this.$store.state.allForecastIds
      forecastDevs.forEach(item => {
      
      this.option.series.push(
        {
          "name": item,
          "data": [],
          "type": "line",
          "sampling": "lttb",
          "showSymbol": false,
          "connectNulls": false,
          "lineStyle": {
              "width": 1,
              "type":"dotted"
          },          
        }
      )
    })

           let path = this.$route.path
           if (path == '/dashboard')
           {
             let rangeIndex = this.$store.state.dash_init;
             this.param = rangeIndex
             this.dataLoader = true;
             this.getData();
           }
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
        this.option.series = []
        let startForZero = this.currDate.split("T")[0]+"T00:00:00.000Z"    
        this.option.series[0] = {
          name: "default",
          data: [[startForZero,0]],   
          type: 'line',
          itemStyle: {
            color: '#fbc808'
          },
          lineStyle:{
            type: 'dotted',
            width: 1
          },        
        } 
       let devs = this.$store.state.allIds 
       devs.forEach((item, i) => {
         this.option.series.push(
           {
             "name": item,
             "data": [],
             "type": "line",
             "sampling": "lttb",
           }
         )

       });
      let forecastDevs = this.$store.state.allForecastIds
      forecastDevs.forEach(item => {
      
      this.option.series.push(
        {
          "name": item,
          "data": [],
          "type": "line",
          "sampling": "lttb",
          "showSymbol": false,
          "connectNulls": false,
          "lineStyle": {
              "width": 1,
              "type":"dotted"
          },          
        }
      )
    })

       this.dev = this.$store.state.selected;

       this.getCurrTime();
       let path = this.$route.path
       if (path == '/client')
       {
         //console.log(this.dev)
         if(this.dev){
         this.getData();
         this.dataLoader = true;
         }
       }

     }
   },
   '$store.state.checked_devs': {
     immediate: true,
     handler() {
       //this.checked_update = this.$store.state.checked_devs
       //console.log(this.checked_update)
       let selDevs = this.$store.state.checked_devs
       
       // let selObj = {}
       // //console.log(typeof selDevs)
       // for (const key in selDevs)
       // {
       //   selObj[selDevs[key]] = true
       // }
       this.option.legend.selected = selDevs

       //this.option.legend.selected = selObj
       //console.log(this.option.legend.selected)



     }

   }
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

.tooltip-set ul {    
    text-align: left;
}
</style>
