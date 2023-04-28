<template>

    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <div class='row'><div class='col'><TreeChartMap :query="query" /></div></div> -->
    <div class='row'><div class='col'><Range @emit-it="handleChange"/></div></div>
    <div class='row'><div class='col'><LineCharts :query="query" /></div></div>
    <div class='row'><div class='col'><PriceChart :query="query" /></div></div>
    <div class='row'><div class='col'><Table /></div></div>
    <div class='row'><div class='col'><div id="map"><Heatmap/></div></div></div>


</template>

<script>

// @ is an alias to /src

import Range from '@/components/Range.vue'
import Table from '@/components/Table.vue'
import LineCharts from '@/components/LineCharts.vue'
import PriceChart from '@/components/PriceChart.vue'
import Heatmap from '@/components/Heatmap.vue'
import TreeChartMap from '@/components/TreeChartMap.vue'

export default {
  name: 'Home',
  components: {
    Range,
    Table,
    LineCharts,
    PriceChart,
    Heatmap,
    TreeChartMap
  },
  data() {
    return {
      query:"today",
      rangeTitle:'',

    }
  },
  created (){
    let rangeIndex = this.rangeTitle
    let path = this.$route.path
    //let title = this.$store.state.path

    this.$router.push({path:path, query:{"range":rangeIndex}})


  },

  methods: {
    handleChange(payload){
      //console.log(payload)
      let path = this.$route.path
      this.query = payload
      this.$router.push({path:path, query:{"range":payload}})

    }


  },

  watch: {
    '$store.state.dash_init': {
      immediate: true,
      handler() {
          this.rangeTitle = this.$store.state.dash_init;
      }
    }
  },



}
</script>

<style scoped>

/* #map
{
    filter: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg"><filter id="g"><feColorMatrix type="matrix" values="0.3 0.3 0.3 0 0 0.3 0.3 0.3 0 0 0.3 0.3 0.3 0 0 0 0 0 1 0"/></filter></svg>#g');
    -webkit-filter: grayscale(100%);
    filter: grayscale(100%);    
    filter: progid:DXImageTransform.Microsoft.BasicImage(grayScale=1);
} */
</style>
