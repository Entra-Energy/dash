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
      password: ""
    };
  },
  methods: {
    loginForm(){
      console.log(this.username)

      axios.post('http://127.0.0.1:8000/api/login-data/', {
        "test":"test2"

        // login: {
        //   "username": this.username,
        //   "password": this.password
        // },


      }).then(response => {
        console.log(response);
        // this.response = response.data
        this.success = 'Data saved successfully';
        this.response = JSON.stringify(response, null, 2)
      }).catch(error => {
        this.response = 'Error: ' + error.response.status
      })
      //this.newEntries = {}

    },
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
