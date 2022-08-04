<template>
  <div class="card card-chart">
  <div class="card-body">
    <v-chart class="chart" ref='lineChart' style="background-color:#27293d;max-width: 100%; height: 350px" :option="option" autoresize />
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

export default {

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
  dev:'',
  name: "ReadyChart",
  components: {
    VChart
  },
  setup () {
   const option = ref({
   title: {
   text: 'Grid Ready/ Not Ready',
   left: 'left',
   color:'#fff'
  },
  test: '',
  responsive: true,

  maintainAspectRatio: true,
  grid: {
         left: '5%',
         bottom: '0%',
         right: '5%',
         top: '25%'
        },
  legend: {
        orient: 'vertical',
        padding:[-500,100,0,0],
        //data: ['sm-0009','sm-0001'],
        selected:{'sm-0001':true,'sm-0009':true, 'sm-0002':true,'sm-0003':true,'sm-0004':true,'sm-0000':true,'sm-00011':true,'sm-00012':true},
     },
  tooltip: {

        trigger: 'axis',
        show:true,
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
   boundaryGap: [0, '800%'],
   axisLabel: {
        formatter: ''
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
    // {
    //   name: "sm-0009",
    //   data: [],
    //   type: 'line',
    //   itemStyle: {
    //     color: '#d725bb'
    //   },
    //   sampling: 'lttb',
    // },
    // {
    //   name: "sm-0009F",
    //   data: [],
    //   type: 'line',
    //   lineStyle:{
    //     type: 'dotted'
    //   },
    //   itemStyle: {
    //     color: '#d725bb'
    //   },
    //   sampling: 'lttb',
    // },

  ],

   });

   return { option };
 },
 methods: {

   daysInMonth (month, year) {
       return new Date(year, month, 0).getDate();
   },
   create_devs(){
     let dev = 'sm-000'
     let all_devs = {}
     for(let i = 0; i <= 12; i++)
     {
       let new_dev = dev+i;
       all_devs[new_dev] = false
     }
     return all_devs
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
     const requestOne = axios.get(url);
     console.log(url)
     const requestTwo = []
     let test = this.param
     axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
       const responseOne = responses[0].data
       responseOne.forEach((itemFirstRes) => {
          let found = this.option.series.find(element => element.name === itemFirstRes.devId)

          if (found)
          {
            if (test == 'today')
            {
              found.data.push([itemFirstRes.created_date,itemFirstRes.grid])
            }
            else
            {
              found.data.push([itemFirstRes.created,itemFirstRes.grid])
            }
          }

        });


        }))
        .catch(errors => {

         })
         .finally(() => {
           if(test == 'today'){
             this.option.xAxis.axisLabel.formatter = timeLineSet//'{HH}:{mm}'
             this.option.tooltip.formatter =  toolTipSet
             this.option.xAxis.splitNumber = 24
             let endStr = this.currDate.split("T")[0]+"T23:00:00.000Z"
             let endArr = [endStr,null]
             this.option.series[1].data.push(endArr)
           }
           else if(test == 'month')
           {
               this.option.xAxis.axisLabel.formatter = {
                 day: '{dayStyle|{d}}',
                 hour: '{hourStyle|{HH}}'
               }
               this.option.xAxis.axisLabel.rich = {
                 // dayStyle: {
                 //   color: '#fff'
                 // },
                 hourStyle: {
                   color: '#27293d'
                 }
               }

               let monthLenthArr = this.currDate.split("T")[0].split("-")
               monthLenthArr[2] = this.monthLenthDays.toString()
               let monthEnd = [monthLenthArr.join("-"),null]


               let monthBegin = [this.currYear+"-"+this.currMonth+"-"+'01',null]
               this.option.series[1].data[0]=monthBegin
               this.option.series[1].data.push(monthEnd)
               this.option.xAxis.splitNumber = 30
               //console.log(this.option.series[1].data)
           }
           else {
               this.option.xAxis.axisLabel.formatter = {
                 month:'{MMM}',
                 day: '{d}',
               }

               let yearBegin = [this.currYear+"-"+"01"+"-"+"01"]
               let yearEnd = [this.currYear+"-"+"12"+"-"+"31"]
               this.option.series[1].data[0]=yearBegin
               this.option.series[1].data.push(yearEnd)
               this.option.xAxis.splitNumber = 12

           }

           //console.log(this.nextP)
           // if(this.nextP)
           // {
           //   console.log(this.nextP)
           //   let url2 = ""
           //   this.get_data_helper(this.nextP,url2)
           // }
           // else{
           //
           // }

         })





    },

    getData() {
      let query_param = this.param;
      let end = this.currTime

      let start = this.currDate
      let devQuery = '&dev=' + this.dev
      if(!this.dev)
      {
        devQuery = ''
      }
      let url = ''
      let url2 = ''
      let readyParam = '&ready=1'
      //let page = "&page="
      //let num = 1

     url = "http://64.225.100.195:8000/api/posts/?date_range="+query_param+devQuery//+readyParam
     url2 = "http://64.225.100.195:8000/api/posts/?created_date=&start_date="+end
     this.get_data_helper(url,url2)
   },

 },

 created (){
    this.option.series = []
    this.getCurrTime()

    let date = this.currDate.split("T")[0].split("-")
    let year = parseInt(date[0])
    let month = parseInt(date[1])
    this.monthLenthDays = this.daysInMonth(month,year)

    const devs = Object.keys(this.create_devs())
    devs.forEach((item, i) => {
      this.option.series.push(
        {
          "name": item,
          "data": [],
          "type": "line",
          "sampling": "lttb",
          "showSymbol": false,
          "connectNulls": false,
          "areaStyle": {
            "color": "#28a745"
    }

        }
      )

    });

 },

 watch: {
   '$store.state.count': {
     immediate: true,
     handler() {

           this.getCurrTime();
           this.option.series = []
           const devs = Object.keys(this.create_devs())
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
       this.option.series = []
       const devs = Object.keys(this.create_devs())
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

       this.dev = this.$store.state.selected;

       this.getCurrTime();
       let path = this.$route.path
       if (path == '/client')
       {
         console.log(this.dev)
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
