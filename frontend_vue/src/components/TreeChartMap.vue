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
            this.all=[]
            this.all = this.$store.state.allDevs
            this.getData();
        }, 30000)
      },

       getData() {
      
        axios
        .get(
          "http://209.38.208.230:8000/api/online/"
        )
        .then(response => response.data.online.forEach(el=>{

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
    async fetchAsignApi() {
      try {
        const response = await axios.get("http://209.38.208.230:8000/api/grid_asign/");
        this.apiAsignAll = response.data;        
        const distinctValues = [...new Set(response.data.map(item => item.grid_name))];
        this.apiResponse = distinctValues;
      } catch (error) {
          console.log(error);
      } finally {
          this.treeMap();
      }
    },
    treeMap() {
      const graphArr = this.option.series[0].data[0].children;

      this.apiResponse.forEach(el => {
        const obj = {
          name: el,
          value: 0,
          children: []
        };
        graphArr.push(obj);
      });

      const helperArr = [];
      this.apiAsignAll.forEach(el => {
        this.all.forEach(elm => {
          if (elm.online !== 'offline' && el.dev === elm.id) {
            let pow = parseFloat(elm.pow);
            if (el.dev === "sm-0016") {
              pow = -pow;
            }
            const sm_data = {
              id: el.dev,
              node: el.grid_name,
              pow: pow
            };
            helperArr.push(sm_data);
          }
        });
      });

      const result = [];
      helperArr.forEach(em => {
        const node = em.node;
        const pow = em.pow;
        const existingNode = result.find(element => element.node === node);
        if (existingNode) {
          existingNode.pow += pow;
        } else {
          result.push({ node, pow });
        }
        graphArr.forEach(it => {
          if (it.name === em.node) {
            const childOb = {
              name: em.id + " | " + em.pow + " kW",
              value: em.pow
            };
            it.children.push(childOb);
          }
        });
      });

  graphArr.forEach(gr => {
    const node = result.find(element => element.node === gr.name);
    if (node) {
      gr.value = node.pow.toFixed(2);
      gr.name = gr.name + " | " + gr.value + " kW";
    }
  });
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
