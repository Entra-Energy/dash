<template>
  <div class="card card-chart">
  <div class="card-body">
    <v-chart class="chart" ref='lineChart' style="background-color:#27293d;max-width: 100%; height: 350px" @dataZoom="updateZoom" :option="option" autoresize />
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

  let texts = hours+":00"
  return texts
}


export default {

  props: {
    query: {
      type: String,
    },
  },
  currTime: '',
  currDate:'',
  param:'today',
  myChart: null,
  zoomUpdater:{},

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
  responsive: true,
  maintainAspectRatio: true,
  grid: {
         left: '5%',
         bottom: '0%',
         right: '5%',
         top: '25%'
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
    splitNumber: 0,
    axisLabel: {
        rotate:40,
        margin:20,
        interval: 1,
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
      name: "sm-0009",
      data: [],
      type: 'line',
      itemStyle: {
        color: '#d725bb'
      },
      sampling: 'lttb',
    },
    {
      name: "sm-0009F",
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

 //   myEventHandler(e) {
 //
 //   console.log(e)
 // },
  //


     updateZoom(e) {

           var start = e.start.toFixed(2)
           var end = e.end.toFixed(2)
           var myZoom = {}
           myZoom.start = start;
           myZoom.end = end;
           this.zoomUpdater = myZoom;
           this.$store.commit('setZoom',myZoom)
           //console.log(myZoom)
    },

    getCurrTime(){
      let date = new Date();
      date.setDate(date.getDate());
      let y = date.getFullYear()
      let thisMonth = date.getMonth()+1
      thisMonth = ('0' + thisMonth).slice(-2);
      let toDay = date.getDate()
      toDay = ('0' + toDay).slice(-2);
      let currHour = date.getHours()
      currHour = ('0' + currHour).slice(-2);
      let currMin = ":00:00Z"
      let now = y+"-"+thisMonth+"-"+toDay+"T"+currHour+currMin
      this.currTime = now
      this.currDate = y+"-"+thisMonth+"-"+toDay+"T"+"00:00:00Z"

    },

     getData() {

       let query_param = this.param;
       console.log(query_param)
       let end = this.currTime
       let start = this.currDate


       let url = ''
       let url2 = ''
       if (query_param == 'today'){

         this.option.xAxis.axisLabel.formatter = '{HH}'
         this.option.tooltip.formatter =  toolTipSet

        // this.option.xAxis.splitNumber = 22
         url = "http://64.225.100.195:8000/api/posts/?created_date=&start_date="+start+"&end_date="+end//+"&date_range="+query_param
         url2 = "http://64.225.100.195:8000/api/posts/?created_date=&start_date="+end
         const requestOne = axios.get(url);
         const requestTwo = axios.get(url2);
         console.log(url,url2)
         axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
         const responseOne = responses[0].data
         const responseTwo = responses[1].data
         responseOne.forEach((itemFirstRes) => {
           if (itemFirstRes.devId === "sm-0009"){
             this.option.series[0].data.push([itemFirstRes.created_date,itemFirstRes.value])
             console.log(itemFirstRes.created_date)
             this.option.xAxis.axisLabel.formatter = timeLineSet
           }

         });
         responseTwo.forEach((itemSecondRes) => {
           if (itemSecondRes.devId === "sm-0009F-FF"){

           this.option.series[1].data.push([itemSecondRes.created_date,itemSecondRes.value])
         }
         });
         })).catch(errors => {
              // react on errors.
          })
       }
       else {
         if (query_param == 'month')
         {
           this.option.xAxis.axisLabel.formatter =  '{dd}'
         }
         else {
           this.option.xAxis.axisLabel.formatter =  '{MMM}'
         }
         //this.option.xAxis.splitNumber = 31

         url = "http://64.225.100.195:8000/api/posts/?timestamp=&date_range="+query_param
         console.log(url)

         try {
           axios
           .get(
             url

           )
           .then(response => response.data.forEach(el=>{

             if(el.devId=='sm-0009')
             {
               this.option.series[0].data.push([el.created_date,el.value])
             }
          }
        ))
      } catch (error) {
       //console.log(error);
     }
    }







    //    let url = "http://127.0.0.1:8000/api/posts/?created_date=&date_range="+query_param
    //    try {
    //      axios
    //      .get(url)
    //      .then(response => response.data.forEach(el=>{
    //       if (el.devId === "sm-0009")
    //       {
    //         this.option.series[0].data.push([el.created_date,el.value])
    //         this.option.tooltip.formatter =  toolTipSet
    //
    //       }
    //       // if (el.devId === "sm-0007")
    //       // {
    //       //   this.option.series[1].data.push([el.created_date,el.value])
    //       // }
    //    }
    // ))
    //
    //  } catch (error) {
    //    //console.log(error);
    //  }
    //  //this.option.xAxis.axisLabel.formatter = timeLineSet
    //  this.option.tooltip.formatter =  toolTipSet

     // let startStr =["2022-03-24T00:00:00.000Z",null]
     // this.option.series[0].data[0] = startStr
     // let endStr = "2022-03-24T23:00:00.000Z"
     // let time = [endStr,null]
     // this.option.series[0].data.push(time)
     //let timeBegin = [startStr,null]
     //this.option.series[0].data.unshift(startStr)
     //console.log(this.option.series[0].data)

   },

 },
 created (){


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
           // update locally relevant data
          let rangeIndex = this.$store.state.count;

           if(rangeIndex == 0){
            this.param = 'today'
           }
           if(rangeIndex == 1)
           {
             this.param = 'month'
           }
           if(rangeIndex == 2)
           {
             this.param = 'year'
           }
           this.option.series[0].data = []
           this.option.series[1].data = []
           //console.log(this.option.xAxis.axisLabel.formatter)
           //this.option1.tooltip.formatter = ''
           //this.option.series[2].data = []

           this.getCurrTime();
           this.getData();

           //console.log(this.param)


      },
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
