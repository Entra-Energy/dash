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
        <th>Location</th>
        <th>Type</th>
        <th>Capacity kW</th>
        <th class="node">Node Asign</th>
        <!-- <th>T['S']</th>
        <th>P['W']</th>
        <th></th> -->

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
         <td>{{ dev.lat+"/"+dev.long }}</td>
         <td>{{ dev.type }}</td>
         <td class="capacity">
            <div class="form-inline pull-left">
             <div class="capa">
              <!-- <label for="power">Power /kW/</label> -->
               <input type="text" class="form-control d-inline-block capacity-asign" placeholder="capacity" style="width: auto;" v-model="capacityAsign[dev.id]" >
             </div>
             <div class = "submitCapa">
               <button type="submit" class="btn btn-warning sbmt-button" @click="submitCapacity(dev.id)">Submit</button>
             </div>
             </div> 
             <div class="capa-log">
              <ul>
               <li v-for="log in capaLog" :key="dev.id">
                 <span v-if="log.dev === dev.id">{{log.capacity}}</span>

               </li>
             </ul> 
            </div>

         </td>   
         <td class="node">
            <div class="form-inline">
             <div class="asign">
              <!-- <label for="power">Power /kW/</label> -->
               <input type="text" class="form-control d-inline-block node-asign" placeholder="#" style="width: auto;" v-model="nodeAsign[dev.id]" >
             </div>
             <div class = "submitNode">
               <button type="submit" class="btn btn-warning sbmt-button" @click="submitNode(dev.id)">Asign</button>
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
      nodeAsign:{},
      capacityAsign:{},
      capaLog:[],
      
      checked: {},
      allSelected: true,
      activeClass: 'disabled',
      btn_class: 'btn btn-success mb-2',
      all:[],    
      receivedDevs: [],
      errors: []
    };
  },

  methods: { 

    capacityLog(){

      axios
          .get("http://127.0.0.1:8000/api/capa_asign/")
          .then(response => response.data.results.forEach(el=>{         
            let dev = el.dev
            let capacity = el.capacity
            this.capaLog.push(
              {"dev":dev,"capacity":capacity}
            )    
          }))
          .catch(error=>{
            console.log(error)
          })

    },

    submitCapacity(dev){
      axios.post('http://127.0.0.1:8000/api/capa/', {
        "dev" : dev,
        "capacity": this.capacityAsign[dev]
      }).then(response =>{
        console.log(response.data)
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })
      this.capacityAsign = {}
    }, 


    submitNode(dev){      
      
      axios.post('http://64.225.100.195:8000/api/asign/', {
        "dev" : dev,
        "node": this.nodeAsign[dev]
      }).then(response =>{
        console.log(response.data)
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })
      this.nodeAsign = {}
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

  },

  created (){
    this.capacityLog()
    this.all = this.$store.state.allDevs
    let ids = this.$store.state.allIds
    ids.forEach(el=>{
      this.checked[el]=true
    })
    //console.log(this.all)
    
  },

  computed: {
    isDisabled: function(){
        return !this.power || !this.countDown;
    }
  },
  watch: {
   '$store.state.allDevs': {
      immediate: true,
      handler() {           
        this.all = this.$store.state.allDevs
      },
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
    padding-top: 5px;
    vertical-align: top !important;
}

.table td {    
    vertical-align: middle;   
}
.asign{
  max-width: 50%;
  margin-left: -20px;
}
.node-asign {
    max-width: 50%;
    max-height: 31px;
    font-size: 13px;
}
.capacity-asign {
    max-width: 50%;
    max-height: 31px;
    font-size: 13px;
}
.sbmt-button{
    padding: 5px 7px;
    font-size: 13px;
    color: #3c3a3a;
}
.capa{
  max-width: 50%;
  margin-left: -20px;
}
.capa-log ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.pull-left{
  float:left
}
.capa-log {
    float: left;
}
</style>
