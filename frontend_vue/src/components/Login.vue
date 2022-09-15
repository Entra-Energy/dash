<template>
  <div id="test">

                 <form @submit.prevent="loginForm" class="form-inline">
                     <div class="form-group form-group-sm">
                       <label for="call" class="sr-only">Login</label>
                        <input type="text" class="form-control" v-model="username" id="Username" placeholder="User">
                        <input class="form-control" v-model="password" id="password" placeholder="pass" type="password">>
                     </div>
                    <button type="submit" class="btn btn-warning btn btn-warning mb-2 mt-2 ml-2">Send</button>
                 </form>

  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      ipArr: [],
      userIp:'',
    };
  },
  methods: {
    loginForm(){
      console.log(this.username)

      axios.post('http://64.225.100.195:8000/api/login-data/', {
        //"test":"test2"

        login: {
          "username": this.username,
          "password": this.password,
          "ip": this.userIp
        },


      }).then(response => {
        
        if(response.data){
          //this.fetchIp()          
        }
        // this.response = response.data
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })
      //this.newEntries = {}

    },
    fetchIp(){
    try {
        axios
        .get(
          "https://api.ipify.org?format=json"
        )
        .then(response => this.userIp = response.data.ip )//console.log(response.data.ip))       

      }catch (error) {
        //console.log(error);
      }

  }
  },
  created(){
    this.fetchIp();
  }

};
</script>

<style scoped>

div#test {
    position: absolute;
    width: 100%;
    height: 100%;
    min-width: 500px;
    min-height: 500px;
    background: #837676;
    z-index: 999;
    display: none;
}
</style>
