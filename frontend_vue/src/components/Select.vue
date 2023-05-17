<template>

  <select class="form-select form-select-lg mb-3" aria-label=".form-select-lg" v-model="selected" @change="onChange($event)" >
    <option v-for="option in options" v-bind:value="option.value">
      {{option.value}}/{{ option.text }}
    </option>
  </select>
  <p class="blynk-name">{{  }}</p>

</template>

<script>
import axios from 'axios';


export default {

  data() {
    return {

      selected: 'sm-0001',  
      options:[],
      all:[]

    };
  },

  created (){
    this.selected = this.$store.state.selected
    this.all = this.$store.state.allDevs
    //console.log(this.all)
    this.blynkGetNames()
    //this.setSelectOptions()
    
  },

  methods: {

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
      
      

    }

  },



};
</script>

<style scoped>

</style>
