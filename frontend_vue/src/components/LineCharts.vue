<template>
 <v-chart class="chart" :option="option" />

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
export default {
  name: "LineCharts",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "dark"
  },
  setup () {
   const option = ref({

  tooltip: {

        trigger: 'axis',
        show:true,
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },

  xAxis: {
    type: 'time',
    axisLabel: {
        rotate:40,
        margin:20,
        //formatter: "t",

        textStyle: {
            color: '#fff'
        },

    },
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: "sm-0002",
      data: [],
      type: 'line'
    },
    {
      name: "sm-0007",
      data: [],
      type: 'line'
    }

  ]

   });

   return { option };
 },

 methods: {



     getData() {
     try {
       axios
       .get(
         "http://64.225.100.195/api/posts/?range=0"
       )
       .then(response => response.data.posts.forEach(el=>{

          if (el.devId === "sm-0002")
          {
            this.option.series[0].data.push([el.created_date,el.value])
            this.setTooltip()
            this.option.xAxis.axisLabel.formatter = function(value,index)
            {
              var local = new Date(value)
                                    let min = local.getMinutes()
                                    if(min < 10)
                                    {
                                        min = ("0"+min).slice(-2)
                                    }
                                    let hours = local.getUTCHours()
                                    hours = ("0"+hours).slice(-2)
                                    // if (hours == -2)
                                    // {
                                    //     hours = 0
                                    // }
                                    // if (hours == -1)
                                    // {
                                    //     hours = 23
                                    // }

                                    var texts = hours+":" + min
                                    return texts
            }
            //console.log(el.created_date)
          }
          // if (el.devId === "sm-0007")
          // {
          //   this.option.series[1].data.push([el.created_date,el.value])
          // }

       }
      ))
     } catch (error) {
       //console.log(error);
     }
   },
 },
 created (){
   this.getData();

 },
 computed: {
   setTooltip(){
   this.option.tooltip.formatter = function (params) {

                                        //var chartdate = (new Date(params[0].value[0])).toLocaleTimeString("bg-BG")
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
 }
 },





};
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>
