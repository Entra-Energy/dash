<template>
    <div class="card card-chart">
    <div class="card-body">
        <v-chart class="chart" :option="option" style="background-color:#27293d;max-width: 100%; height: 650px" autoresize />
    </div>
  </div>
  
  
</template>

<script>
import axios from 'axios';
import { helper, use } from "echarts/core";
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
polling: null,
//apiResponse: [],


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
    fontSize: 16,
    color:'white'
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
                          // {
                          // name: 'GN1',value:0,
                          // children: []
                          // },
                          // {name: 'GN2',
                          // children: []           
                          // },
                      ]
            }],
      top: '25%',
      left: '8%',
      bottom: '25%',
      right: '20%',
      symbolSize: 12,
      edgeShape: 'polyline',
      edgeForkPosition: '70%',
      initialTreeDepth: 3,
      lineStyle: {
        width: 2,
        color: '#e07c58'
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
          color: '#FFF'
        }
      },
      emphasis: {
        focus: 'descendant'
      },
      expandAndCollapse: false,

  },
],

});

 return { option };
},
data() {
    return {
      apiResponse:[],
      apiAsignAll:[]
    };
  },


methods: { 

        pollData(){
          this.polling = setInterval(() => {
            this.option.series[0].data[0].children = []
            this.getData();
        }, 30000)
      },

       getData() {
      
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
        }) )
        .catch(error=>{
          console.log(error)
        })
        .finally(() => {
          this.fetchAsignApi()
        })

    },
    fetchAsignApi(){
      axios
          .get("http://64.225.100.195:8000/api/grid_asign/")
          .then(response =>{          
            this.apiAsignAll = response.data.results
            const distinctValues = [...new Set(response.data.results.map(item => item.grid_name))];            
            this.apiResponse = distinctValues; 
          })
          .catch(error=>{
            console.log(error)
          })
          .finally(()=>{
            this.treeMap()
          })      
    },

    treeMap(){ 
      this.apiResponse.forEach(el=>{
        let obj = {
          'name':el,'value':0,"children":[]
        }
        this.option.series[0].data[0].children.push(obj)
      })
        let helperArr = []
        this.apiAsignAll.forEach(el=>{
          this.all.forEach(elm=>{
            if(el.dev === elm.id){
              let test = {
                "id":el.dev,
                "node":el.grid_name,
                "pow":elm.pow
              }
              helperArr.push(test)              
            }
          })
        
        })
        console.log(helperArr)
       
        let graphArr = this.option.series[0].data[0].children        

        helperArr.forEach(em=>{
          graphArr.forEach(it=>{
            if(it.name === em.node )
            {
              
              let childOb = {
                "name":em.id+" | "+ em.pow +" kW",
                "value":em.pow
              }
              it.children.push(childOb)  
                              
            }
          })        
        })
        let result = helperArr.reduce((acc, curr) => {
        let item = acc.find(item => item.node === curr.node);

        if (item) {
          item.pow += curr.pow;
        } else {
          acc.push(curr);
        }

        return acc;
      }, []);
      graphArr.forEach((gr) => {
        const res = result.find((r) => r.node === gr.name)
        if (res) {
          gr.value = res.pow
          gr.name = gr.name + " | " + res.pow + " kW" 
        }
      })
      // graphArr.forEach(gr=>{
      //   result.forEach(res=>{
      //     if(gr.name === res.node){
      //       gr.value = res.pow
      //     }
      //   })
      
      // })

      }
  

},



created (){
 
  this.all = this.$store.state.allDevs
  //this.fetchAsignApi();
  this.getData()
  this.pollData();

},
computed: {
  
},
beforeDestroy () {
	   clearInterval(this.polling)
  },




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
