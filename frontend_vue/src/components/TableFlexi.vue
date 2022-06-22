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
        <th><input type="checkbox" v-model="allSelected" @change="selectAll" /></th>
        <th>DevID</th>
        <th>Status</th>
        <th>Power</th>
        <!-- <th>Customer</th>
        <th>Location</th>
        <th>Capacity</th> -->
        <th>Flexibility /Start Date, Duration, Power/</th>
        <th>Flexibility Log</th>

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
         <!-- <td>{{ dev.location }}</td>
         <td>{{ "Sofia" }}</td>
         <td>{{ 10000 }}</td> -->
         <td>
           <div class='row flexi'>
             <!-- <div class='col-md-3'> -->
             <div class='col-md-12'>
               <div class="form-group form-group-sm mb-2 mt-2 ml-2 mr-2">
                 <DatePicker class="datepick" v-model="test[dev.id]" mode="dateTime" is24hr color="purple" :popover="{ visibility: 'focus' }" >
                 <template v-slot="{ inputValue, inputEvents }">
                   <i class="far fa-calendar-alt"></i>
                   <input
                     class="px-2 py-1 border rounded focus:outline-none focus:border-blue-300"
                     :value="test[dev.id]"
                     v-on="inputEvents"
                   />
                 </template>
               </DatePicker>
             </div>
       <!-- </div> -->
       <!-- <div class="col-md-3"> -->
         <div class="form-group form-group-sm duration mb-2 mt-2 ml-2 mr-2">

         <select class="form-control d-inline-block" style="width: auto;" v-model="duration[dev.id]" @change="onChange($event)" >

           <option v-for="item in items" :value="item.val" :key="item.id">{{item.val}}</option>
         </select>
       </div>
     <!-- </div> -->
     <!-- <div class='col-md-3'> -->
       <div class="form-group form-group-sm pow mb-2 mt-2 ml-2 mr-2">
         <input type="text" class="form-control d-inline-block" style="width: auto;" id="pow" v-model="powVolume[dev.id]" placeholder="Power">
       </div>
     <!-- </div> -->
     <!-- <div class="col-md-3 sendIt"> -->
     <div class = "form-group form-group-sm mb-2 mt-2 ml-2 mr-2 sendIt">
       <button type="submit" class="btn btn-warning" @click="sendIt(dev.id)">Send</button>
     </div>
     <!-- </div> -->
       </div>
     </div>

       </td>
       <td>
         <div class='row'>
           <div class='col-sm-12'>
             <div class="flexi-display overflow-auto pt-3 pb-2" style="max-height: 60px;">
             <ul>
               <li v-for="flexi in flexiResp" :key="dev.id">
                 <span v-if="flexi.dev === dev.id"><b>{{flexi.dev}}</b>|{{flexi.time}}|Power:{{flexi.pow}}|Duration:{{flexi.duration}}</span>

               </li>
             </ul>
           </div>
             <!-- <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>dev</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="flexi in flexiResp" :key="dev.id">
                    <td v-if="flexi.dev === dev.id">{{flexi.dev}}</td>
                </tr>
            </tbody>
        </table> -->
             <!-- <div class="form-group form-group-sm pow mb-2 mt-2 ml-2 mr-2">
               <input type="text" class="form-control d-inline-block" style="width: auto;" id="pow" v-model="flexiResp[dev.id]" placeholder="">
             </div> -->
           </div>
         </div>
       </td>


      </tr>
     </tbody>
  </table>

</div>

</template>

<script>

import axios from 'axios';
import { Calendar, DatePicker } from 'v-calendar';
export default {
  components: {
     Calendar,
     DatePicker,
   },

  data() {
    return {
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
      checked: {'sm-0001':true,'sm-0009':true, 'sm-0002':true,'sm-0003':true,'sm-0004':true,'sm-0000':true,'sm-00011':true,'sm-00012':true},
      allSelected: true,
      activeClass: 'disabled',
      btn_class: 'btn btn-success mb-2',

      all: [

        {
          "id":"sm-0009","pow":"", "online":"offline","customer":"","location":"Teodor's Home","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },
        {
          "id":"sm-0001","pow":"", "online":"offline","customer":"","location":"Teodor's Home","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },
        {
          "id":"sm-0002","pow":"", "online":"offline","customer":"","location":"Teodor's Home","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },
        {
          "id":"sm-0003","pow":"", "online":"offline","customer":"","location":"Teodor's Home","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },
        {
          "id":"sm-0004","pow":"", "online":"offline","customer":"","location":"Office","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },
        {
          "id":"sm-0000","pow":"", "online":"offline","customer":"","location":"Office","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },
        {
          "id":"sm-00011","pow":"", "online":"offline","customer":"","location":"Energo Pro","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },
        {
          "id":"sm-00012","pow":"", "online":"offline","customer":"","location":"Energo Pro","capacity":"","correctionT":"","correctionP":"","calibration":"","ready":0
        },



    ],
      posts: [],
      errors: []
    };
  },

  methods: {

    sendIt(dev){


      axios.post('http://64.225.100.195:8000/api/flexi/', {

        //flexi: this.myObjSend,
        myObj:  {
          "date": this.test[dev],
          "duration": this.duration[dev],
          "dev":dev,
          "pow": this.powVolume[dev]
        }



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
//     onChange(event) {
//           //console.log(event.target.value);
//           //console.log(this.selected)
//         },
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
      selectAll() {
          if (this.allSelected) {
            const selected = this.all.map((u) => u.id);
            this.checked = selected;
          } else {
            this.checked = [];
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


            let respObj = {
              'dev': el.flexiDev,
              'time': el.response_time,
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

.calendar i {
    margin-right: 10px;
    font-size: 20px;
}
.calendar input {
    background: #e9ecef;
    cursor: pointer;
}
.duration:before {
  font-family: FontAwesome;
  content: "\f254";
  display: inline-block;
  padding-right: 10px;
  vertical-align: middle;
}
/* .datepick{
  padding: .375rem .75rem;
} */
.duration select {
    max-height: 33px;
}
.datepick i {
    margin-right: 10px;
}
.duration {
    text-align: left;
}
.pow {
    text-align: left;
}
.flexi .form-group {
  float: left;
}
/* .sendIt {
  text-align:left;
} */

.flexi-display ul {
    list-style: none;
    margin: 0;
    padding: 0;
    color: gray;
    text-align: left;
}
.flexi-display {
    margin: 0 auto;
}
.red {
  color: red
}
.offline {
    width: 15px;
    height: 15px;
    background: gray;
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
