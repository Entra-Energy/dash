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
        selected:{'sm-0001':true,'sm-0002':true,'sm-0003':true,'sm-0004':true,'sm-0005':true,'sm-0006':true,'sm-0007':true,'sm-0008':true,'sm-0009':true,'sm-00010':true},
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

 //   myEventHandler(e) {
 //
 //   console.log(e)
 // },
  //

    create_devs(){
      let dev = 'sm-000'
      let all_devs = {}
      for(let i = 0; i <= 10; i++)
      {
        let new_dev = dev+i;
        all_devs[new_dev] = false
      }
      return all_devs
    },


     updateZoom(e) {

           let start = e.start.toFixed(2)
           let end = e.end.toFixed(2)
           let myZoom = {}
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
      let currMin = date.getMinutes()
      currMin = ('0' + currMin).slice(-2);
      //let currMin = ":00:00Z"
      let now = y+"-"+thisMonth+"-"+toDay+"T"+currHour+":"+currMin
      this.currTime = now
      this.currDate = y+"-"+thisMonth+"-"+toDay+"T"+"00:00:00Z"

    },

     get_data_helper(url,url2){
       const requestOne = axios.get(url);
       const requestTwo = axios.get(url2);
       let test = this.param
       if(test == 'today')
       {
         this.option.xAxis.axisLabel.formatter = timeLineSet
         this.option.tooltip.formatter =  toolTipSet
       }
       else if (test == 'month')
       {
         this.option.xAxis.axisLabel.formatter =  '{dd}'
       }
       else {
         this.option.xAxis.axisLabel.formatter =  '{MMM}'
       }

       axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
          const responseOne = responses[0].data
          const responseTwo = responses[1].data
          responseOne.forEach((itemFirstRes) => {
            let found = this.option.series.find(element => element.name === itemFirstRes.devId)
            if (found)
            {
              found.data.push([itemFirstRes.created_date,itemFirstRes.value])
            }

          });
          // responseTwo.forEach((itemSecondRes) => {
          //
          //   if (itemSecondRes.devId === "sm-0009F"){
          //
          // }
          // });
          })).catch(errors => {
               // react on errors.
           })
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
       if(!this.dev)
       {
         devQuery = ''
       }
       let url = ''
       let url2 = ''


      url = "http://64.225.100.195:8000/api/posts/?date_range="+query_param+devQuery
      url2 = "http://64.225.100.195:8000/api/posts/?created_date=&start_date="+end
      this.get_data_helper(url,url2)

    //    if (query_param == 'today'){
    //
    //      this.option.xAxis.axisLabel.formatter = timeLineSet
    //      this.option.tooltip.formatter =  toolTipSet
    //
    //     // this.option.xAxis.splitNumber = 22
    //      url = "http://64.225.100.195:8000/api/posts/?created_date=&start_date="+start+"&end_date="+end+devQuery
    //      url2 = "http://64.225.100.195:8000/api/posts/?created_date=&start_date="+end
    //      console.log(url)
    //      const requestOne = axios.get(url);
    //      const requestTwo = axios.get(url2);
    //      axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
    //      const responseOne = responses[0].data
    //      const responseTwo = responses[1].data
    //      responseOne.forEach((itemFirstRes) => {
    //        let found = this.option.series.find(element => element.name === itemFirstRes.devId)
    //        if (found)
    //        {
    //          found.data.push([itemFirstRes.created_date,itemFirstRes.value])
    //        }
    //
    //      });
    //      responseTwo.forEach((itemSecondRes) => {
    //
    //        if (itemSecondRes.devId === "sm-0009F"){
    //
    //      }
    //      });
    //      })).catch(errors => {
    //           // react on errors.
    //       })
    //    }
    //    else {
    //      if (query_param == 'month')
    //      {
    //       // this.option.xAxis.axisLabel.formatter =  '{dd}'
    //      }
    //      else {
    //       // this.option.xAxis.axisLabel.formatter =  '{MMM}'
    //      }
    //      //this.option.xAxis.splitNumber = 31
    //
    //      url = "http://64.225.100.195:8000/api/posts/?timestamp=&date_range="+query_param
    //      console.log(query_param)
    //
    //      try {
    //        axios
    //        .get(
    //          url
    //
    //        )
    //        .then(response => response.data.forEach(el=>{
    //
    //          if(el.devId=='sm-0009')
    //          {
    //           // this.option.series[0].data.push([el.created_date,el.value])
    //          }
    //       }
    //     ))
    //   } catch (error) {
    //    //console.log(error);
    //  }
    // }


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
    this.option.series = []

    this.getCurrTime()

    const devs = Object.keys(this.create_devs())
    devs.forEach((item, i) => {
      this.option.series.push(
        {
          "name": item,
          "data": [],
          "type": "line",
          "sampling": "lttb",
          "showSymbol": false,
          //"sampling": "average"
        }
      )

    });


    let path = this.$route.path
    if (path == '/dashboard')
    {
    //  this.getData();
    }

    if (path == '/client')
    {

       if (this.dev)
       {
        // this.getData();
       }

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
          // this.option.series[0].data = []
        //   this.option.series[1].data = []
           //console.log(this.option.xAxis.axisLabel.formatter)
           //this.option1.tooltip.formatter = ''
           //this.option.series[2].data = []

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
           console.log("click")
           let path = this.$route.path
           if (path == '/dashboard')
           {
            this.getData();
           }
           if (path == '/client')
           {
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
         if(this.dev){
         this.getData();
         }
       }

       //
       // this.option.legend.selected = this.create_devs()
       // this.option.legend.selected[this.dev] = true
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
       console.log(selDevs)
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
</style>
