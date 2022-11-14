<template>
  <div class='row'>
    <div class='col-md-6'>

  <!-- <form @submit.prevent="submitForm" v-on:submit="countDownTimer" class="form-inline col-xs-3">
    <div class="form-group form-group-sm">
      <label for="inputpower" class="sr-only">Reduce Power</label>
      <input type="text" class="form-control" id="inputpower" v-model="power" placeholder="Power Correction">
    </div>
    <div class="form-group form-group-sm">
      <label for="inputtime" class="sr-only">Time Interval</label>
      <input type="text" class="form-control ml-2" id="inputtime" v-model="countDown" placeholder="Time">
    </div>
    <button type="submit" :disabled='isDisabled' class="btn btn-warning mb-2 mt-2 ml-2">Send </button>
  </form> -->
</div>
<div class="col-md-6">
  <div class="pull-right">
  <!-- <form @submit.prevent="submitFormCali" v-on:submit="cali" class="form-inline">
    <div class="form-group mx-sm-3 mb-2">
      <label for="calibration" class="sr-only">Calibration</label>
      <input type="text" class="form-control" id="calibration" v-model="cali" placeholder="Calibration">
    </div>
    <button type="submit" :disabled='isDisabled' class="btn btn-warning mb-2">Send </button>
  </form> -->
</div>
</div>
</div>
  <div class="table-responsive-sm">
  <table class="table table-striped table-sm">
    <thead class="thead-light">
      <tr>
        <th>
          <div class="form-check"> <input class="sel-all" type="checkbox" v-model="allSelected" @change="selectAll($event)" /></div>
        </th>
        <th>DevID</th>
        <th>Status</th>
        <th>Power</th>
        <th>Device Name</th>
        <th>Location</th>
        <th>Capacity</th>
        <!-- <th>T['S']</th>
        <th>P['W']</th>
        <th></th> -->

      </tr>
    </thead>
    <tbody>
      <tr v-for="(dev,i) in all" :key="i">
        <td>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="checked[dev.id]" @change="check($event)" id="flexCheck">
          </div>
        </td>
         <td>{{ dev.id }}</td>
         <td><div v-bind:class="dev.online"></div></td>
         <td>{{ dev.pow }}</td>
         <td>{{ dev.customer }}</td>
         <td>{{ dev.lat+"/"+dev.long }}</td>
         <td>{{ 10000 }}</td>
         <!-- <td>{{ dev.correctionT }}</td>
         <td>{{ dev.correctionP }}</td> -->
         <!-- <td>
           <div class='row'>

             <form @submit.prevent="submitForm2" class="form-inline">
                 <div class="form-group form-group-sm">
                   <label for="call" class="sr-only">Calibrate</label>
                    <input type="text" class="form-control" v-model="newEntries[dev.id]" id="calibrate-single" placeholder="Calibrate">
                 </div>
                <button type="submit" class="btn btn-warning btn btn-warning mb-2 mt-2 ml-2">Send</button>
             </form>
             <button type="submit" class="btn btn-warning mb-2 mt-2 ml-2 reset" @click="reset(dev.id)">R </button>

        </div>
          <div class='row'>
            <form @submit.prevent="submitFormSingle" v-on:submit="countDownTimer" class="form-inline col-xs-3">
               <div class="form-group form-group-sm">
                 <label for="inputpower" class="sr-only">Reduce Power</label>
                 <input type="text" class="form-control" id="inputpower" v-model="singleCorrection[dev.id]" placeholder="Correction">
               </div>
               <div class="form-group form-group-sm">
                 <label for="inputtime" class="sr-only">Time Interval</label>
                 <input type="text" class="form-control ml-2 mr-2" id="inputtime" v-model="countDown[dev.id]" placeholder="Timer">
               </div>
               <button type="submit" class="btn btn-warning mb-2 mt-2">Send </button>
            </form>
          </div>
         </td> -->
         <!-- Timer -->
         <!-- <td><div class="mx-auto">
           <form @submit.prevent="submitFormSingle" v-on:submit="countDownTimer" class="form-inline col-xs-3">
             <div class="form-group form-group-sm">
               <label for="inputpower" class="sr-only">Reduce Power</label>
               <input type="text" class="form-control" id="inputpower" v-model="singleCorrection[dev.id]" placeholder="Power Correction">
             </div>
             <div class="form-group form-group-sm">
               <label for="inputtime" class="sr-only">Time Interval</label>
               <input type="text" class="form-control ml-2" id="inputtime" v-model="countDown[dev.id]" placeholder="Timer">
             </div>
             <button type="submit" class="btn btn-warning mb-2 mt-2 ml-2">Send </button>
           </form>
         </div>
         </td> -->
         <!-- end_Timer -->
      </tr>
     </tbody>
  </table>
</div>

</template>

<script>
import axios from 'axios';
export default {

  data() {
    return {
      power: '',
      powerCorr:'',
      time:'',
      countDown: {},
      polling: null,
      newEntries: {},
      singleCorrection:{},
      
      checked: {},
      allSelected: true,
      activeClass: 'disabled',
      btn_class: 'btn btn-success mb-2',
      all:[],    
    posts: [],
    errors: []
    };
  },

  methods: { 

      pollData () {
          this.polling = setInterval(() => {
            this.getData();
          
        }, 4000)
      },

      selectAll(e) {
          let ids = this.$store.state.allIds
          if (this.allSelected) {
            Object.keys(this.checked).forEach(key => {this.checked[key] = true;});
            
            this.$store.commit('setChecked', this.checked)

          } else {         
            Object.keys(this.checked).forEach(key => {this.checked[key] = false;});
            this.$store.commit('setChecked', this.checked)
          }

      },

      check(e){
        // let checked_state = {}
        let checked_state = this.checked

        this.$store.commit('setChecked', checked_state)
        
      },


      getData() {
        
      try {
        axios
        .get(
          "http://64.225.100.195:8000/api/online/"
        )
        .then(response => response.data.online.forEach(el=>{

            let found = this.all.find(element => element.id === el.dev)


            if (found)
            {
              found.ready = el.ready
              found.pow = el.pow
              found.providing = el.providing
              found.online = 'online'
              found.customer = el.dev_name
              found.lat = el.lat
              found.long = el.long

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
        

      } catch (error) {
        //console.log(error);
      }
    },
  },

  created (){
    
    this.getData();
    this.pollData();
    this.all = this.$store.state.allDevs
    let ids = this.$store.state.allIds
    ids.forEach(el=>{
      this.checked[el]=true
    })
   // console.log(this.checked)
    
  },
  beforeDestroy () {
	   clearInterval(this.polling)
  },
  computed: {
    isDisabled: function(){
        return !this.power || !this.countDown;
    }
  },
  
 



};
</script>

<style scoped>
.table {
    color: #e9ecef;
}
.pull-right {
  float: right;
}
input#inputpower {
    max-width: 60px;
    font-size: 0.65rem;
    padding: 3px;
}
input#inputtime {
  max-width: 60px;
  font-size: 0.65rem;
  padding: 3px;
}
input#calibrate-single {
  max-width: 60px;
  font-size: 0.65rem;
  padding: 3px;
}
.btn{
  font-size: 0.65rem;
  padding: 0.375rem 0.25rem;
}
.offline {
    width: 15px;
    height: 15px;
    background: #535353;
    border-radius: 50%;
    margin: 0 auto;
}
.not-ready {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: skyblue;
    margin: 0 auto;
}

.ready {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #5fd85f;
    margin: 0 auto;
}
.providing {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: orange;
    margin: 0 auto;
}
</style>
