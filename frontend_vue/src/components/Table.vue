<template>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>DevID</th>
        <th>Status</th>
        <th>Power</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(dev,i) in all" :key="i">
         <td>{{ dev.id}}</td>
         <td>{{ dev.online }}</td>
         <td>{{ dev.pow }}</td>

      </tr>
     </tbody>
  </table>

</template>

<script>
import axios from 'axios';
export default {

  data() {
    return {
      all: [

        {
          "id":"sm-0001","pow":"", "online":"offline"
        },
        {
          "id":"sm-0002","pow":"", "online":"offline"
        },
        {
          "id":"sm-0003","pow":"", "online":"offline"
        },
        {
          "id":"sm-0004","pow":"", "online":"offline"
        }

    ],
      posts: [],
      errors: []
    };
  },

  methods: {
      getData() {
        try {
     	    await axios.get('/api/posts/?range=0')
     }    catch (error) {
          const err = error as AxiosError
          if (err.response) {
           console.log(err.response.status)
           console.log(err.response.data)
          }
        this.handleAxiosError(error)
     }

    },
  },
  created (){
    this.getData();



  },



};
</script>

<style scoped>

</style>
