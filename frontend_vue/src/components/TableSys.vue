<template>
  <div class='row'>
    <div class='col-md-6'> 
</div>
<div class="col-md-6">
  <div class="pull-right">
</div>
</div>
</div>
  <div class="table-responsive-sm">
  <table class="table table-striped table-sm">
    <thead class="thead-light">
      <tr>
        <th>
          <div class="form-check select-all-box"> <input class="sel-all" type="checkbox" v-model="allSelected" @change="selectAll($event)" /></div>
        </th>
        <th>DevID</th>
        <th>Status</th>
        <th>Power kW</th>
        <th>Device Name</th>
        <!-- <th>Location</th> -->
        <th>Capacity kW</th>
        <th></th>

      </tr>
    </thead>
    <tbody>
      <tr v-for="(dev,i) in all" :key="i">
        <td class="check-dev">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="checked[dev.id]" @change="check($event)" id="flexCheck">
          </div>
        </td>
         <td>{{ dev.id }}</td>
         <td><div v-bind:class="dev.online"></div></td>
         <td>{{ dev.pow }}</td>
         <td>{{ dev.customer }}</td>
         <!-- <td>{{ dev.location }}</td> -->
         <td>{{ 22 }}</td>
         <!-- <td>{{ dev.correctionT }}</td>
         <td>{{ dev.correctionP }}</td> -->
         <td>
           <div class='row'>

             <form @submit.prevent="submitForm2" class="form-inline">
                 <div class="form-group form-group-sm">
                   <label for="call" class="sr-only">Calibrate</label>
                    <input type="text" class="form-control" v-model="newEntries[dev.id]" id="calibrate-single" placeholder="Calibrate">
                 </div>                 
                <button type="submit" class="btn btn-warning btn mb-2 mt-2 ml-2">Send</button>               
             </form>
             <button type="submit" class="btn btn-danger mb-2 mt-2 ml-2 reset" @click="reset(dev.id)">Reset</button>

        </div>
          
         </td>

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
      all: [],
      posts: [],
      errors: []
    };
  },

  methods: {      

    
      reset(e)
      {
          axios.post('http://209.38.208.230:8000/api/reset/', {
          reset: {
            "devId":e,
            "reset":true
          },


        }).then(response => {

          this.success = 'Data saved successfully';
          this.response = JSON.stringify(response, null, 2)
        }).catch(error => {
          this.response = 'Error: ' + error.response.status
        })

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

        let checked_state = this.checked

        this.$store.commit('setChecked', checked_state)
        
      },


      submitForm2(){


        axios.post('http://209.38.208.230:8000/api/cali/', {
          calibrate: this.newEntries,


        }).then(response => {

          this.success = 'Data saved successfully';
          this.response = JSON.stringify(response, null, 2)
        }).catch(error => {
          this.response = 'Error: ' + error.response.status
        })
        this.newEntries = {}

      },    
     },

  created (){   
    this.all = this.$store.state.allDevs
    let ids = this.$store.state.allIds
    ids.forEach(el=>{
      this.checked[el]=true
    })

  },
  beforeDestroy () {
	   clearInterval(this.polling)
  },
  computed: {
    isDisabled: function(){
        return !this.power || !this.countDown;
    }
  }



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
  max-width: 73px;  
  padding: 3px;
}
.reset {
  /* font-size: 0.65rem; */
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
    background: #782686;
    margin: 0 auto;
}
.providing {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: orange;
    margin: 0 auto;
}
.form-check.select-all-box {
    padding: 0;
    margin-left: -5px;
}

td.check-dev {
    padding-top: 22px;
    vertical-align: top !important;
}

.table td {    
    vertical-align: middle;   
}
</style>
