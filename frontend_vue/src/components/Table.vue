<template>
  <div class='row'>
    <div class='col-md-6'>

  <form @submit.prevent="submitForm" v-on:submit="countDownTimer" class="form-inline">
    <div class="form-group mx-sm-3 mb-2">
      <label for="inputpower" class="sr-only">Reduce Power</label>
      <input type="text" class="form-control" id="inputpower" v-model="power" placeholder="Power Correction">
    </div>
    <div class="form-group mx-sm-3 mb-2">
      <label for="inputtime" class="sr-only">Time Interval</label>
      <input type="text" class="form-control" id="inputtime" v-model="countDown" placeholder="Time">
    </div>
    <button type="submit" :disabled='isDisabled' class="btn btn-warning mb-2">Send </button>
  </form>
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
  <table class="table table-striped">
    <thead class="thead-light">
      <tr>
        <th>DevID</th>
        <th>Status</th>
        <th>Power</th>
        <th>Customer</th>
        <th>Location</th>
        <th>Capacity</th>
        <th>Correction T {{countDown}}</th>
        <th>Correction P</th>
        <th></th>        
      </tr>
    </thead>
    <tbody>
      <tr v-for="(dev,i) in all" :key="i">
         <td>{{ dev.id }}</td>
         <td>{{ dev.online }}</td>
         <td>{{ dev.pow }}</td>
         <td>{{ "Teo" }}</td>
         <td>{{ "Sofia" }}</td>
         <td>{{ 10000 }}</td>
         <td>{{ countDown }}</td>
         <td>{{ powerCorr }}</td>
         <td><div class="mx-auto"><form @submit.prevent="submitForm" v-on:submit="countDownTimer" class="form-inline">
           <div class="form-group mx-sm-3 mb-2">
             <label for="call" class="sr-only">Reduce Power</label>
             <input type="text" class="form-control" id="calibrate-single" v-model="call" placeholder="Calibrate">
           </div>
             <button type="submit" class="btn btn-warning mb-2">Send</button>
         </form></div>
         </td>


      </tr>
     </tbody>
  </table>

</template>

<script>
import axios from 'axios';
export default {

  data() {
    return {
      power: '',
      powerCorr:'',
      countDown: '',
      test: '',
      activeClass: 'disabled',
      btn_class: 'btn btn-success mb-2',

      all: [

        {
          "id":"sm-0009","pow":"", "online":"offline","customer":"","location":"","capacity":"","correctionT":"","correctionP":"","calibration":""
        },


    ],
      posts: [],
      errors: []
    };
  },

  methods: {
      getData() {
      try {
        axios
        .get(
          "http://127.0.0.1:8000/api/online/"
        )
        .then(response => response.data.online.forEach(el=>{
            //this.posts.push(el)
            //console.log(el.dev)
            let found = this.all.find(element => element.id === el.dev)
            if (found)
            {
              found.pow = el.pow
              found.online = 'online'
            }

            //console.log(this.all[0].id)

        }) )
        //console.log(this.all)

      } catch (error) {
        //console.log(error);
      }
    },
    submitForm() {
      this.powerCorr = this.power
      axios.post('http://127.0.0.1:8000/api/correction/', {
        power: this.power,
        timer: this.countDown

      }).then(response => {
        // console.log(response);
        // this.response = response.data
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })
      this.power = '';


    },

    countDownTimer () {
                this.countDown = parseInt(this.countDown)
                this.all["correctionT"] = this.countDown

                if (this.countDown > 0) {
                    setTimeout(() => {
                        this.countDown -= 1
                        this.countDownTimer()
                    }, 1000)
                }
            },

    },

  created (){
    this.getData();
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
</style>
