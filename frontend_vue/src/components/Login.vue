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
      console.log(this.ipArr)
      console.log(this.userIp)

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
      let test = 'x'
    try {
        axios
        .get(
          "https://api.ipify.org?format=json"
        )
        .then(response => {
            test = response.data["ip"]
            this.userIp = test
            let vals = this.ipArr
            vals.forEach(el=>{

              
              if (el == test)
               {
                 console.log("test")
                 console.log(test)
               }
            })
           // console.log(this.userIp)
           // console.log(this.ipArr)
            //let vals = Object.values(this.ipArr)
            //console.log(vals)
           // const found = this.vals.find(element => element = this.userIp);
           // console.log(vals)
        }      
        )

      }catch (error) {
        //console.log(error);
      }
      //console.log(test)
  },
    getIps(){
      try {
        axios
        .get(
          "http://64.225.100.195:8000/api/userip/"
        )
        .then(response => response.data.forEach(el=>{
          this.ipArr.push(el.user_ip)
        }))       

      }catch (error) {
        //console.log(error);
      }
      
    },

    checkIp(){
      
      // let found = this.ipArr.find(element => element === this.userIp)
      // console.log(found)
    }





  },
  created(){
    this.getIps();
    this.fetchIp();    
    this.checkIp();
    
    
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
