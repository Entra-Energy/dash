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
        <th><input class="sel-all" type="checkbox" v-model="allSelected" @change="selectAll" /></th>
        <th>DevID</th>
        <th>Status</th>
        <th>Power kW</th>
        <!-- <th>Customer</th>
        <th>Location</th>
        <th>Capacity</th> -->
        <th><span class="pull-left">Start</span> <span class="dur">Duration /min/</span></th>
        <th><span class="power">Power kW</span></th>
        <th>Log</th>

      </tr>
    </thead>
    <tbody>
      <tr v-for="(dev,i) in all" :key="i">
        <td class="chckbox">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="checked[dev.id]" @change="check($event)" id="flexCheck">
          </div>
        </td>
         <td>{{ dev.id }}</td>
         <td><div v-bind:class="dev.online"></div></td>
         <td>{{ dev.pow }}</td>
         <!-- <td>{{ dev.location }}</td>
         <td>{{ "Sofia" }}</td>
         <td>{{ 10000 }}</td> -->
         <td class="date-durr">
          <!-- <div class="inter">
          <div class="row">
          <div class="col-md-12"> -->
           <div class='request-date-pick' >             
               <div class='form-row'>
                <div class="form-inline">
                 <div class="calendar-pick">
                   <DatePicker class="datepick" v-model="test[dev.id]" mode="dateTime" is24hr color="purple" :popover="{ visibility: 'focus' }" >
                   <template v-slot="{ inputValue, inputEvents }">
                     <!-- <i class="far fa-calendar-alt"></i> -->
                     <!-- <label for="schedule">Start</label> -->
                     <input
                       class="cal-input px-2 py-1 border rounded focus:outline-none focus:border-blue-300 form-control"
                       :value="test[dev.id]"
                       :disabled="!dev.ready"
                       v-on="inputEvents"
                       name="schedule"
                     />
                   </template>
                  </DatePicker>
                </div>
               <div class="duration">
                <!-- <label for="duration">duration /min/</label> -->
                 <select class="form-control d-inline-block" id="duration" :class="testClass" v-model="duration[dev.id]" @change="onChange($event)" :disabled="!dev.ready">
                   <option v-for="item in items" :value="item.val" :key="item.id" >{{item.val}}</option>
                 </select>
               </div>
               </div>
               <!-- new -->
               </div>
               </div>
              </td>
              <td class="pow-second">
               <div class="form-inline second-inline">
               <div class="pow">
                 <!-- <label for="power">Power /kW/</label> -->
                 <input type="text" name="power" class="form-control d-inline-block power-in" style="width: auto;" v-model="powVolume[dev.id]" :disabled="!dev.ready" >
               </div>

               <div class = "sendIt">
                 <button type="submit" class="btn btn-warning" @click="sendIt(dev.id)" :disabled="!dev.ready">Send</button>
               </div> 
               </div>              
               <!-- </div>-->
               </td>

     <!-- </div> -->
     <!-- </div>
     </div>
     </div> -->
       <!-- </td> -->
       <td>
        
         <div class='rowww'>
           <div class='col-sm-12w'>
           <!-- <Modal :flexi="flexiResp" :mydev="dev.id"/> -->
             <div class="flexi-display overflow-auto pt-2 pb-2" style="max-height: 30px;">
             <ul>
               <li v-for="flexi in flexiResp" :key="dev.id">
                 <span v-if="flexi.dev === dev.id">{{flexi.time}} | Duration:{{flexi.duration}} | Power: {{flexi.pow}}</span>

               </li>
             </ul>
           </div>
           </div>
         </div>
       </td>


      </tr>
     </tbody>
  </table>

</div>

</template>

