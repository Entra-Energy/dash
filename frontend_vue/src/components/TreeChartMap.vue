<template>
    <div class="card card-chart">
    <div class="card-body">
        <v-chart class="chart" :option="option" style="background-color:#27293d;max-width: 100%; height: 950px" autoresize />
    </div>
  </div>
  
  
</template>

<script>
import axios from 'axios';
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { TreeChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,  
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent } from "vue";
use([
  CanvasRenderer,
  TreeChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent, 
  
]);

export default {

props: {
  query: {
    type: String,
  },
},

param:'today',
all:[],


name: "TreeChartMap",
components: {
  VChart
},

setup () {
 const option = ref({
test: '',
title: {
 text: 'TreeChart',
 left: 'center',
 padding: [1, 1, 1, 1],
 textStyle: {
    fontSize: 12,
    color:'#dfdfdf'
  },
},
responsive: true,
maintainAspectRatio: true,
tooltip: {
    trigger: 'item',
    triggerOn: 'mousemove'
  },


series: [
  {
      type: 'tree',
      id: 0,
      name: 'tree1',
      data: [{
            name: 'EnergoPro',
            children: [
                          {
                          name: 'GN1',value:0,
                          children: []
                          },
                          {name: 'GN2',
                          children: []           
                          },
                      ]
            }],
      top: '1%',
      left: '8%',
      bottom: '1%',
      right: '20%',
      symbolSize: 17,
      edgeShape: 'polyline',
      edgeForkPosition: '63%',
      initialTreeDepth: 3,
      lineStyle: {
        width: 2
      },
      label: {
        backgroundColor: "none",
        position: 'left',
        verticalAlign: 'bottom',
        align: 'right',
        color: '#fff',
        fontSize:13

      },
      leaves: {
        label: {
          position: 'right',
          verticalAlign: 'middle',
          align: 'left',
          color: 'red'
        }
      },
      emphasis: {
        focus: 'descendant'
      },
      expandAndCollapse: false,
      //animationDuration: 550,
      //animationDurationUpdate: 750
  },
],

});

 return { option };
},


methods: { 

        pollData(){
          this.polling = setInterval(() => {
            //this.option.series[0].data[0].children[0].children = []
            this.getData();
        }, 10000)
      },

       getData() {
      try {
        axios
        .get(
          "http://64.225.100.195:8000/api/online/"
        )
        .then(response => response.data.online.forEach(el=>{
            //this.posts.push(el)
            //console.log(el.dev)
            let found = this.all.find(element => element.id === el.dev)


            if (found)
            {
              found.ready = el.ready
              found.pow = el.pow
              found.providing = el.providing
              found.online = 'online'

              if (found.ready == 1)
              {
                if (found.providing == 0)
                {
                found.online = 'ready'
                }
                else if (found.providing == 1)
                {
                  found.online = 'providing'
                }
              }
              else if (found.ready == 0)
              {
                found.online = 'not-ready'
              }
              else{
                found.online = 'offline'
              }



            }

            //console.log(this.all[0].id)

        }) )

        

      } catch (error) {
        //console.log(error);
      }
      this.treeMap();

      

      
    },

    treeMap(){
      console.log(this.all)
      this.option.series[0].data[0].children[0].children = []
      this.option.series[0].data[0].children[1].children = []
      let GN1Count = 0
      let GN2Count = 0
       this.all.forEach(el=>{
        if(el.online != "offline"){
        switch(el.id){
            case "sm-0001":      
     
            GN1Count += parseFloat(el.pow)
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
            case "sm-0002":
            GN2Count += parseFloat(el.pow)
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
            case "sm-0003":
            GN1Count += parseFloat(el.pow)            
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0004":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0006":
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0007":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0008":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0009":
            GN1Count += parseFloat(el.pow)  
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0010":
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0011":
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0012":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0013":
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0015":
            GN2Count += parseFloat(el.pow) 
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0016":
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0017":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0018":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0019":
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0020":
            GN2Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[1].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0024":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
          case "sm-0025":
            GN1Count += parseFloat(el.pow) 
            this.option.series[0].data[0].children[0].children.push({'name' :el.id +" " + el.pow,'value':el.pow})
            break
        }
        this.option.series[0].data[0].children[0].value = GN1Count
        this.option.series[0].data[0].children[1].value = GN2Count
      }

      })
    }
  

},



created (){

  this.all = this.$store.state.allDevs
  this.pollData();

},
computed: {
  
},
beforeDestroy () {
	   clearInterval(this.polling)
  },

// watch: {
//    '$store.state.allDevs': {
//       immediate: true,
//       handler() {           
//        let all = this.$store.state.allDevs
      
//        let GN1Count = 0
//        all.forEach(el=>{

//         switch(el.id){
//           case "sm-0001":
//             GN1Count += parseFloat(el.pow)
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0002":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0003":
//             GN1Count += parseFloat(el.pow)
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0004":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0006":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0007":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0008":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0009":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0010":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0011":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0012":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0013":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0015":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0016":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0017":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0018":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0019":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0020":
//             this.option.series[0].data[0].children[1].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0024":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//           case "sm-0025":
//             this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})
//             break
//         }
//        })
//        //this.option.series[0].data[0].children[0].children.push({'name':el.id,'value':el.pow})


       
        
//       },
//     }
//    },



};
</script>


<style scoped>
/* .chart {
  height: 400px;
} */
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
