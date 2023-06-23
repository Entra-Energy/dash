<template>
  <div class="about">
    <div class="row">
      <div class="col-md-12">
          <Range @emit-it="handleChange" />
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="pull-left">
          <Select @emit-sel="selectChange" />
      </div>
    </div>
   </div>
   <div class="row">
      <div class="col-md-12 mb-1">
        <div class="pull-left">
          <button type="submit" class="btn btn-warning" @click="sendIt()" :disabled="isButtonDisabled" >Forecast</button>
          <button type="submit" class="btn btn-warning ml-2" @click="clearIt()" :disabled="isButtonClearDisabled" >Clear</button>
        </div>  
      </div>
    </div>
   <div class='row'><div class='col'><LineCharts :query="query" :forecast="forecast" /></div></div>
   <div class='row'><div class='col'><ReadyChart :query="query" /></div></div>
   <div class='row'><div class='col'><DealSimChart :query="query" /></div></div>
   <div class='row'><div class='col'><PriceChart :query="query" /></div></div>
  



  </div>
</template>
<script>
// @ is an alias to /src
import Range from '@/components/Range.vue'
import Select from '@/components/Select.vue'
import LineCharts from '@/components/LineCharts.vue'
import PriceChart from '@/components/PriceChart.vue'
import ReadyChart from '@/components/ReadyChart.vue'
import DealSimChart from '@/components/DealSimChart.vue'
import axios from 'axios';

export default {
  name: 'About',
  components: {
    Range,
    Select,
    LineCharts,
    PriceChart,
    ReadyChart,
    DealSimChart,  

  },
  data() {
    return {
      dev : {},
      query:{},
      rangeTitle: '',
      forecast: {},
      isButtonDisabled: true,
      isButtonClearDisabled: false,
      intervalId: null,
      intLength:5000

    }
  },
  created() {
    let rangeIndex = this.rangeTitle
    this.forecast.range = rangeIndex
    let path = this.$route.path

    this.$router.push({path:path, query:{"range":rangeIndex}})
    this.checkAPI();
    // this.startAPICheck();
    this.isButtonDisabled = false
    

  },
  beforeDestroy() {
    // Clear the interval when the component is destroyed
    this.stopAPICheck();
  },
  methods: {
    startAPICheck() {
      // Execute the API check function every 5 seconds (adjust the interval as needed)
      this.intervalId = setInterval(this.checkAPI, 5000);
    },
    
    stopAPICheck() {
      // Clear the interval to stop the periodic API check
      clearInterval(this.intervalId);
    },
    checkAPI() {
      
      // Example using Axios
      
      if(this.query.dev){
        let url = 'http://209.38.208.230:8000/api/post_forecast/?date_range=today&dev='+this.query.dev+'F'
        
        axios.get(url)
          .then(response => {            
            
            if(response.data.length == 0)
            {              
              this.isButtonDisabled = false
              this.isButtonClearDisabled = true
            }
            else{
              this.isButtonDisabled = true
              this.isButtonClearDisabled = false
            }
            
          })
          .catch(error => {
            // Handle any errors
            console.error('API error:', error);
          });
        }
    },

    sendIt()
    {
      this.forecast.range = this.query 
      
      this.isButtonDisabled = true
      axios.post('http://209.38.208.230:8000/api/forecast_today/', {       

                "forecast": this.forecast

      }).then(response => {
        
        // this.response = response.data
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })

      
    },

    clearIt()
    {
      this.forecast.range = this.query 
      axios.post('http://209.38.208.230:8000/api/clear_today/', {       

        "clear": this.forecast

        }).then(response => {
        console.log(response);
        // this.response = response.data
        this.success = 'Data saved successfully';
        
        this.response = JSON.stringify(response, null, 2)
        }).catch(error => {
        this.response = 'Error: ' + error.response.status
        })

    },

    handleChange(payload){

      let ran = payload
      //console.log(ran)
      let path = this.$route.path

      this.query["range"] = payload
      //console.log(this.query)
      //
      // //

      //
      //
      // //console.log(this.query)
      this.$router.push({path:path, query:this.query})
      // console.log(this.query)
    //  this.$router.push({path:path, query:{"range":payload.range, "dev": this.dev.dev}})
    //  console.log(payload)
  },
    selectChange(value)
    {
       let path = this.$route.path
      //
      let dev = value
      let range = this.$store.state.path
      this.query["range"] = range

      this.query["dev"] = dev

      // //let query = this.$route.query
      // //this.dev = value
      //
      // console.log(this.query)
      this.$router.push({path:path, query:this.query})
      this.checkAPI()
      //this.$router.push({path:path,query:this.query})

    },
    // resChange(value){
    //   let path = this.$route.path
    //   let resolution = value      
    //   this.query["res"] = resolution
    //   this.$router.push({path:path, query:this.query})      
    // }
  },
  watch: {
    '$store.state.client_init': {
      immediate: true,
      handler() {
          this.rangeTitle = this.$store.state.client_init ;


      }
    }
  },
}
</script>

<style scoped>
.pull-left {
    float: left;
}
</style>
