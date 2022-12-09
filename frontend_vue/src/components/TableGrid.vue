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
        <th><input type="checkbox" v-model="allSelected" @change="selectAll" /></th>
        <th>DevID</th>
        <th>Status</th>
        <th>Power</th>
        <!-- <th>Device Name</th>
        <th>Location</th> -->
        <!-- <th>Capacity</th> -->
        <!-- <th>T['S']</th>
        <th>P['W']</th> -->
        <!-- <th></th> -->
        <th>Simulate</th>
        <th> <button type="submit" class="btn btn-warning" @click="execAll()">Execute all!</button></th>


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
         <!-- <td>{{ dev.customer }}</td>
         <td>{{ dev.location }}</td> -->
         <!-- <td>{{ 10000 }}</td> -->
         <!-- <td>{{ dev.correctionT }}</td>
         <td>{{ dev.correctionP }}</td> -->
         <!-- <td>
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
         <td>
           <div class='row flexi'>
             <!-- <div class='col-md-3'> -->
             <div class='form-row'>
              <div class="form-inline">
               <div class="calendar-pick">
                 <DatePicker class="datepick" v-model="test[dev.id]" mode="dateTime" :model-config="modelConfig" is24hr color="purple" :popover="{ visibility: 'focus' }" >
                 <template v-slot="{ inputValue, inputEvents }">
                   <!-- <i class="far fa-calendar-alt"></i> -->
                   <label for="schedule">Schedule</label>
                   <input
                     class="cal-input px-2 py-1 border rounded focus:outline-none focus:border-blue-300"
                     :value="test[dev.id]"
                     v-on="inputEvents"
                   />
                 </template>
               </DatePicker>
              </div>

             <div class="duration">
              <label for="duration">duration /min/</label>
               <select class="form-control d-inline-block" style="width: auto;" v-model="duration[dev.id]" @change="onChange($event)" >
               <option v-for="item in items" :value="item.val" :key="item.id">{{item.val}}</option>
               </select>
             </div>
         
             <div class="pow">
              <label for="power">Power /kW/</label>
               <input type="text" class="form-control d-inline-block power-in" style="width: auto;" v-model="powVolume[dev.id]" >
             </div>
             <div class = "sendIt">
               <button type="submit" class="btn btn-warning" @click="sendIt(dev.id)">Send</button>
             </div>
           </div>
     </div>
     </div>

       </td>
       <td></td>

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
      modelConfig: {
        type: 'string',
        mask: 'YYYY-MM-DDTHH:mm',
      },
      power: '',
      powerCorr:'',
      time:'',
      countDown: {},
      test:{},
      duration: {},
      items:[],
      powVolume:{},
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

    execAll(){
      axios.post('http://64.225.100.195:8000/api/execall/', {
        "execAll":"all"
      }).then(response => {
        // console.log(response);
        // this.response = response.data
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })
    },

    onChange(event) {
          //console.log(event.target.value);
          //console.log(this.selected)
        },

    sendIt(dev){
      let date = this.test[dev]
      console.log(date)

      axios.post('http://64.225.100.195:8000/api/sched/', {

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
    createMins(){
      for(let i=1; i<=60; i++)
      {
        this.items.push({
          'id': i,
          'val':i
        })
      }
    },
    selectAll() {
        if (this.allSelected) {
          const selected = this.all.map((u) => u.id);
          this.checked = selected;
        } else {
          this.checked = [];
        }

    },
    check(e){
      // let checked_state = {}
      let checked_state = this.checked

      this.$store.commit('setChecked', checked_state)
      //console.log(e)
    },

      submitFormSingle() {
        let dev = Object.keys(this.singleCorrection)[0];
        let value = this.singleCorrection[dev]
        let time = this.countDown[dev]
        this.time = parseInt(time)

        axios.post('http://64.225.100.195:8000/api/single-corr/', {
          power: value,
          timer: time,
          dev: dev,

        }).then(response => {
          // console.log(response);
          // this.response = response.data
          this.success = 'Data saved successfully';
          this.response = JSON.stringify(response, null, 2)
        }).catch(error => {
          this.response = 'Error: ' + error.response.status
        })
      },

    countDownTimer () {
                let dev = Object.keys(this.singleCorrection)[0];
                //let value = this.singleCorrection[dev]
                this.countDown[dev] = this.time
                let found = this.all.find(element => element.id === dev)
                if (found){
                  found.correctionT = this.time
                  found.correctionP = this.singleCorrection[dev]
                }

                if (this.time > 0) {
                    setTimeout(() => {
                        this.time -= 1
                        this.countDownTimer()

                    }, 1000)
                }
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
        console.log(checked_state)
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

},

  created (){
    
    this.getData();
    this.pollData();
    this.createMins();
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
.duration::before {
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
    /* max-height: 33px;
    max-width: 52%; */
}
.datepick i {
    margin-right: 10px;
}
.duration {
    /* text-align: left; */
}
.pow {
  margin-left: 20px;
  max-width: 94px;
}
.pow::before{
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

input.cal-input {
    max-width: 72%;
}
input.power-in {
    max-height: 36px;
    max-width: 74%;
}
.sendIt .btn {
    max-height: 36px;
}
.flexi {
  padding-top: 14px;
}
.table td, .table th {
    vertical-align: middle;
}
.sendIt {
    margin-top: 48px;
}
</style>
