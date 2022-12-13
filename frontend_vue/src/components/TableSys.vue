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
          <!-- <div class='row'>
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
          </div> -->
         </td>
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

      all: [],
      posts: [],
      errors: []
    };
  },

  methods: {

      reset(e)
      {
          axios.post('http://64.225.100.195:8000/api/reset/', {
          reset: {
            "devId":e,
            "reset":true
          },


        }).then(response => {
          // console.log(response);
          // this.response = response.data
          this.success = 'Data saved successfully';
          this.response = JSON.stringify(response, null, 2)
        }).catch(error => {
          this.response = 'Error: ' + error.response.status
        })

      },

      pollData () {
          this.polling = setInterval(() => {
            this.getData();
        }, 10000)
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


      submitForm2(){


        axios.post('http://64.225.100.195:8000/api/cali/', {
          calibrate: this.newEntries,


        }).then(response => {
          // console.log(response);
          // this.response = response.data
          this.success = 'Data saved successfully';
          this.response = JSON.stringify(response, null, 2)
        }).catch(error => {
          this.response = 'Error: ' + error.response.status
        })
        this.newEntries = {}

      },

      getData() {
      try {
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
              found.customer = el.dev_name

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

            //console.log(this.all[0].id)

        }) )
        //console.log(this.all)

      } catch (error) {
        //console.log(error);
      }
    },
    // submitForm() {
    //   this.powerCorr = this.power
    //   axios.post('http://64.225.100.195:8000/api/correction/', {
    //     power: this.power,
    //     timer: this.countDown
    //
    //   }).then(response => {
    //     // console.log(response);
    //     // this.response = response.data
    //     this.success = 'Data saved successfully';
    //     this.response = JSON.stringify(response, null, 2)
    //   }).catch(error => {
    //     this.response = 'Error: ' + error.response.status
    //   })
    //   this.power = '';
    //
    //
    // },
    // submitFormSingle() {
    //   let dev = Object.keys(this.singleCorrection)[0];
    //   let value = this.singleCorrection[dev]
    //   let time = this.countDown[dev]
    //   this.time = parseInt(time)
    //
    //   axios.post('http://64.225.100.195:8000/api/single-corr/', {
    //     power: value,
    //     timer: time,
    //     dev: dev,
    //
    //   }).then(response => {
    //     // console.log(response);
    //     // this.response = response.data
    //     this.success = 'Data saved successfully';
    //     this.response = JSON.stringify(response, null, 2)
    //   }).catch(error => {
    //     this.response = 'Error: ' + error.response.status
    //   })
    // },
    //
    // countDownTimer () {
    //             let dev = Object.keys(this.singleCorrection)[0];
    //             //let value = this.singleCorrection[dev]
    //             this.countDown[dev] = this.time
    //             let found = this.all.find(element => element.id === dev)
    //             if (found){
    //               found.correctionT = this.time
    //               found.correctionP = this.singleCorrection[dev]
    //             }
    //
    //             if (this.time > 0) {
    //                 setTimeout(() => {
    //                     this.time -= 1
    //                     this.countDownTimer()
    //
    //                 }, 1000)
    //             }
    //         },
    //
     },

  created (){
    this.getData();
    this.pollData();
    this.all = this.$store.state.allDevs
    let ids = this.$store.state.allIds
    ids.forEach(el=>{
      this.checked[el]=true
    })
    

    // const selected = this.all.map((u) => u.id);
    // this.checked = selected;
    // this.$store.commit('setChecked', this.checked)
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
