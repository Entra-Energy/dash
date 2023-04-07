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
        <th>Power kW</th>
        <!-- <th>Device Name</th>
        <th>Location</th> -->
        <!-- <th>Capacity</th> -->
        <!-- <th>T['S']</th>
        <th>P['W']</th> -->
        <!-- <th></th> -->
        <th><span class="pull-left">Start</span> <span class="dur">Duration /min/</span></th>
        <th><span class="power">Power kW </span></th>
        <!-- <th> <button type="submit" class="btn btn-warning" @click="execAll()">Execute all!</button></th> -->
        <th>Log<div class="pull-right exec-all"><button type="submit" class="btn btn-success" @click="execAll()">Execute all!</button></div></th>

      </tr>
    </thead>
    <tbody>
      <tr v-for="(dev,i) in all" :key="i">
        <td class="checkboxes">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="checked[dev.id]" @change="check($event)" id="flexCheck">
          </div>
        </td>
         <td>{{ dev.id }}</td>
         <td><div v-bind:class="dev.online"></div></td>
         <td>{{ dev.pow }}</td>
        
         <td class="date-durr">
           <!-- <div class='row flexi'> -->
             <!-- <div class='col-md-3'> -->
             <!-- <div class='form-row'> -->
              <div class="form-inline">
               <div class="calendar-pick">
                 <DatePicker class="datepick" v-model="test[dev.id]" mode="dateTime" :model-config="modelConfig" is24hr color="purple" :popover="{ visibility: 'focus' }" >
                 <template v-slot="{ inputValue, inputEvents }">
                   <!-- <i class="far fa-calendar-alt"></i> -->
                   <!-- <label for="schedule">Start</label> -->
                   <input
                     class="cal-input form-control px-2 border rounded focus:outline-none focus:border-blue-300"
                     :value="test[dev.id]"
                     v-on="inputEvents"
                   />
                 </template>
               </DatePicker>
              </div>

             <div class="duration">
              <!-- <label for="duration">duration /min/</label> -->
               <select class="form-control d-inline-block" id="duration" style="width: auto;" v-model="duration[dev.id]" @change="onChange($event)" >
               <option v-for="item in items" :value="item.val" :key="item.id">{{item.val}}</option>
               </select>
             </div>
            </div>
            <!-- </div> -->
            <!-- </div> -->
            </td>
          <td class="pow-second">
            <div class="form-inline second-inline">
             <div class="pow">
              <!-- <label for="power">Power /kW/</label> -->
               <input type="text" class="form-control d-inline-block power-in" style="width: auto;" v-model="powVolume[dev.id]" >
             </div>
             <div class = "sendIt">
               <button type="submit" class="btn btn-warning" @click="sendIt(dev.id)">Send</button>
             </div>
             </div>  

       </td>
       <td>        
        <div class='rowww'>
           <div class='col-sm-12w'>
           <!-- <Modal :flexi="flexiResp" :mydev="dev.id"/> -->
             <div class="flexi-display overflow-auto pt-2 pb-2" style="max-height: 30px;">
             <ul>
               <li v-for="flexi in simLog" :key="dev.id">
                 <span v-if="flexi.dev === dev.id">{{flexi.time}} | Duration:{{flexi.duration}} | Power: {{flexi.pow}}</span>

               </li>
             </ul>
           </div>
           </div>
         </div></td>

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
      simLog:[],
      checked: {'sm-0001':true,'sm-0009':true, 'sm-0002':true,'sm-0003':true,'sm-0004':true,'sm-0000':true,'sm-00011':true,'sm-00012':true},
      allSelected: true,
      activeClass: 'disabled',
      btn_class: 'btn btn-success mb-2',

      all: [],
      posts: [],
      errors: []
    };
  },

  methods: {

    getSimLog(){
      try {
        axios
        .get(
          "http://64.225.100.195:8000/api/flexi_sim/"
        )
        //.then(response => console.log(response.data))
        .then(response => response.data.forEach(el=>{
              
          let time = el.scheduled
          time = time.split('T')
          let datePart = time[0]
          let timePart = time[1].slice(0, -1);
          let day = datePart.split('-')[2]
          let month = datePart.split('-')[1]
          let year = datePart.split('-')[0]

          let date = day + "/" + month + "/" + year + " | " + timePart
          let respObj = {
            'dev': el.provided_dev,
            'time': date,
            'pow': el.sched_pow,
            'duration': el.sched_durration
          }
          this.simLog.push(respObj)


        }

      ))

    }
    catch (error) {
      //console.log(error);
    }

    },

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

    sendIt(dev){
      let date = this.test[dev]
      axios.post('http://64.225.100.195:8000/api/sched/', {        
          "date": this.test[dev],
          "duration": this.duration[dev],
          "dev":dev,
          "pow": this.powVolume[dev],
          'key':'14252)5q?12FGs'
          
          // 'date':'2023-01-19T16:02',
          // 'duration':2,
          // 'dev': 'sm-0016',
          // 'pow': -10.5,
          // 'key':'14252)5q?12FGs'        


      }).then(response => {
        console.log(response.data)
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

    // countDownTimer () {
    //             let dev = Object.keys(this.singleCorrection)[0];
    //             //let value = this.singleCorrection[dev]
    //             this.countDown[dev] = this.time
    //             let found = this.all.find(element => element.id === dev)
    //             if (found){
    //               found.correctionT = this.time
    //               found.correctionP = this.singleCorrection[dev]
    //             }

    //             if (this.time > 0) {
    //                 setTimeout(() => {
    //                     this.time -= 1
    //                     this.countDownTimer()

    //                 }, 1000)
    //             }
    //         },

      // pollData () {
      //     this.polling = setInterval(() => {
      //       this.getData();
      //   }, 10000)
      // },

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



    //   getData() {
    //   try {
    //     axios
    //     .get(
    //       "http://64.225.100.195:8000/api/online/"
    //     )
    //     .then(response => response.data.online.forEach(el=>{
    //         //this.posts.push(el)
    //         //console.log(el.dev)
    //         let found = this.all.find(element => element.id === el.dev)


    //         if (found)
    //         {
    //           found.ready = el.ready
    //           found.pow = el.pow
    //           found.providing = el.providing
    //           found.online = 'online'

    //           if (found.ready == 1)
    //           {
    //             if (found.providing == 0)
    //             {
    //             found.online = 'ready'
    //             }
    //             else if (found.providing == 1)
    //             {
    //               found.online = 'providing'
    //             }
    //           }
    //           else if (found.ready == 0)
    //           {
    //             found.online = 'not-ready'
    //           }
    //           else{
    //             found.online = 'offline'
    //           }
    //         }

    //         //console.log(this.all[0].id)

    //     }) )
    //     //console.log(this.all)

    //   } catch (error) {
    //     //console.log(error);
    //   }
    // },

},

  created (){
    
    //this.getData();
   // this.pollData();
    this.createMins();
    this.getSimLog();
    this.all = this.$store.state.allDevs
    let ids = this.$store.state.allIds
    ids.forEach(el=>{
      this.checked[el]=true
    })
    console.log(this.simLog)

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
  max-width: 50%;
  margin-left: -20px;
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
    max-width: 72%;
    padding: 2px;
}
input.power-in {
    
    max-width: 50%;
}
.sendIt .btn {
    padding: 5px 7px;
    font-size: 13px;
    color: #3c3a3a;
}
.flexi {
  /* padding-top: 14px; */
}
.table td, .table th {
    vertical-align: middle;
}
.sendIt {   
    margin-left: -5px; 
}
span.pull-left {
  float: left;
  margin-left: 75px; 
}
.dur {
    /* float: left; */
    margin-left: 9px;

}
th {
    font-size: 12px;
}
.exec-all .btn {
    padding: 4px 7px;
    font-size: 12px;
    font-weight: bold;
    color: #e6e4e4;
}
.form-inline .form-control {
    max-height: 31px;
    font-size: 13px;
}
th.start-dur {
    width: 300px;
}
span.power {
    float: left;
    padding: 5px;
    margin: 0 auto;
    width: 38%;
}
table td.checkboxes {
    /* margin-top: 37px; */
    vertical-align: top !important;
    padding: 9px 0px 0px 5px;
}
select#duration {
    max-width: 53px;
    padding: 3px;
}
td.pow-second {
    margin-right: 0;
    padding-right: 0;
   
}

</style>
