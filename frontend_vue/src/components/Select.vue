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
      options:[{"text":"","value":"sm-0004"}],

    };
  },

  created (){
    this.selected = this.$store.state.selected
    this.blynkGetNames()
  },
  methods: {

    blynkGetNames(){
      
      let url1 = "https://blynk.cloud/external/api/device/meta?token=7cxB4CX0Zcmn_8xidXJ1o0wUMwerjvRh&metaFieldId=1" //sm-0001
      let url2 = "https://blynk.cloud/external/api/device/meta?token=Kus3KqYGsvlDXdp3gS9oEnnebcd52S8q&metaFieldId=1" //sm-0002
      let url3 = "https://blynk.cloud/external/api/device/meta?token=fGSKqYFHSviVVzDF4LmKUyMAsUr0tFuZ&metaFieldId=1" //sm-0004
      let url4 = "" //sm-0003
      let url5 = "https://blynk.cloud/external/api/device/meta?token=WatW7M2so1CIwhqD2VpZ5HB3OwoFeaCq&metaFieldId=1" //sm-00011
      let url6 = "https://blynk.cloud/external/api/device/meta?token=aUXVv0mef5GLXZqvEv48Z1f0jiHweetw&metaFieldId=1" //sm-00012
      
      let blynkDevObj = {
        'sm-0001':url1,
        'sm-0002':url2,
        'sm-0004':url3,
        'sm-0003':url4,
        'sm-00011':url5,
        'sm-00012':url6,

      }

      for (const key in blynkDevObj) {

          //console.log(`${key}: ${blynkDevObj[key]}`);

          let url = blynkDevObj[key]
          
          try{
            axios
            .get(url)
            //.then(response=>this.blynkName.push({[key]:response.data.value}))  
            .then(response=>this.options.push({"text":response.data.value,"value":key})) 
            

          }catch (error) {
            console.log(error);
          }
          // axios
          //   .get(url)
          //   const response = response.data
          //   console.log(response)       

      }



      // let selected = this.selected
      // let url = blynkDevObj[selected]
      // console.log(url)
      // try{
      //   axios
      //   .get(url)
      //   .then(
      //     response => this.blynkName = response.data.value
      //     // response => response.data.forEach(el=>{
      //     //   console.log(el)
      //     // }) 
            
           
      //   )
      // }catch (error) {
      //   console.log(error);
      // }
      
      
      

    
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
      //console.log(typeof(this.blynkName))
      
      

    }

  },



};
</script>

<style scoped>

</style>
