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

  name: "ArisCharts",
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
                   left: '5%',
                   bottom: '0%',
                   right: '5%',
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
      //  formatter: '{value} BGN'
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
      name: "power",
      smooth: false,
      itemStyle: {
        color: 'rgb(255, 222, 33)'
      },
      //sampling: 'lttb',
      data: [],
      type: 'line',
      showSymbol: false,
      connectNulls: false,
      lineStyle: {
          width: 1
      },

    },
    {
      name: "wind",
      smooth: false,
      itemStyle: {
        color: 'rgb(102,173,62)'
      },
      sampling: 'lttb',
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
       console.log(query_param)
       let end = this.currTime
       let start = this.currDate

       let url = ''
       let url2 = ''
       //console.log(query_param)

         url = "http://64.225.100.195:8000/api/aris/?date_range="+query_param
         //url2 = "http://64.225.100.195:8000/api/price/?timestamp=&start_date="+end
         console.log(url)
         const requestOne = axios.get(url);
         //const requestTwo = axios.get(url2);
         const requestTwo = []

         axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
         const responseOne = responses[0].data
         const responseTwo = responses[1].data
         console.log(responseOne)
         responseOne.forEach((itemFirstRes) => {
           if (query_param == 'today')
           {
             this.option.series[0].data.push([itemFirstRes.timestamp_aris,itemFirstRes.power_aris])

           }
           else{
             this.option.series[0].data.push([itemFirstRes.created,itemFirstRes.power_aris])
           }
         });
         //
         // responseTwo.forEach((itemSecondRes) => {
         //   this.option.series[2].data.push([itemSecondRes.timestamp,itemSecondRes.value])
         // });
         }))
         .catch(errors => {
              // react on errors.
          })
          .finally(() => {
            if(query_param == 'today'){
              this.option.xAxis.axisLabel.formatter = timeLineSet//'{HH}:{mm}'
              this.option.tooltip.formatter =  toolTipSet
              this.option.xAxis.splitNumber = 24
              let endStr = this.currDate.split("T")[0]+"T23:00:00.000Z"
              let endArr = [endStr,null]
              this.option.series[0].data.push(endArr)
            }
            else if(query_param == 'month')
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
                monthLenthArr[2] = this.monthLenth.toString()
                let monthEnd = [monthLenthArr.join("-"),null]


                let monthBegin = [this.currYear+"-"+this.currMonth+"-"+'01',null]
                this.option.series[0].data[0]=monthBegin
                this.option.series[0].data.push(monthEnd)
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
                this.option.series[0].data[0]=yearBegin
                this.option.series[0].data.push(yearEnd)
                this.option.xAxis.splitNumber = 12

            }
          })


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
   this.monthLenth = this.daysInMonth(month,year)
  },
 computed: {

 },
 watch: {
   '$store.state.count': {
     immediate: true,
     handler() {
           this.option.series[0].data = []
           this.option.series[1].data = []
           let path = this.$route.path
           if (path == '/producer')
           {
             let rangeIndex = this.$store.state.producer_init;
             this.param = rangeIndex
           }

           this.getCurrTime();
           this.getData();

        }
   },

   // query: function (val) {
   //
   //   this.param = val
   //   //console.log(val)
   //   this.option.series[0].data = []
   //   this.option.series[1].data = []
   //   this.option.series[2].data = []
   //   //this.getData();
   // },

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
