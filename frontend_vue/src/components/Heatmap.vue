<template>
    <vue-google-heatmap :points="points"
                        
                        :height="350"
                        :initial-zoom=8
                        :lat="43.2456"
                        :lng="27.929292"
                        :mapTypeId= 'satellite'                       
                        :options="{maxIntensity: 12,radius:10,saturation: -100,}"
                         />
  </template>

<script>
export default {
  data() {
    return {
      // points: [
      //   {lat: 43.2526052344952, lng:27.909300, weight:6},
      //   {lat: 43.22659389711073, lng:27.95049, weight:7},
      //   {lat: 43.2456, lng:27.929292, weight:8},
      //   {lat: 43.2470, lng:27.929191,weight: 22},
      //   {lat: 43.3001, lng:27.8378,weight: 20},
      //   {lat: 43.3221, lng:27.8888,weight: 19},
      //   {lat: 43.3444, lng:27.8991,weight: 10},
      //   {lat: 43.3333, lng:27.7777,weight: 12},
      //   {lat: 43.1111, lng:27.6565,weight: 12},
      //   {lat: 43.1212, lng:27.6811,weight: 12},
      //   {lat: 43.1111, lng:27.67765,weight: 13},
      //   {lat: 43.3421, lng:27.54556,weight: 12},
      //   {lat: 43.1010, lng:27.65555,weight: 11},
      //   {lat: 43.310, lng:27.65559,weight: 15},
      //   {lat:43.11040803683683, lng:27.541258821652253,weight: 12},
      //   {lat:43.20788385179599, lng:27.79985141137878,weight: 10},
      //   {lat:43.125905319457644,lng: 27.885331473460607,weight: 30},
      //   {lat:43.1455692430971, lng:27.713107379811007,weight: 20},
      //   {lat:43.1455692430971, lng:27.76700063360612,weight: 19},
      //   {lat:43.20452307293171,lng:27.756456301341863,weight: 10},
      //   {lat:43.23355185356251, lng:27.874787141196347,weight: 2},
      //   {lat:43.11564337092553, lng:27.874787141196347,weight: 2},
      //   {lat:43.265126293370855,lng: 27.887674658408216,weight: 5},
      // ],
      all:[],
      points:[]

    }
  },

  created () {  
     
    this.all = this.$store.state.allDevs
     
    },
  watch: {
   '$store.state.allDevs': {
      immediate: true,
      handler() {           
        this.all = this.$store.state.allDevs
        //console.log(this.all)
        this.all.forEach(el=>{
          if(el.lat && el.pow){
          let heatObj = {
            "lat":el.lat,
            "lng":el.long,
            "weight":parseFloat(el.pow)
          }
          this.points.push(heatObj)
        }
        })
        //console.log(this.points)
      },
    }
   },
}
</script>