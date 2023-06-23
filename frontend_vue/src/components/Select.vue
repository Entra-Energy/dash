<template>
  <div class="row">
  <label for="client" class="form-label ml-2 mr-2 sel-label" >Select Client: </label>
  <select id="client" class="form-select form-select-lg mb-3" aria-label=".form-select-lg" v-model="selected" @change="onChange($event)" >
    <option v-for="option in options" v-bind:value="option.value">
      {{option.value}}/{{ option.text }}
    </option>
  </select>
  </div>
  <!-- <p class="blynk-name">{{  }}</p> -->
  <div class="row">
    <label for="smootSlider" class="form-label ml-2 mr-2 sl-label">Smooth Level: </label>
    <input id="smootSlider" v-model="sliderValue" type="range" min="0" max="60" :step="5" class="slider"  @mouseup="handleSliderRelease" />
    <span class="pl-2 sl-label">sampling: {{ sliderValue }} min</span>
  </div>  
  <!-- <label for="resolution" class="form-label">Select Resolution: </label>
  <select id="resolution" class="form-select form-select-lg mb-3" aria-label=".form-select-lg" v-model="resolution" @change="onRes($event)" >
    <option v-for="option in resOptions" :value="option.value" :key="option.value">
      {{ option.label }}
    </option>
  </select> -->

</template>

<script>
import axios from 'axios';
import { ref } from "vue";

export default {

  data() {
    return {
      sliderValue: 1,
      selected: 'sm-0001',
      resolution: 'min',  
      options:[],
      //resOptions:[],
      all:[]

    };
  },

  created (){
    this.selected = this.$store.state.selected
    //this.resolution = this.$store.state.resolution
    this.all = this.$store.state.allDevs
    //console.log(this.all)
    this.blynkGetNames()
    // this.resOptions = [
    //   { value: '1', label: '1min' },
    //   { value: '15', label: '15min' },
    // ];
    
    //this.setSelectOptions()
    
  },

  methods: {
    handleSliderRelease() {
      // Perform actions when the slider is released
      if (this.sliderValue == 0)
      {
        this.sliderValue = 1
      }
      this.$store.commit('setResolution', this.sliderValue)

    },

    setSelectOptions(){
      // this.blynkGetNames()
      // let allDevs = this.all
      
      // allDevs.forEach(el=>{
      //   //console.log(el)
      //   this.options.push(
      //     {
      //       "text":el.customer,
      //       "value":el.id
      //     }
      //   )
      // })
    },

    blynkGetNames(){        
        let onlineUrl = "http://209.38.208.230:8000/api/online/"
        axios.get(onlineUrl)
             .then(response => response.data.online.forEach(el=>{
                  let found = this.all.find(element => element.id === el.dev)
                 
                  found.customer = el.dev_name  
                  //console.log(found)  
                                
             }))
             .catch(errors => {})
             .finally(() => {
              //console.log(this.all)
              this.all.forEach(elm => {
                this.options.push(
                {
                  "text":elm.customer,
                  "value":elm.id

                })
              })
             })        
    },



    onChange(event)
    {
      //this.options=[]
      this.$emit("emit-sel", this.selected)
      let dev = this.selected

      let query = this.$route.query
      
      let path = this.$route.path

      //this.$router.push({path:path, query:{"range":query.range, "dev": this.selected}})
      this.$store.commit('setSelect', this.selected)
      //this.blynkGetNames()
     // console.log(this.selected)
     // this.setSelectOptions()

    },
    
    // onRes(event)
    // {
    //   this.$store.commit('setResolution', this.resolution)
    //   this.$emit("emitRes", this.resolution)
    //   //console.log('Selected resolution:', this.resolution);
      
    // }

  },



};
</script>

<style scoped>
.sel-label, .sl-label{
  color: aliceblue;
}
.slider{
  padding: 1px 1px 1px 1px;
}
</style>