<script>
import Modal from '@/components/Modal.vue'
import axios from 'axios';
import { Calendar, DatePicker } from 'v-calendar';
export default {
  components: {
     Calendar,
     DatePicker,
     Modal
   },

  data() {
    return {
      testClass : 'disabled',
      disabled: true,
      isActive: true,
      date: new Date(),
      powVolume:{},
      myObjSend:{},
      duration: {},
      items:[],
      test:{},
      flexiResp:[],
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

    testIt(dev){
//       $('#myModal').on('shown.bs.modal', function () {
//       $('#myInput').trigger('focus')
// })

    },

    sendIt(dev){


      axios.post('http://64.225.100.195:8000/api/flexi/', {       
          "date": this.test[dev],
          "duration": this.duration[dev],
          "dev":dev,
          "pow": this.powVolume[dev],
          'key':'14252)5q?12FGs'

      }).then(response => {
        // console.log(response);
        // this.response = response.data
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })
      this.test = {}
      this.items = []
      this.duration = {}
      this.powVolume = {}
      this.createMins();
      this.myObjSend = {}


    },
//
//
//
    onChange(event) {
          //console.log(event.target.value);
          //console.log(this.selected)
        },
//
      createMins(){
        for(let i=1; i<=60; i++)
        {
          this.items.push({
            'id': i,
            'val':i
          })
        }
      },
//
      pollData(){
          this.polling = setInterval(() => {
            this.getData();
        }, 10000)
      },
//
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
//
//
      check(e){
        // let checked_state = {}
        let checked_state = this.checked

        this.$store.commit('setChecked', checked_state)
        //console.log(e)
      },
//
//
//
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
    getFlexi(){
      try {
        axios
        .get(
          "http://64.225.100.195:8000/api/flexi_res/"
        )
        .then(response => response.data.forEach(el=>{

          let time = el.response_time

          time = time.split('T')
          let datePart = time[0]
          let timePart = time[1].slice(0, -1);
          let day = datePart.split('-')[2]
          let month = datePart.split('-')[1]
          let year = datePart.split('-')[0]

          let date = day + "/" + month + "/" + year + " | " + timePart

            let respObj = {
              'dev': el.flexiDev,
              'time': date,
              'pow': el.res_pow,
              'duration': el.res_durr
            }
            this.flexiResp.push(respObj)


        }

      ))

    } catch (error) {
      //console.log(error);
    }

  }

  },

  created (){
    //console.log(this.date)
    this.getData();
    this.createMins();
    this.getFlexi();
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
    },
  },
  // watch: {
  //    test: {
  //       handler: function (e) {
  //         //let dev = Object.keys()
  //
  //
  //
  //
  //           let myObj = {
  //             //"date": this.test[dev],
  //             "duration": this.duration,
  //             //"dev":dev,
  //             "pow": this.powVolume
  //           }
  //           this.myObjSend = myObj
  //
  //
  //       },
  //       deep: true
  //     }
  //    },


};
</script>

<style scoped>
.table {
    color: #e9ecef;
}
.pull-right {
  float: right;
}
/* input#inputpower {
    max-width: 160px;
    font-size: 0.65rem;
    padding: 3px;
} */
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

.calendar i {
    margin-right: 10px;
    font-size: 20px;
}
.calendar input {
    background: #e9ecef;
    cursor: pointer;
}
/* .duration::before {
  font-family: FontAwesome;
  content: "\f254";
  display: inline-block;
  padding-right: 10px;
  vertical-align: middle;
} */
/* .datepick{
  padding: .375rem .75rem;
} */
/* .duration select {
    max-height: 33px;
    max-width: 52%;
} */
.datepick i {
    margin-right: 10px;
}
.duration {    
    margin-left: 9px;
}
select#duration {
    max-width: 53px;
    padding: 3px;
}
.pow {
  max-width: 65%;
    margin-left: -9px;
    /* text-align: left; */
  }
/* .pow::before{
      font-family: FontAwesome;
      content: "\f884";
      display: inline-block;
      padding-right: 5px;
      vertical-align: middle;
      padding-left: 12px;
}
.datepick::before{
  font-family: FontAwesome;
  content: "\f073";
  display: inline-block;
  padding-right: 5px;
  vertical-align: middle;
  padding-left: 8px;
} */
/* .flexi .form-group {
  float: left;
} */
/* .sendIt {
  text-align:left;
} */

.flexi-display ul {
    list-style: none;
    margin: 0;
    padding: 0;
    color: gray;
    text-align: left;
    font-size: 12px;
    
}
.flexi-display {
    margin: 0 auto;
    
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
input.cal-input {
    /* max-width: 72%; */
}
input.power-in {
    /* max-height: 36px; */
    max-width: 50%;
}
.sendIt .btn {
    padding: 5px 7px;
    font-size: 13px;
    color: #3c3a3a;


}
.table td, .table th {
    vertical-align: middle;
}
.request-date-pick {
  /* padding-top: 14px; */
}
.form-control:disabled, .form-control[readonly] {
  background-color: #5c5c66;
}
.sendIt {
    /* margin-top: 18px; */
    margin-left: -5px;
 }

.form-inline .form-control {
    max-height: 31px;
    font-size: 13px;
}
.form-inline label {
    font-size: 12px;
}
.second-inline {
    max-width: 140px;
}
.cal-input {
    max-width: 120px;
}
th {
    font-size: 12px;
}
span.pull-left {
    float: left;
    margin-left: 44px;
}
span.power {
    float: left;
    margin-left: 4px;
}
td.date-durr {
    padding-right: 0;
}
td.pow-second {
    padding-left: 0;
}
.dur {
    margin-left: 9px;
}
.sel-all {
    margin: 7px;
}
.chckbox[data-v-bff3c4dc] {
    vertical-align: top !important;
    padding-left: 10px;
    padding-top: 10px;
}
</style>
