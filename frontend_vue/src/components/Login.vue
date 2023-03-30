<template>
  <div class = "login">
                 <form @submit.prevent="loginForm" class="form-inline">
                     <div class="form-group form-group-sm">
                       <label for="call" class="sr-only">Login</label>
                        <input type="text" class="form-control" v-model="username" id="Username" placeholder="User">
                        <input class="form-control" v-model="password" id="password" placeholder="pass" type="password">
                     </div>
                    <button type="submit" class="btn btn-warning btn btn-warning mb-2 mt-2 ml-2">Send</button>
                 </form>
  </div>
</template>
<script>

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",     
    };
  },
  methods: {
    
    loginForm(){
      this.$emit("emit-it", {username:this.username,pass:this.password})
    }
   
  },
  created(){
    
    
  }

};
</script>

<style scoped>




</style>
